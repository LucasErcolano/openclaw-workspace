# Session: 2026-03-08 01:29:22 UTC

- **Session Key**: agent:main:main
- **Session ID**: 9ff3d16c-dad1-4b57-a39f-0837fc028b4a
- **Source**: gateway:sessions.reset

## Conversation Summary

user: Sender (untrusted metadata):
```json
{
  "label": "openclaw-tui (gateway-client)",
  "id": "gateway-client",
  "name": "openclaw-tui",
  "username": "openclaw-tui"
}
```

[Sun 2026-03-08 00:43 UTC] Dime todo lo que sabes del proyecto
assistant: [[reply_to_current]] Te lo doy directo y sin humo:

- **Es un Mailbot semiautomatizado** para responder emails con **human-in-the-loop**.
- **Stack principal:** Python + IMAP/SMTP + Twilio WhatsApp + Flask webhook + LLM (Gemini/Rook/OpenClaw).
- **Repo principal:** `inbound_repo/Email-Auto-Response`.

### Qué hace exactamente
- Lee correos no leídos de múltiples cuentas (`EMAIL_USER`, `EMAIL_USER_2...`).
- Genera borrador con LLM según contexto de empresa.
- Envía borrador + contexto al revisor por WhatsApp.
- El revisor decide con comandos finales:
  - `LISTO` (envía)
  - `ELIMINAR`
  - `SPAM`
  - `GUARDAR`
- Si el revisor manda texto libre, lo toma como feedback y reescribe.

### Arquitectura clave
- `src/main.py`: loop principal, polling IMAP, locks, workflow.
- `src/llm_service.py`: generación de borradores, spam-check, fallback de providers.
- `src/email_service.py`: lectura IMAP, envío SMTP, guardado de borradores.
- `src/whatsapp_sender.py`: envío por Twilio, chunking de mensajes.
- `src/webhook_server.py`: recibe respuestas WhatsApp (`/whatsapp`, `/h5k5`, `/alfa`).
- `src/runtime_state.py`: persistencia de pendientes en `.runtime/workflow_state.json`.

### Locks y concurrencia
- Lock por cuenta/revisor/línea Twilio (cola por key de revisión).
- Solo un workflow activo por lock.
- Limpia pendientes vencidos con TTL (`PENDING_TTL_SECONDS`).
- Tiene circuit breaker y backoff para fallos IMAP.

### LLM
- **Track 1:** Gemini primary.
- **Track 2:** Rook/OpenClaw primary + Gemini fallback.
- Soporta retries, cooldown de keys, fallback de modelos, y salida JSON estricta.

### Estado real actual (ahora)
- **Gateway OpenClaw:** OK.
- **Watchdog del Mailbot:** está corriendo.
- **Problema crítico detectado:** el runner está en **crash-loop** con  
  `ModuleNotFoundError: No module named 'dotenv'`  
  (watchdog levanta `python3 src/main.py` con Python del sistema, no el venv).
- `.runtime/workflow_state.json`: sin pendientes (sin locks colgados ahora).
- `run.log` está vacío; la actividad útil está en `app.log`.

### Calidad / pruebas
- Hay estructura de pytest para unit/integration/e2e/load, pero **cobertura real baja** (vi muy pocos tests efectivos).
- Hay scripts de evaluación semántica con Himalaya/IMAP y reportes en `reports/`.
- Hallazgos repetidos en reportes: inconsistencias de firma/marketing no solicitado y bajo match de adjuntos (aunque ya metieron mejoras de fuzzy matching).

### Estado de git
- Rama `main` local está **ahead 4 commits** de `origin/main`.
- Working tree con cambios sin commitear (incluye `src/main.py`, `src/llm_service.py`, `src/whatsapp_sender.py`, etc.).

Si querés, siguiente paso te lo hago yo: **te dejo el Mailbot estable en 10 min** (fix de runner a venv + restart + smoke test IMAP/Twilio + verificación de locks).
user: Sender (untrusted metadata):
```json
{
  "label": "openclaw-tui (gateway-client)",
  "id": "gateway-client",
  "name": "openclaw-tui",
  "username": "openclaw-tui"
}
```

[Sun 2026-03-08 00:47 UTC] Dale
user: Sender (untrusted metadata):
```json
{
  "label": "openclaw-tui (gateway-client)",
  "id": "gateway-client",
  "name": "openclaw-tui",
  "username": "openclaw-tui"
}
```

[Sun 2026-03-08 00:47 UTC] Dale
user: Sender (untrusted metadata):
```json
{
  "label": "openclaw-tui (gateway-client)",
  "id": "gateway-client",
  "name": "openclaw-tui",
  "username": "openclaw-tui"
}
```

[Sun 2026-03-08 01:22 UTC] Como termino?
assistant: Current thinking level: xhigh.
Options: off, minimal, low, medium, high, xhigh, adaptive.
assistant: Thinking level set to adaptive.
