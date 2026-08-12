"""
Agente de IA con Google Gemini (HTTP directo, sin SDK)
"""
import os
import json
import requests
from typing import Dict
from dotenv import load_dotenv

load_dotenv()

GEMINI_BASE = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

SYSTEM_PROMPT = """Eres un experto en LaLiga Fantasy con años de experiencia.
Analiza los datos del equipo y el mercado y proporciona recomendaciones detalladas y precisas.
Siempre responde en español. Sé directo, concreto y justifica cada recomendación con datos."""


def _call_gemini(prompt: str) -> str:
    """Llama a la API de Gemini directamente via HTTP"""
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        return "Error: GEMINI_API_KEY no configurada"

    # Intentar con gemini-2.0-flash, si falla probar con gemini-1.5-flash-latest
    models = [
        "gemini-2.0-flash",
        "gemini-1.5-flash-latest",
        "gemini-1.5-pro-latest"
    ]

    payload = {
        "contents": [{"parts": [{"text": SYSTEM_PROMPT + "\n\n" + prompt}]}],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 2048
        }
    }

    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        try:
            resp = requests.post(url, json=payload, timeout=60)
            if resp.status_code == 200:
                data = resp.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
            elif resp.status_code == 404:
                continue  # probar siguiente modelo
            else:
                return f"Error API Gemini ({model}): {resp.status_code} - {resp.text[:300]}"
        except Exception as e:
            continue

    return "Error: No se pudo conectar con ningún modelo de Gemini"


class FantasyAIAgent:
    def analyze_full(self, fantasy_data: Dict) -> Dict:
        """Análisis completo del equipo con recomendaciones"""
        data_summary = self._prepare_data_summary(fantasy_data)
        has_team_data = bool(data_summary.get("equipo"))

        if has_team_data:
            context = f"Datos reales del equipo:\n{json.dumps(data_summary, ensure_ascii=False, indent=2)}"
        else:
            context = """No se pudieron obtener datos automáticos de LaLiga Fantasy (login pendiente de configurar).
Proporciona consejos generales basados en la temporada actual de LaLiga para ayudar a ganar la liga."""

        prompt = f"""
{context}

Genera un análisis completo de LaLiga Fantasy {"con los datos reales" if has_team_data else "con consejos generales para esta temporada"}.

Devuelve EXACTAMENTE este JSON (sin texto adicional):
{{
  "resumen_situacion": "Análisis de la situación actual",
  "posicion_clasificacion": "Consejos sobre clasificación y estrategia de liga",
  "alineacion_optima": {{
    "formacion": "4-3-3",
    "titulares": [
      {{"posicion": "POR", "nombre": "Jugador recomendado", "razon": "Motivo"}}
    ],
    "suplentes": [
      {{"nombre": "Jugador suplente", "razon": "Motivo"}}
    ],
    "capitan": {{"nombre": "Jugador capitán recomendado", "razon": "Por qué capitán esta jornada"}},
    "capitan_alternativo": {{"nombre": "Alternativa capitán", "razon": "Por qué como alternativa"}}
  }},
  "mercado": {{
    "vender": [
      {{"nombre": "Jugador a vender", "precio_recomendado": 0, "urgencia": "media", "razon": "Motivo de venta"}}
    ],
    "fichar": [
      {{"nombre": "Jugador a fichar", "precio_estimado": 0, "prioridad": "alta", "razon": "Motivo de fichaje"}}
    ]
  }},
  "alertas": [
    {{"tipo": "rendimiento", "jugador": "Jugador destacado", "mensaje": "Información relevante"}}
  ],
  "estrategia_jornada": "Estrategia recomendada para maximizar puntos esta jornada",
  "puntuacion_estimada": "Estimación de puntos esperados",
  "consejo_experto": "El consejo más importante para ganar la liga esta semana"
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
Analiza al jugador {player_name} para LaLiga Fantasy en la temporada actual.
{f"Contexto: {context}" if context else ""}

Devuelve EXACTAMENTE este JSON:
{{
  "jugador": "{player_name}",
  "valoracion_general": 7,
  "forma_actual": "buena",
  "proximo_rival": "Equipo rival",
  "dificultad_rival": "media",
  "recomendacion": "mantener",
  "razon_detallada": "Análisis detallado del jugador, su momento de forma, próximos partidos y valor en fantasy",
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
{"Contexto del equipo: " + context if context else "Sin datos específicos del equipo disponibles."}

Pregunta del usuario: {message}

Responde como experto en LaLiga Fantasy en español. Sé concreto, útil y da recomendaciones específicas.
Menciona jugadores reales de LaLiga cuando sea relevante.
"""
        return _call_gemini(prompt)

    def _prepare_data_summary(self, fantasy_data: Dict) -> Dict:
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
                "jugadores": self._extract_players(team)
            }
        round_data = fantasy_data.get("current_round")
        if round_data:
            summary["jornada_actual"] = {
                "numero": round_data.get("round") or round_data.get("id", "?"),
                "estado": round_data.get("status") or round_data.get("state", "?"),
            }
        return summary

    def _extract_players(self, team: Dict) -> list:
        players = []
        raw = team.get("players") or team.get("squad") or team.get("lineup") or []
        for p in raw:
            if isinstance(p, dict):
                pl = p.get("player") or p
                players.append({
                    "nombre": pl.get("name") or pl.get("playerName", "?"),
                    "posicion": pl.get("position") or pl.get("positionId", "?"),
                    "puntos": pl.get("points") or pl.get("totalPoints", 0),
                    "precio": pl.get("marketValue") or pl.get("price", 0),
                })
        return players
