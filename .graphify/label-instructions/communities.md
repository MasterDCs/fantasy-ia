# Community Labeling

Graphify is running in assistant/skill mode (no API key). You are the host
assistant (Claude Code / Codex / Gemini CLI). Read the community listing below
and write 2-5 word plain-language names for each.

## Language

LANGUAGE: each community line ends with a `[lang=…]` marker giving the
language of its source nodes. Write that community's name in EXACTLY that
language. Do not normalize every name to one common language.

## Communities

Community 0: api(, hide(, loadDashboard(, loadMarket(, loadTeam(, runAnalysis(, show(, app.js, addChatMsg(, alertIcon(, analyzePlayer(, fmtMoney( [lang=en]
Community 1: get_fantasy_data(, analyze(, chat(, get_market(, get_team(, Obtiene el mercado de fichajes, Análisis completo con IA — endpoint principal, Chat libre con el agente de IA, Obtiene datos de Fantasy con caché, Obtiene datos del equipo [lang=es]
Community 2: LaLigaFantasyClient, fantasy_client.py, .buy_player(, .__init__(, .sell_player(, Cliente para LaLiga Fantasy Marca API Reverse-engineered de, Ficha un jugador del mercado, Vende un jugador al mercado [lang=en]
Community 3: FantasyAIAgent, .__init__(, ActionRequest, ChatMessage, LineupRequest, PlayerAnalysisRequest, BaseModel [lang=en]
Community 4: main.py, health(, market_action(, Servidor FastAPI — Fantasy IA Assistant, Ejecuta una acción de mercado (comprar/vender, root(, serve_frontend( [lang=en]
Community 5: .analyze_full(, ._extract_players(, ._prepare_data_summary(, Prepara un resumen legible de los datos para la IA, Extrae la lista de jugadores del equipo, Análisis completo del equipo con recomendaciones [lang=es]
Community 6: .get_current_round(, .get_full_data(, .get_league_standings(, Obtiene información de la jornada actual, Obtiene la clasificación de la liga, Obtiene todos los datos necesarios para el análisis de IA [lang=es]
Community 7: .get_my_leagues(, .get_my_team(, Obtiene las ligas del usuario, Obtiene los datos del equipo del usuario [lang=es]
Community 8: .analyze_player(, Análisis específico de un jugador [lang=en]
Community 9: .chat(, Chat libre con el agente de fantasy [lang=es]
Community 10: ai_agent.py, Agente de IA con Google Gemini para análisis de Fantasy [lang=en]
Community 11: .get_market(, Obtiene el mercado de fichajes [lang=en]
Community 12: .get_players_stats(, Obtiene estadísticas de todos los jugadores [lang=en]
Community 13: .login(, Autenticación en LaLiga Fantasy [lang=en]
Community 14: .set_lineup(, Establece la alineación [lang=en]
Community 15: analyze_player(, Análisis de un jugador específico [lang=en]
Community 16: clear_cache(, Limpia el caché para forzar datos frescos [lang=es]
Community 17: Guarda la alineación aprobada, set_lineup( [lang=en]

## Instructions

Write a single JSON object mapping each community id (as a string) to its
2-5 word name to: c:\Users\khonorat\OneDrive - NTT DATA EMEAL\Escritorio\App Fantasy\.graphify\label-instructions\communities.json

Example:
```json
{
  "0": "Authentication Flow",
  "1": "Authentication Flow",
  "2": "Authentication Flow"
}
```

Then re-run `graphify update` (or `graphify label`) to ingest the names.
