# Graph Report - .  (2026-08-12)

## Corpus Check
- Corpus is ~3556 words - fits in a single context window. You may not need a graph.

## Summary
- 89 nodes · 150 edges · 18 communities detected
- Extraction: 83% EXTRACTED · 17% INFERRED · 0% AMBIGUOUS · INFERRED: 26 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output
- Edge kinds: contains: 38 · calls: 36 · rationale_for: 28 · uses: 26 · method: 18 · inherits: 4


## Input Scope
- Requested: all
- Resolved: all (source: configured-default)
- Included files: 4 · Candidates: recursive
- Excluded: 0 untracked · 0 ignored · 0 sensitive · 0 missing committed
## God Nodes (most connected - your core abstractions)
1. `LaLigaFantasyClient` - 26 edges
2. `FantasyAIAgent` - 20 edges
3. `get_fantasy_data()` - 6 edges
4. `loadDashboard()` - 6 edges
5. `runAnalysis()` - 5 edges
6. `loadTeam()` - 5 edges
7. `loadMarket()` - 5 edges
8. `api()` - 5 edges
9. `show()` - 5 edges
10. `hide()` - 5 edges

## Surprising Connections (you probably didn't know these)
- `ActionRequest` --uses--> `LaLigaFantasyClient`  [INFERRED]
  backend/main.py → backend/fantasy_client.py
- `ChatMessage` --uses--> `LaLigaFantasyClient`  [INFERRED]
  backend/main.py → backend/fantasy_client.py
- `LineupRequest` --uses--> `LaLigaFantasyClient`  [INFERRED]
  backend/main.py → backend/fantasy_client.py
- `PlayerAnalysisRequest` --uses--> `LaLigaFantasyClient`  [INFERRED]
  backend/main.py → backend/fantasy_client.py
- `Servidor FastAPI — Fantasy IA Assistant` --uses--> `FantasyAIAgent`  [INFERRED]
  backend/main.py → backend/ai_agent.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.20
Nodes (17): addChatMsg(), analyzePlayer(), api(), fmtMoney(), hide(), loadDashboard(), loadMarket(), loadTeam() (+9 more)

### Community 1 - "Community 1"
Cohesion: 0.20
Nodes (10): analyze(), chat(), get_fantasy_data(), get_market(), get_team(), Obtiene el mercado de fichajes, Análisis completo con IA — endpoint principal, Chat libre con el agente de IA (+2 more)

### Community 2 - "Community 2"
Cohesion: 0.25
Nodes (4): LaLigaFantasyClient, Cliente para LaLiga Fantasy Marca API Reverse-engineered de la app oficial, Ficha un jugador del mercado, Vende un jugador al mercado

### Community 3 - "Community 3"
Cohesion: 0.43
Nodes (6): FantasyAIAgent, ActionRequest, ChatMessage, LineupRequest, PlayerAnalysisRequest, BaseModel

### Community 4 - "Community 4"
Cohesion: 0.29
Nodes (3): market_action(), Servidor FastAPI — Fantasy IA Assistant, Ejecuta una acción de mercado (comprar/vender)

### Community 5 - "Community 5"
Cohesion: 0.33
Nodes (3): Prepara un resumen legible de los datos para la IA, Extrae la lista de jugadores del equipo, Análisis completo del equipo con recomendaciones

### Community 6 - "Community 6"
Cohesion: 0.33
Nodes (3): Obtiene información de la jornada actual, Obtiene la clasificación de la liga, Obtiene todos los datos necesarios para el análisis de IA

### Community 7 - "Community 7"
Cohesion: 0.50
Nodes (2): Obtiene las ligas del usuario, Obtiene los datos del equipo del usuario

### Community 8 - "Community 8"
Cohesion: 1.00
Nodes (1): Análisis específico de un jugador

### Community 9 - "Community 9"
Cohesion: 1.00
Nodes (1): Chat libre con el agente de fantasy

### Community 10 - "Community 10"
Cohesion: 1.00
Nodes (1): Agente de IA con Google Gemini para análisis de Fantasy

### Community 11 - "Community 11"
Cohesion: 1.00
Nodes (1): Obtiene el mercado de fichajes

### Community 12 - "Community 12"
Cohesion: 1.00
Nodes (1): Obtiene estadísticas de todos los jugadores

### Community 13 - "Community 13"
Cohesion: 1.00
Nodes (1): Autenticación en LaLiga Fantasy

### Community 14 - "Community 14"
Cohesion: 1.00
Nodes (1): Establece la alineación

### Community 15 - "Community 15"
Cohesion: 1.00
Nodes (2): analyze_player(), Análisis de un jugador específico

### Community 16 - "Community 16"
Cohesion: 1.00
Nodes (2): clear_cache(), Limpia el caché para forzar datos frescos

### Community 17 - "Community 17"
Cohesion: 1.00
Nodes (2): Guarda la alineación aprobada, set_lineup()

## Knowledge Gaps
- **19 isolated node(s):** `Agente de IA con Google Gemini para análisis de Fantasy`, `Análisis completo del equipo con recomendaciones`, `Análisis específico de un jugador`, `Chat libre con el agente de fantasy`, `Prepara un resumen legible de los datos para la IA` (+14 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 7`** (2 nodes): `Obtiene las ligas del usuario`, `Obtiene los datos del equipo del usuario`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 8`** (1 nodes): `Análisis específico de un jugador`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 9`** (1 nodes): `Chat libre con el agente de fantasy`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 10`** (1 nodes): `Agente de IA con Google Gemini para análisis de Fantasy`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 11`** (1 nodes): `Obtiene el mercado de fichajes`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 12`** (1 nodes): `Obtiene estadísticas de todos los jugadores`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 13`** (1 nodes): `Autenticación en LaLiga Fantasy`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 14`** (1 nodes): `Establece la alineación`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 15`** (2 nodes): `analyze_player()`, `Análisis de un jugador específico`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 16`** (2 nodes): `clear_cache()`, `Limpia el caché para forzar datos frescos`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 17`** (2 nodes): `Guarda la alineación aprobada`, `set_lineup()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LaLigaFantasyClient` connect `Community 2` to `Community 6`, `Community 11`, `Community 7`, `Community 12`, `Community 13`, `Community 14`, `Community 3`, `Community 4`, `Community 1`, `Community 15`, `Community 17`, `Community 16`?**
  _High betweenness centrality (0.348) - this node is a cross-community bridge._
- **Why does `FantasyAIAgent` connect `Community 3` to `Community 10`, `Community 5`, `Community 8`, `Community 9`, `Community 4`, `Community 1`, `Community 15`, `Community 17`, `Community 16`?**
  _High betweenness centrality (0.217) - this node is a cross-community bridge._
- **Why does `ChatMessage` connect `Community 3` to `Community 4`, `Community 2`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `LaLigaFantasyClient` (e.g. with `ActionRequest` and `ChatMessage`) actually correct?**
  _`LaLigaFantasyClient` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `FantasyAIAgent` (e.g. with `ActionRequest` and `ChatMessage`) actually correct?**
  _`FantasyAIAgent` has 13 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Agente de IA con Google Gemini para análisis de Fantasy`, `Análisis completo del equipo con recomendaciones`, `Análisis específico de un jugador` to the rest of the system?**
  _19 weakly-connected nodes found - possible documentation gaps or missing edges._