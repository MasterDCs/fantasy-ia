"""
Agente de IA con Google Gemini para análisis de Fantasy
"""
import os
import json
from typing import Dict, Optional
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


SYSTEM_PROMPT = """Eres un experto en LaLiga Fantasy con años de experiencia. 
Analiza los datos del equipo y el mercado y proporciona recomendaciones detalladas y precisas.
Siempre responde en español. Sé directo, concreto y justifica cada recomendación con datos.
Formato de respuesta: siempre usa JSON estructurado como se te indique."""


class FantasyAIAgent:
    def __init__(self):
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=SYSTEM_PROMPT
        )

    def analyze_full(self, fantasy_data: Dict) -> Dict:
        """Análisis completo del equipo con recomendaciones"""

        # Preparar resumen de datos para la IA
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
    "formacion": "4-3-3 (o la que recomiendas)",
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
      {{"nombre": "Jugador", "precio_recomendado": 0, "urgencia": "alta/media/baja", "razon": "Motivo"}}
    ],
    "fichar": [
      {{"nombre": "Jugador", "precio_estimado": 0, "prioridad": "alta/media/baja", "razon": "Motivo"}}
    ]
  }},
  "alertas": [
    {{"tipo": "lesion/sancion/precio/rendimiento", "jugador": "Nombre", "mensaje": "Detalle"}}
  ],
  "estrategia_jornada": "Descripción de la estrategia recomendada para esta jornada",
  "puntuacion_estimada": "Estimación de puntos para esta jornada",
  "consejo_experto": "Un consejo estratégico extra para ganar la liga"
}}
"""
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()

            # Limpiar respuesta si viene con markdown
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()

            result = json.loads(text)
            return {"success": True, "analysis": result}

        except json.JSONDecodeError as e:
            # Si no puede parsear JSON, devolver texto limpio
            return {
                "success": True,
                "analysis": {"texto_libre": response.text},
                "warning": "Respuesta en formato texto"
            }
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
  "valoracion_general": 0,
  "forma_actual": "buena/regular/mala",
  "proximo_rival": "Nombre del rival",
  "dificultad_rival": "baja/media/alta",
  "recomendacion": "comprar/mantener/vender",
  "razon_detallada": "Explicación completa",
  "precio_justo": 0,
  "tendencia_precio": "subiendo/estable/bajando"
}}
"""
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
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
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error al procesar la consulta: {str(e)}"

    def _prepare_data_summary(self, fantasy_data: Dict) -> Dict:
        """Prepara un resumen legible de los datos para la IA"""
        summary = {
            "autenticado": fantasy_data.get("authenticated", False),
            "errores": fantasy_data.get("errors", []),
        }

        # Datos del equipo
        team = fantasy_data.get("team")
        if team:
            summary["equipo"] = {
                "nombre": team.get("name") or team.get("teamName", "Mi Equipo"),
                "presupuesto": team.get("budget") or team.get("money", 0),
                "puntos_totales": team.get("points") or team.get("totalPoints", 0),
                "valor_plantilla": team.get("teamValue") or team.get("value", 0),
                "jugadores": self._extract_players(team)
            }

        # Jornada actual
        round_data = fantasy_data.get("current_round")
        if round_data:
            summary["jornada_actual"] = {
                "numero": round_data.get("round") or round_data.get("id", "?"),
                "estado": round_data.get("status") or round_data.get("state", "?"),
                "fecha": round_data.get("date") or round_data.get("startDate", "?")
            }

        # Clasificación
        standings = fantasy_data.get("standings")
        if standings:
            summary["clasificacion"] = standings

        # Mercado
        market = fantasy_data.get("market")
        if market:
            summary["mercado"] = market

        # Top jugadores disponibles
        players = fantasy_data.get("players_stats", [])
        if players:
            summary["top_jugadores_mercado"] = players[:20]

        return summary

    def _extract_players(self, team: Dict) -> list:
        """Extrae la lista de jugadores del equipo"""
        players = []
        raw_players = (
            team.get("players") or
            team.get("squad") or
            team.get("lineup") or
            []
        )
        for p in raw_players:
            if isinstance(p, dict):
                player_info = p.get("player") or p
                players.append({
                    "nombre": player_info.get("name") or player_info.get("playerName", "?"),
                    "posicion": player_info.get("position") or player_info.get("positionId", "?"),
                    "puntos": player_info.get("points") or player_info.get("totalPoints", 0),
                    "precio": player_info.get("marketValue") or player_info.get("price", 0),
                    "estado": player_info.get("status") or player_info.get("playerStatus", "disponible"),
                    "en_alineacion": p.get("inLineup") or p.get("starter") or False
                })
        return players


if __name__ == "__main__":
    agent = FantasyAIAgent()
    # Test básico
    test_data = {
        "authenticated": True,
        "team": {
            "name": "Mi Equipo Test",
            "budget": 5000000,
            "points": 450,
            "players": []
        },
        "current_round": {"round": 15, "status": "active"},
        "errors": []
    }
    result = agent.analyze_full(test_data)
    print(json.dumps(result, indent=2, ensure_ascii=False))
