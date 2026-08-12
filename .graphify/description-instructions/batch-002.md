# Node Description Batch 3 of 3

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

- "backend_fantasy_client_rationale_39": "Autenticación en LaLiga Fantasy" | kind=entity | source=backend/fantasy_client.py:L39 | neighbors=[.login()]
- "backend_fantasy_client_rationale_77": "Obtiene los datos del equipo del usuario" | kind=entity | source=backend/fantasy_client.py:L77 | neighbors=[.get_my_team()]
- "backend_main_health": "health()" | kind=code-symbol | source=backend/main.py:L78 | neighbors=[main.py]
- "backend_main_rationale_183": "Ejecuta una acción de mercado (comprar/vender)" | kind=entity | source=backend/main.py:L183 | neighbors=[market_action()]
- "backend_main_root": "root()" | kind=code-symbol | source=backend/main.py:L73 | neighbors=[main.py]
- "backend_main_serve_frontend": "serve_frontend()" | kind=code-symbol | source=backend/main.py:L221 | neighbors=[main.py]
- "frontend_app_alerticon": "alertIcon()" | kind=code-symbol | source=frontend/app.js:L43 | neighbors=[app.js]
- "frontend_app_poslabel": "posLabel()" | kind=code-symbol | source=frontend/app.js:L31 | neighbors=[app.js]
- "frontend_app_urgencybadge": "urgencyBadge()" | kind=code-symbol | source=frontend/app.js:L37 | neighbors=[app.js]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: c:\Users\khonorat\OneDrive - NTT DATA EMEAL\Escritorio\App Fantasy\.graphify\description-instructions\batch-002.json

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
