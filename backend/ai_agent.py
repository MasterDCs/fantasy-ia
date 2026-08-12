"""
Agente de IA con Google Gemini (HTTP directo, sin SDK)
"""
import os
import json
import requests
from typing import Dict, Optional
from dotenv import load_dotenv

load_dotenv()

GEMINI_BASE = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

SYSTEM_PROMPT = """Eres un experto en LaLiga Fantasy con años de experiencia.
Analiza los datos del equipo y el mercado y proporciona recomendaciones detalladas y precisas.
Siempre responde en español. Sé directo, concreto y justifica cada recomendación con datos."""


def _call_gemini(prompt: str) -> str:
    """Llama a la API de Gemini directamente via HTTP"""
    api_key = os.getenv("GEMINI_API_KEY", "")
    url = f"{GEMINI_BASE}?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": SYSTEM_PROMPT + "\n\n" + prompt}]}],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 2048
        }
    }
    try:
        resp = requests.post(url, json=payload, timeout=60)
        if resp.status_code == 200:
            data = resp.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"Error API Gemini: {resp.status_code} - {resp.text[:200]}"
    except Exception as e:
        return f"Error llamando a Gemini: {str(e)}"


class FantasyAIAgent:
    def analyze_full(self, fantasy_data: Dict) -> Dict:
        """Análisis completo del equipo con recomendaciones"""
        data_summary = self._prepare_data_summary(fantasy_data)

        prompt = f"""
Analiza los siguientes datos de mi equipo de LaLiga Fantasy y dame un análisis completo.

DATOS DE MI EQUIPO Y MERCADO:
{json.dumps(data_summary, ensure_ascii=False, indent=2)}

Devuelve EXACTAMENTE este JSON (sin texto adicional, solo el JSON):
{{
  "resumen_situacion": "Descripción breve de la situación actual del equipo",
  "posicion_clasificacion": "Tu posición actual en la liga y análisis",
  "alineacion_optima": {{
    "formacion": "4-3-3",
    "titulares": [
      {{"posicion": "POR", "nombre": "Nombre jugador", "razon": "Por qué titular"}}
    ],
    "suplentes": [
      {{"nombre": "Nombre jugador", "razon": "Por qué suplente"}}
    ],
    "capitan": {{"nombre": "Nombre jugador", "razon": "Por qué capitán"}},
    "capitan_alternativo": {{"nombre": "Nombre jugador", "razon": "Alternativa"}}
  }},
  "mercado": {{
    "vender": [
      {{"nombre": "Jugador", "precio_recomendado": 0, "urgencia": "alta", "razon": "Motivo"}}
    ],
    "fichar": [
      {{"nombre": "Jugador", "precio_estimado": 0, "prioridad": "alta", "razon": "Motivo"}}
    ]
  }},
  "alertas": [
    {{"tipo": "lesion", "jugador": "Nombre", "mensaje": "Detalle"}}
  ],
  "estrategia_jornada": "Descripción de la estrategia recomendada para esta jornada",
  "puntuacion_estimada": "Estimación de puntos para esta jornada",
  "consejo_experto": "Un consejo estratégico extra para ganar la liga"
}}
"""
        try:
            text = _call_gemini(prompt).strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()
            result = json.loads(text)
            return {"success": True, "analysis": result}
        except json.JSONDecodeError:
            return {"success": True, "analysis": {"texto_libre": text}, "warning": "Formato texto"}
        except Exception as e:
            return {"success": False, "error": str(e), "analysis": None}

    def analyze_player(self, player_name: str, context: str = "") -> Dict:
        """Análisis específico de un jugador"""
        prompt = f"""
Analiza al jugador {player_name} para LaLiga Fantasy.
Contexto adicional: {context}

Devuelve EXACTAMENTE este JSON:
{{
  "jugador": "{player_name}",
  "valoracion_general": 7,
  "forma_actual": "buena",
  "proximo_rival": "Nombre del rival",
  "dificultad_rival": "media",
  "recomendacion": "mantener",
  "razon_detallada": "Explicación completa",
  "precio_justo": 0,
  "tendencia_precio": "estable"
}}
"""
        try:
            text = _call_gemini(prompt).strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            return {"success": True, "analysis": json.loads(text.strip())}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def chat(self, message: str, context: str = "") -> str:
        """Chat libre con el agente de fantasy"""
        prompt = f"""
Contexto de mi equipo: {context}

Pregunta: {message}

Responde como experto en LaLiga Fantasy en español, de forma concisa y práctica.
"""
        return _call_gemini(prompt)

    def _prepare_data_summary(self, fantasy_data: Dict) -> Dict:
        """Prepara un resumen legible de los datos para la IA"""
        summary = {
            "autenticado": fantasy_data.get("authenticated", False),
            "errores": fantasy_data.get("errors", []),
        }
        team = fantasy_data.get("team")
        if team:
            summary["equipo"] = {
                "nombre": team.get("name") or team.get("teamName", "Mi Equipo"),
                "presupuesto": team.get("budget") or team.get("money", 0),
                "puntos_totales": team.get("points") or team.get("totalPoints", 0),
                "valor_plantilla": team.get("teamValue") or team.get("value", 0),
                "jugadores": self._extract_players(team)
            }
        round_data = fantasy_data.get("current_round")
        if round_data:
            summary["jornada_actual"] = {
                "numero": round_data.get("round") or round_data.get("id", "?"),
                "estado": round_data.get("status") or round_data.get("state", "?"),
            }
        standings = fantasy_data.get("standings")
        if standings:
            summary["clasificacion"] = standings
        market = fantasy_data.get("market")
        if market:
            summary["mercado"] = market
        players = fantasy_data.get("players_stats", [])
        if players:
            summary["top_jugadores_mercado"] = players[:20]
        return summary

    def _extract_players(self, team: Dict) -> list:
        players = []
        raw_players = team.get("players") or team.get("squad") or team.get("lineup") or []
        for p in raw_players:
            if isinstance(p, dict):
                pl = p.get("player") or p
                players.append({
                    "nombre": pl.get("name") or pl.get("playerName", "?"),
                    "posicion": pl.get("position") or pl.get("positionId", "?"),
                    "puntos": pl.get("points") or pl.get("totalPoints", 0),
                    "precio": pl.get("marketValue") or pl.get("price", 0),
                    "estado": pl.get("status") or pl.get("playerStatus", "ok"),
                })
        return players
