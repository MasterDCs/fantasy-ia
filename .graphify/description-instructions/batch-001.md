# Node Description Batch 2 of 3

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
LANGUAGE: each entry has a `lang=` marker giving the language of its source.
Write that entry's description in EXACTLY that language. Do not translate to
a single common language — match each node's source language individually.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "backend_main_rationale_55": "Obtiene datos de Fantasy con caché" | kind=entity | source=backend/main.py:L55 | neighbors=[FantasyAIAgent, LaLigaFantasyClient, get_fantasy_data()] | lang=it
- "backend_main_rationale_88": "Obtiene datos del equipo" | kind=entity | source=backend/main.py:L88 | neighbors=[FantasyAIAgent, LaLigaFantasyClient, get_team()] | lang=en
- "frontend_app_refreshdata": "refreshData()" | kind=code-symbol | source=frontend/app.js:L345 | neighbors=[app.js, loadDashboard(), toast()] | lang=en
- "frontend_app_showtab": "showTab()" | kind=code-symbol | source=frontend/app.js:L5 | neighbors=[app.js, loadMarket(), loadTeam()] | lang=en
- "frontend_app_toast": "toast()" | kind=code-symbol | source=frontend/app.js:L16 | neighbors=[app.js, analyzePlayer(), refreshData()] | lang=en
- "backend_ai_agent": "ai_agent.py" | kind=code-symbol | source=backend/ai_agent.py:L1 | neighbors=[FantasyAIAgent, Agente de IA con Google Gemini para aná…] | lang=en
- "backend_ai_agent_fantasyaiagent_analyze_player": ".analyze_player()" | kind=code-symbol | source=backend/ai_agent.py:L97 | neighbors=[FantasyAIAgent, Análisis específico de un jugador] | lang=en
- "backend_ai_agent_fantasyaiagent_chat": ".chat()" | kind=code-symbol | source=backend/ai_agent.py:L129 | neighbors=[FantasyAIAgent, Chat libre con el agente de fantasy] | lang=en
- "backend_fantasy_client": "fantasy_client.py" | kind=code-symbol | source=backend/fantasy_client.py:L1 | neighbors=[LaLigaFantasyClient, Cliente para LaLiga Fantasy Marca API …] | lang=en
- "backend_fantasy_client_laligafantasyclient_buy_player": ".buy_player()" | kind=code-symbol | source=backend/fantasy_client.py:L233 | neighbors=[LaLigaFantasyClient, Ficha un jugador del mercado] | lang=en
- "backend_fantasy_client_laligafantasyclient_sell_player": ".sell_player()" | kind=code-symbol | source=backend/fantasy_client.py:L244 | neighbors=[LaLigaFantasyClient, Vende un jugador al mercado] | lang=en
- "backend_fantasy_client_laligafantasyclient_set_lineup": ".set_lineup()" | kind=code-symbol | source=backend/fantasy_client.py:L211 | neighbors=[LaLigaFantasyClient, Establece la alineación] | lang=en
- "backend_main_analyze_player": "analyze_player()" | kind=code-symbol | source=backend/main.py:L154 | neighbors=[main.py, Análisis de un jugador específico] | lang=en
- "backend_main_clear_cache": "clear_cache()" | kind=code-symbol | source=backend/main.py:L208 | neighbors=[main.py, Limpia el caché para forzar datos fresc…] | lang=en
- "backend_main_market_action": "market_action()" | kind=code-symbol | source=backend/main.py:L182 | neighbors=[main.py, Ejecuta una acción de mercado (comprar/…] | lang=en
- "backend_main_set_lineup": "set_lineup()" | kind=code-symbol | source=backend/main.py:L165 | neighbors=[main.py, Guarda la alineación aprobada] | lang=en
- "frontend_app_addchatmsg": "addChatMsg()" | kind=code-symbol | source=frontend/app.js:L329 | neighbors=[app.js, sendChat()] | lang=en
- "frontend_app_analyzeplayer": "analyzePlayer()" | kind=code-symbol | source=frontend/app.js:L277 | neighbors=[app.js, toast()] | lang=en
- "frontend_app_fmtmoney": "fmtMoney()" | kind=code-symbol | source=frontend/app.js:L24 | neighbors=[app.js, loadDashboard()] | lang=en
- "frontend_app_quickchat": "quickChat()" | kind=code-symbol | source=frontend/app.js:L324 | neighbors=[app.js, sendChat()] | lang=en
- "frontend_app_removetyping": "removeTyping()" | kind=code-symbol | source=frontend/app.js:L339 | neighbors=[app.js, sendChat()] | lang=en
- "frontend_app_renderalerts": "renderAlerts()" | kind=code-symbol | source=frontend/app.js:L194 | neighbors=[app.js, runAnalysis()] | lang=en
- "backend_ai_agent_fantasyaiagent_init": ".__init__()" | kind=code-symbol | source=backend/ai_agent.py:L22 | neighbors=[FantasyAIAgent] | lang=en
- "backend_ai_agent_rationale_1": "Agente de IA con Google Gemini para análisis de Fantasy" | kind=entity | source=backend/ai_agent.py:L1 | neighbors=[ai_agent.py] | lang=en
- "backend_ai_agent_rationale_130": "Chat libre con el agente de fantasy" | kind=entity | source=backend/ai_agent.py:L130 | neighbors=[.chat()] | lang=es
- "backend_ai_agent_rationale_145": "Prepara un resumen legible de los datos para la IA" | kind=entity | source=backend/ai_agent.py:L145 | neighbors=[._prepare_data_summary()] | lang=es
- "backend_ai_agent_rationale_189": "Extrae la lista de jugadores del equipo" | kind=entity | source=backend/ai_agent.py:L189 | neighbors=[._extract_players()] | lang=en
- "backend_ai_agent_rationale_29": "Análisis completo del equipo con recomendaciones" | kind=entity | source=backend/ai_agent.py:L29 | neighbors=[.analyze_full()] | lang=en
- "backend_ai_agent_rationale_98": "Análisis específico de un jugador" | kind=entity | source=backend/ai_agent.py:L98 | neighbors=[.analyze_player()] | lang=en
- "backend_fantasy_client_laligafantasyclient_init": ".__init__()" | kind=code-symbol | source=backend/fantasy_client.py:L27 | neighbors=[LaLigaFantasyClient] | lang=en
- "backend_fantasy_client_rationale_1": "Cliente para LaLiga Fantasy Marca API\r Reverse-engineered de la app oficial" | kind=entity | source=backend/fantasy_client.py:L1 | neighbors=[fantasy_client.py] | lang=es
- "backend_fantasy_client_rationale_108": "Obtiene las ligas del usuario" | kind=entity | source=backend/fantasy_client.py:L108 | neighbors=[.get_my_leagues()] | lang=es
- "backend_fantasy_client_rationale_130": "Obtiene estadísticas de todos los jugadores" | kind=entity | source=backend/fantasy_client.py:L130 | neighbors=[.get_players_stats()] | lang=en
- "backend_fantasy_client_rationale_153": "Obtiene el mercado de fichajes" | kind=entity | source=backend/fantasy_client.py:L153 | neighbors=[.get_market()] | lang=en
- "backend_fantasy_client_rationale_176": "Obtiene información de la jornada actual" | kind=entity | source=backend/fantasy_client.py:L176 | neighbors=[.get_current_round()] | lang=en
- "backend_fantasy_client_rationale_197": "Obtiene la clasificación de la liga" | kind=entity | source=backend/fantasy_client.py:L197 | neighbors=[.get_league_standings()] | lang=en
- "backend_fantasy_client_rationale_212": "Establece la alineación" | kind=entity | source=backend/fantasy_client.py:L212 | neighbors=[.set_lineup()] | lang=en
- "backend_fantasy_client_rationale_234": "Ficha un jugador del mercado" | kind=entity | source=backend/fantasy_client.py:L234 | neighbors=[.buy_player()] | lang=en
- "backend_fantasy_client_rationale_245": "Vende un jugador al mercado" | kind=entity | source=backend/fantasy_client.py:L245 | neighbors=[.sell_player()] | lang=fr
- "backend_fantasy_client_rationale_256": "Obtiene todos los datos necesarios para el análisis de IA" | kind=entity | source=backend/fantasy_client.py:L256 | neighbors=[.get_full_data()] | lang=es

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: c:\Users\khonorat\OneDrive - NTT DATA EMEAL\Escritorio\App Fantasy\.graphify\description-instructions\batch-001.json

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
