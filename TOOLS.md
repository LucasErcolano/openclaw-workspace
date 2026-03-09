# TOOLS.md - Infraestructura de Rook & Mailbot

Este archivo contiene el mapa exacto de tu entorno de ejecución. Utiliza estas rutas y alias cuando necesites ejecutar comandos de terminal, reiniciar servicios o diagnosticar problemas.

## 1. Rutas del Proyecto (Workspace)
- **Directorio Base:** `/home/ubuntu/.openclaw/workspace/inbound_repo/Email-Auto-Response/`
- **Archivo de Logs Principal:** `run.log` (Usa `tail -n 50 run.log` para revisiones rápidas).
- **Entorno Virtual (Python):** El proyecto utiliza un `venv` local. Si necesitas ejecutar un script de diagnóstico (como `reproduce_issue.py` o `verify_changes.py`) o reiniciar el bot manualmente, **siempre** utiliza el ejecutable de Python del entorno virtual: `venv/bin/python`.

## 2. Gestión de Servicios (Mailbot)
*(Nota para Rook: Verifica con comandos `ps aux | grep python` o revisa si se usa `pm2` / `systemd` para mantener el proceso vivo).*
- Si tienes que reiniciar el Mailbot tras un fallo, asegúrate de matar el proceso huérfano anterior antes de iniciar el nuevo para evitar duplicación de *locks* o conflictos de puertos IMAP.
- Revisa `app.log` y `error.txt` si `run.log` no proporciona suficiente información sobre un *crash* profundo (Stack Trace).

## 3. LLM Router Interno del Mailbot (Rate Limits sin FreeRide)
El Mailbot ahora gestiona la continuidad LLM con un router propio en `src/llm_router.py`.
- Estado del router: `.runtime/llm_router_state.json`
- Orden de failover: `LLM_PROVIDER_ORDER` en `.env`
- Cooldowns y circuit breaker: `LLM_COOLDOWN_*` y `LLM_CIRCUIT_BREAKER_*`
- Si ves 429 en `run.log`, revisa en estado qué provider/key entró en cooldown en lugar de reiniciar gateway.

## 4. Sistema de Locks
- Los locks de las empresas (Pares/Impares) determinan si se pueden generar nuevos borradores. 
- Si determinas mediante `HEARTBEAT.md` que un lock está colgado (deadlock), localiza el archivo o registro de ese lock en este directorio y elimínalo/modifícalo usando herramientas bash (`rm`, `sed`, etc.) para liberar la cola.
