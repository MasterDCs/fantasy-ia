# Node Description Batch 1 of 3

Graphify is running in assistant/skill mode (no API key). You are the host
assistant (Claude Code / Codex / Gemini CLI). Read the prompt below and write
your JSON answer to the answer file.

## Prompt

You are documenting nodes in a knowledge graph.
For each entry below, write ONE concise factual plain-language sentence
describing what it is or does. Use only the provided context.
For a code symbol (kind=code-symbol — a function, class, or constant),
describe what the function/symbol does based on its name, source location
and neighbors — e.g. "Resolves the configured ontology profile from graphify.yaml.".
For an entity node (any other kind — e.g. a person, place, event, object),
describe what the entity is and its role, grounded in its type, its
relations (neighbors) and the provided citations/evidence — e.g.
"Lady Carfax, a wealthy heiress who disappears en route to Lausanne.".
Ground entity descriptions in the citations/evidence when present; do not
speculate beyond the context, so a node with no supporting context may be
left out of the reply.
Write every description in Spanish (es). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "backend_fantasy_client_laligafantasyclient": "LaLigaFantasyClient" | kind=code-symbol | source=backend/fantasy_client.py:L26 | neighbors=[fantasy_client.py, .buy_player(), .get_current_round(), .get_full_data(), .get_league_standings(), .get_market()]
- "backend_ai_agent_fantasyaiagent": "FantasyAIAgent" | kind=code-symbol | source=backend/ai_agent.py:L21 | neighbors=[ai_agent.py, .analyze_full(), .analyze_player(), .chat(), ._extract_players(), .__init__()]
- "frontend_app": "app.js" | kind=code-symbol | source=frontend/app.js:L1 | neighbors=[addChatMsg(), alertIcon(), analyzePlayer(), api(), fmtMoney(), hide()]
- "backend_main": "main.py" | kind=code-symbol | source=backend/main.py:L1 | neighbors=[ActionRequest, analyze(), analyze_player(), chat(), ChatMessage, clear_cache()]
- "backend_fantasy_client_laligafantasyclient_get_full_data": ".get_full_data()" | kind=code-symbol | source=backend/fantasy_client.py:L255 | neighbors=[LaLigaFantasyClient, .get_current_round(), .get_league_standings(), .get_market(), .get_my_leagues(), .get_my_team()]
- "backend_main_get_fantasy_data": "get_fantasy_data()" | kind=code-symbol | source=backend/main.py:L54 | neighbors=[main.py, analyze(), chat(), get_market(), get_team(), Obtiene datos de Fantasy con caché]
- "frontend_app_loaddashboard": "loadDashboard()" | kind=code-symbol | source=frontend/app.js:L49 | neighbors=[app.js, api(), fmtMoney(), hide(), show(), refreshData()]
- "frontend_app_api": "api()" | kind=code-symbol | source=frontend/app.js:L352 | neighbors=[app.js, loadDashboard(), loadMarket(), loadTeam(), runAnalysis()]
- "frontend_app_hide": "hide()" | kind=code-symbol | source=frontend/app.js:L359 | neighbors=[app.js, loadDashboard(), loadMarket(), loadTeam(), runAnalysis()]
- "frontend_app_loadmarket": "loadMarket()" | kind=code-symbol | source=frontend/app.js:L244 | neighbors=[app.js, api(), hide(), show(), showTab()]
- "frontend_app_loadteam": "loadTeam()" | kind=code-symbol | source=frontend/app.js:L203 | neighbors=[app.js, api(), hide(), show(), showTab()]
- "frontend_app_runanalysis": "runAnalysis()" | kind=code-symbol | source=frontend/app.js:L86 | neighbors=[app.js, api(), hide(), renderAlerts(), show()]
- "frontend_app_show": "show()" | kind=code-symbol | source=frontend/app.js:L358 | neighbors=[app.js, loadDashboard(), loadMarket(), loadTeam(), runAnalysis()]
- "backend_ai_agent_fantasyaiagent_prepare_data_summary": "._prepare_data_summary()" | kind=code-symbol | source=backend/ai_agent.py:L144 | neighbors=[FantasyAIAgent, .analyze_full(), ._extract_players(), Prepara un resumen legible de los datos…]
- "backend_fantasy_client_laligafantasyclient_get_my_leagues": ".get_my_leagues()" | kind=code-symbol | source=backend/fantasy_client.py:L107 | neighbors=[LaLigaFantasyClient, .get_full_data(), .get_my_team(), Obtiene las ligas del usuario]
- "backend_fantasy_client_laligafantasyclient_get_my_team": ".get_my_team()" | kind=code-symbol | source=backend/fantasy_client.py:L76 | neighbors=[LaLigaFantasyClient, .get_full_data(), .get_my_leagues(), Obtiene los datos del equipo del usuario]
- "backend_main_actionrequest": "ActionRequest" | kind=code-symbol | source=backend/main.py:L46 | neighbors=[main.py, FantasyAIAgent, LaLigaFantasyClient, BaseModel]
- "backend_main_chatmessage": "ChatMessage" | kind=code-symbol | source=backend/main.py:L35 | neighbors=[main.py, FantasyAIAgent, LaLigaFantasyClient, BaseModel]
- "backend_main_lineuprequest": "LineupRequest" | kind=code-symbol | source=backend/main.py:L43 | neighbors=[main.py, FantasyAIAgent, LaLigaFantasyClient, BaseModel]
- "backend_main_playeranalysisrequest": "PlayerAnalysisRequest" | kind=code-symbol | source=backend/main.py:L39 | neighbors=[main.py, FantasyAIAgent, LaLigaFantasyClient, BaseModel]
- "basemodel": "BaseModel" | kind=code-symbol | neighbors=[ActionRequest, ChatMessage, LineupRequest, PlayerAnalysisRequest]
- "frontend_app_sendchat": "sendChat()" | kind=code-symbol | source=frontend/app.js:L298 | neighbors=[app.js, quickChat(), addChatMsg(), removeTyping()]
- "backend_ai_agent_fantasyaiagent_analyze_full": ".analyze_full()" | kind=code-symbol | source=backend/ai_agent.py:L28 | neighbors=[FantasyAIAgent, ._prepare_data_summary(), Análisis completo del equipo con recome…]
- "backend_ai_agent_fantasyaiagent_extract_players": "._extract_players()" | kind=code-symbol | source=backend/ai_agent.py:L188 | neighbors=[FantasyAIAgent, ._prepare_data_summary(), Extrae la lista de jugadores del equipo]
- "backend_fantasy_client_laligafantasyclient_get_current_round": ".get_current_round()" | kind=code-symbol | source=backend/fantasy_client.py:L175 | neighbors=[LaLigaFantasyClient, .get_full_data(), Obtiene información de la jornada actual]
- "backend_fantasy_client_laligafantasyclient_get_league_standings": ".get_league_standings()" | kind=code-symbol | source=backend/fantasy_client.py:L196 | neighbors=[LaLigaFantasyClient, .get_full_data(), Obtiene la clasificación de la liga]
- "backend_fantasy_client_laligafantasyclient_get_market": ".get_market()" | kind=code-symbol | source=backend/fantasy_client.py:L152 | neighbors=[LaLigaFantasyClient, .get_full_data(), Obtiene el mercado de fichajes]
- "backend_fantasy_client_laligafantasyclient_get_players_stats": ".get_players_stats()" | kind=code-symbol | source=backend/fantasy_client.py:L129 | neighbors=[LaLigaFantasyClient, .get_full_data(), Obtiene estadísticas de todos los jugad…]
- "backend_fantasy_client_laligafantasyclient_login": ".login()" | kind=code-symbol | source=backend/fantasy_client.py:L38 | neighbors=[LaLigaFantasyClient, .get_full_data(), Autenticación en LaLiga Fantasy]
- "backend_main_analyze": "analyze()" | kind=code-symbol | source=backend/main.py:L118 | neighbors=[main.py, get_fantasy_data(), Análisis completo con IA — endpoint pri…]
- "backend_main_chat": "chat()" | kind=code-symbol | source=backend/main.py:L136 | neighbors=[main.py, get_fantasy_data(), Chat libre con el agente de IA]
- "backend_main_get_market": "get_market()" | kind=code-symbol | source=backend/main.py:L104 | neighbors=[main.py, get_fantasy_data(), Obtiene el mercado de fichajes]
- "backend_main_get_team": "get_team()" | kind=code-symbol | source=backend/main.py:L87 | neighbors=[main.py, get_fantasy_data(), Obtiene datos del equipo]
- "backend_main_rationale_1": "Servidor FastAPI — Fantasy IA Assistant" | kind=entity | source=backend/main.py:L1 | neighbors=[FantasyAIAgent, LaLigaFantasyClient, main.py]
- "backend_main_rationale_105": "Obtiene el mercado de fichajes" | kind=entity | source=backend/main.py:L105 | neighbors=[FantasyAIAgent, LaLigaFantasyClient, get_market()]
- "backend_main_rationale_119": "Análisis completo con IA — endpoint principal" | kind=entity | source=backend/main.py:L119 | neighbors=[FantasyAIAgent, LaLigaFantasyClient, analyze()]
- "backend_main_rationale_137": "Chat libre con el agente de IA" | kind=entity | source=backend/main.py:L137 | neighbors=[FantasyAIAgent, LaLigaFantasyClient, chat()]
- "backend_main_rationale_155": "Análisis de un jugador específico" | kind=entity | source=backend/main.py:L155 | neighbors=[FantasyAIAgent, LaLigaFantasyClient, analyze_player()]
- "backend_main_rationale_166": "Guarda la alineación aprobada" | kind=entity | source=backend/main.py:L166 | neighbors=[FantasyAIAgent, LaLigaFantasyClient, set_lineup()]
- "backend_main_rationale_209": "Limpia el caché para forzar datos frescos" | kind=entity | source=backend/main.py:L209 | neighbors=[FantasyAIAgent, LaLigaFantasyClient, clear_cache()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: c:\Users\khonorat\OneDrive - NTT DATA EMEAL\Escritorio\App Fantasy\.graphify\description-instructions\batch-000.json

Keep each description factual and concise (one sentence). No markdown, no prose
outside the JSON object. It is acceptable to omit a node if context is
insufficient — but include every node you can ground confidently.

Example answer format:
```json
{
  "node_id_1": "Resolves the configured ontology profile from graphify.yaml.",
  "node_id_2": "Colonel James Barclay, an antagonist in The Crooked Man."
}
```
