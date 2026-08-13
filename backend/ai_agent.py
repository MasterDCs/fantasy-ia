"""
Agente de IA con Google Gemini (HTTP directo, sin SDK)
Modelos: gemini-2.5-flash, gemini-2.5-pro, gemini-2.5-flash-lite (confirmados disponibles)
"""
import os
import json
import requests
from typing import Dict
from dotenv import load_dotenv

load_dotenv()

# Modelos disponibles confirmados por /api/gemini-test
GEMINI_MODELS = [
    ("v1beta", "gemini-2.5-flash"),
    ("v1beta", "gemini-2.5-pro"),
    ("v1beta", "gemini-2.5-flash-lite"),
    ("v1beta", "gemini-flash-latest"),
]

SYSTEM_PROMPT = """Eres un experto en LaLiga Fantasy Marca con años de experiencia.
Conoces a fondo a todos los jugadores de LaLiga, sus estadísticas, lesiones, rachas y valores en el juego.
Siempre respondes en español. Eres directo, concreto y das recomendaciones específicas con jugadores reales."""


def _call_gemini(prompt: str) -> str:
    """Llama a la API de Gemini directamente via HTTP"""
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        return "Error: GEMINI_API_KEY no configurada"

    payload = {
        "contents": [{"parts": [{"text": SYSTEM_PROMPT + "\n\n" + prompt}]}],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 2048
        }
    }

    last_error = ""
    for api_version, model in GEMINI_MODELS:
        url = f"https://generativelanguage.googleapis.com/{api_version}/models/{model}:generateContent?key={api_key}"
        try:
            resp = requests.post(url, json=payload, timeout=60)
            if resp.status_code == 200:
                data = resp.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
            else:
                last_error = f"{api_version}/{model} → {resp.status_code}: {resp.text[:150]}"
        except Exception as e:
            last_error = str(e)

    return f"Error Gemini: {last_error}"


def _extract_json(text: str) -> str:
    """Extrae el JSON de una respuesta que puede tener texto extra o markdown alrededor"""
    # Limpiar bloques markdown tipo ```json ... ```
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0]
    elif "```" in text:
        text = text.split("```")[1].split("```")[0]
    text = text.strip()
    # Buscar primer { y último } para extraer solo el JSON
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1 and end > start:
        return text[start:end + 1]
    return text


class FantasyAIAgent:

    def analyze_full(self, fantasy_data: Dict) -> Dict:
        """Análisis completo del equipo con recomendaciones"""
        data_summary = self._prepare_data_summary(fantasy_data)
        has_team_data = bool(data_summary.get("equipo") and data_summary["equipo"].get("jugadores"))

        if has_team_data:
            context = f"Datos reales del equipo:\n{json.dumps(data_summary, ensure_ascii=False, indent=2)}"
            mode = "con los datos reales del equipo"
        else:
            context = "No hay datos del equipo disponibles (login de LaLiga Fantasy pendiente)."
            mode = "con consejos generales basados en la jornada actual de LaLiga"

        prompt = f"""
{context}

Genera un análisis completo de LaLiga Fantasy Marca {mode}.
Usa jugadores reales de LaLiga y sé muy específico con nombres, precios y razonamientos.

Devuelve EXACTAMENTE este JSON (sin texto adicional, sin markdown):
{{
  "resumen_situacion": "Análisis breve de la situación / contexto de la jornada",
  "posicion_clasificacion": "Consejos para mejorar posición en la liga",
  "alineacion_optima": {{
    "formacion": "4-3-3",
    "titulares": [
      {{"posicion": "POR", "nombre": "Nombre real", "razon": "Motivo específico"}},
      {{"posicion": "DEF", "nombre": "Nombre real", "razon": "Motivo específico"}},
      {{"posicion": "DEF", "nombre": "Nombre real", "razon": "Motivo específico"}},
      {{"posicion": "DEF", "nombre": "Nombre real", "razon": "Motivo específico"}},
      {{"posicion": "DEF", "nombre": "Nombre real", "razon": "Motivo específico"}},
      {{"posicion": "MED", "nombre": "Nombre real", "razon": "Motivo específico"}},
      {{"posicion": "MED", "nombre": "Nombre real", "razon": "Motivo específico"}},
      {{"posicion": "MED", "nombre": "Nombre real", "razon": "Motivo específico"}},
      {{"posicion": "DEL", "nombre": "Nombre real", "razon": "Motivo específico"}},
      {{"posicion": "DEL", "nombre": "Nombre real", "razon": "Motivo específico"}},
      {{"posicion": "DEL", "nombre": "Nombre real", "razon": "Motivo específico"}}
    ],
    "suplentes": [
      {{"nombre": "Nombre real", "razon": "Motivo"}},
      {{"nombre": "Nombre real", "razon": "Motivo"}},
      {{"nombre": "Nombre real", "razon": "Motivo"}}
    ],
    "capitan": {{"nombre": "Nombre real", "razon": "Por qué capitán esta jornada"}},
    "capitan_alternativo": {{"nombre": "Nombre real", "razon": "Alternativa"}}
  }},
  "mercado": {{
    "vender": [
      {{"nombre": "Jugador real", "precio_recomendado": 5000000, "urgencia": "alta", "razon": "Motivo concreto"}}
    ],
    "fichar": [
      {{"nombre": "Jugador real", "precio_estimado": 3000000, "prioridad": "alta", "razon": "Motivo concreto"}}
    ]
  }},
  "alertas": [
    {{"tipo": "lesion", "jugador": "Nombre real", "mensaje": "Detalle"}}
  ],
  "estrategia_jornada": "Estrategia detallada para maximizar puntos",
  "puntuacion_estimada": "Entre X y Y puntos esperados",
  "consejo_experto": "El consejo más importante para ganar esta semana"
}}
"""
        try:
            text = _call_gemini(prompt).strip()
            json_text = _extract_json(text)
            result = json.loads(json_text)
            return {"success": True, "analysis": result}
        except json.JSONDecodeError:
            return {"success": True, "analysis": {"texto_libre": text}, "warning": "Formato texto"}
        except Exception as e:
            return {"success": False, "error": str(e), "analysis": None}

    def analyze_player(self, player_name: str, context: str = "") -> Dict:
        """Análisis específico de un jugador"""
        prompt = f"""
Analiza al jugador {player_name} para LaLiga Fantasy Marca en la temporada actual.
{f"Contexto adicional: {context}" if context else ""}

Devuelve EXACTAMENTE este JSON (sin markdown):
{{
  "jugador": "{player_name}",
  "valoracion_general": 7,
  "forma_actual": "buena",
  "proximo_rival": "Nombre del rival próximo",
  "dificultad_rival": "baja",
  "recomendacion": "comprar",
  "razon_detallada": "Análisis detallado: forma, estadísticas, próximos partidos y valor en fantasy",
  "precio_justo": 5000000,
  "tendencia_precio": "subiendo"
}}
"""
        try:
            text = _call_gemini(prompt).strip()
            json_text = _extract_json(text)
            return {"success": True, "analysis": json.loads(json_text)}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def chat(self, message: str, context: str = "") -> str:
        """Chat libre con el agente de fantasy"""
        prompt = f"""
{"Contexto del equipo del usuario: " + context if context else "El usuario no tiene datos del equipo cargados aún."}

Pregunta: {message}

Responde como experto en LaLiga Fantasy Marca. Sé muy concreto:
- Menciona jugadores reales con sus nombres
- Da precios aproximados cuando sea relevante
- Justifica cada recomendación con datos reales (lesiones, rachas, próximos rivales)
- Responde en español siempre
- Máximo 3-4 párrafos, sin listas excesivas
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
