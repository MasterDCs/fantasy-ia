"""
Servidor FastAPI — Fantasy IA Assistant
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import json
import os
from datetime import datetime

from fantasy_client import LaLigaFantasyClient
from ai_agent import FantasyAIAgent

app = FastAPI(title="Fantasy IA Assistant", version="1.0.0")

# CORS para permitir acceso desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cache simple en memoria
cache: Dict[str, Any] = {}
CACHE_TTL = 300  # 5 minutos


# ─── Modelos ───────────────────────────────────────────────────────────────────

class ChatMessage(BaseModel):
    message: str
    include_team_context: bool = True

class PlayerAnalysisRequest(BaseModel):
    player_name: str
    context: Optional[str] = ""

class LineupRequest(BaseModel):
    lineup: Dict

class ActionRequest(BaseModel):
    action: str  # "buy" | "sell"
    player_id: str
    price: int


# ─── Helpers ───────────────────────────────────────────────────────────────────

def get_fantasy_data(force_refresh: bool = False) -> Dict:
    """Obtiene datos de Fantasy con caché"""
    cache_key = "fantasy_data"
    now = datetime.now().timestamp()

    if not force_refresh and cache_key in cache:
        cached = cache[cache_key]
        if now - cached["timestamp"] < CACHE_TTL:
            return cached["data"]

    client = LaLigaFantasyClient()
    data = client.get_full_data()
    cache[cache_key] = {"data": data, "timestamp": now}
    return data


# ─── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"status": "ok", "message": "Fantasy IA Assistant API", "version": "1.0.0"}


@app.get("/api/health")
def health():
    return {
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "cache_entries": len(cache)
    }


@app.get("/api/team")
def get_team(refresh: bool = False):
    """Obtiene datos del equipo"""
    try:
        data = get_fantasy_data(force_refresh=refresh)
        return {
            "success": data.get("authenticated", False),
            "team": data.get("team"),
            "leagues": data.get("leagues", []),
            "current_round": data.get("current_round"),
            "standings": data.get("standings"),
            "errors": data.get("errors", [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/market")
def get_market(refresh: bool = False):
    """Obtiene el mercado de fichajes"""
    try:
        data = get_fantasy_data(force_refresh=refresh)
        return {
            "success": True,
            "market": data.get("market"),
            "players_stats": data.get("players_stats", [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/analyze")
def analyze(refresh: bool = False):
    """Análisis completo con IA — endpoint principal"""
    try:
        data = get_fantasy_data(force_refresh=refresh)
        agent = FantasyAIAgent()
        result = agent.analyze_full(data)

        # Añadir metadata
        result["timestamp"] = datetime.now().isoformat()
        result["data_available"] = data.get("authenticated", False)
        result["errors"] = data.get("errors", [])

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/chat")
def chat(req: ChatMessage):
    """Chat libre con el agente de IA"""
    try:
        context = ""
        if req.include_team_context:
            data = get_fantasy_data()
            team = data.get("team")
            if team:
                context = f"Equipo: {team.get('name', 'Mi equipo')}, Puntos: {team.get('points', 0)}, Presupuesto: {team.get('budget', 0)}"

        agent = FantasyAIAgent()
        response = agent.chat(req.message, context)
        return {"success": True, "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/player/analyze")
def analyze_player(req: PlayerAnalysisRequest):
    """Análisis de un jugador específico"""
    try:
        agent = FantasyAIAgent()
        result = agent.analyze_player(req.player_name, req.context or "")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/lineup/set")
def set_lineup(req: LineupRequest):
    """Guarda la alineación aprobada"""
    try:
        client = LaLigaFantasyClient()
        if not client.login():
            raise HTTPException(status_code=401, detail="No se pudo autenticar")
        # Obtener team_id
        client.get_my_team()
        success = client.set_lineup(req.lineup)
        return {"success": success, "message": "Alineación guardada" if success else "Error al guardar"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/market/action")
def market_action(req: ActionRequest):
    """Ejecuta una acción de mercado (comprar/vender)"""
    try:
        client = LaLigaFantasyClient()
        if not client.login():
            raise HTTPException(status_code=401, detail="No se pudo autenticar")

        if req.action == "buy":
            success = client.buy_player(req.player_id, req.price)
            msg = "Jugador fichado correctamente" if success else "Error al fichar"
        elif req.action == "sell":
            success = client.sell_player(req.player_id, req.price)
            msg = "Jugador vendido correctamente" if success else "Error al vender"
        else:
            raise HTTPException(status_code=400, detail="Acción no válida")

        # Invalidar caché
        cache.clear()
        return {"success": success, "message": msg}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/cache")
def clear_cache():
    """Limpia el caché para forzar datos frescos"""
    cache.clear()
    return {"success": True, "message": "Caché limpiado"}


# ─── Servir frontend ───────────────────────────────────────────────────────────

frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/app", StaticFiles(directory=frontend_path, html=True), name="frontend")

    @app.get("/app")
    def serve_frontend():
        return FileResponse(os.path.join(frontend_path, "index.html"))


# ─── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando Fantasy IA Assistant...")
    print("📱 Dashboard: http://localhost:8000/app")
    print("📡 API Docs: http://localhost:8000/docs")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
