# Monitoreo Continuo del Mailbot y LLMs (Heartbeat)

Eres Rook. En cada ciclo de ejecución, realiza las siguientes comprobaciones sobre la infraestructura del Mailbot y tu propia configuración de LLMs. Si todos los sistemas están nominales, finaliza la tarea en silencio con `NO_REPLY`. Solo notifica o toma acción si detectas una anomalía.

## 1. Salud del Proceso Principal (Logs del Mailbot)
- Usa tus herramientas de terminal para inspeccionar los logs del sistema ejecutando:
  `tail -n 50 /home/ubuntu/.openclaw/workspace/inbound_repo/Email-Auto-Response/run.log`
- Busca específicamente:
  - Desconexiones o timeouts del protocolo IMAP.
  - Errores de API de Twilio (fallos al enviar desde `+18144859184` o `+447380843002`).
  - Errores de "Rate Limit", "429 Too Many Requests" o cuota excedida en la generación de borradores.

## 2. Detección y Liberación de Deadlocks
- Revisa el estado de los *locks* de concurrencia para ambas empresas.
- Si un *lock* está activo pero el `run.log` no muestra actividad reciente con el `REVIEWER_ID` (ni `LISTO`, `ELIMINAR`, `SPAM`, ni `GUARDAR`), asume que el flujo se trabó.
- **Acción:** Purga o libera ese *lock* específico usando tus herramientas y envíame una alerta informando del desbloqueo.

## 3. Procesamiento Background
- Verifica en el `run.log` o en los procesos del sistema que el subproceso de eliminación de SPAM siga corriendo y filtrando correos entrantes.

## 4. Gestión de Rate Limits de la LLM (Router Interno)
- Tu misión crítica es asegurar que tú (Rook) y el Mailbot nunca se queden sin cuota de API en OpenRouter.
- Verifica el estado del router leyendo `.runtime/llm_router_state.json` y que haya proveedores con éxitos recientes.
- **Verificación del Router:** confirma que `LLM_PROVIDER_ORDER` exista en `.env` y que haya al menos una key válida por proveedor disponible.
- **Rotación de Emergencia:** Si en el paso 1 detectaste errores de "Rate Limit" en el `run.log`, fuerza una rotación manual de modelos ejecutando:
  1. Confirma en estado que la key/provider afectada entró en cooldown.
  2. Verifica que el siguiente proveedor tome tráfico con éxito en logs.
  3. Si todos fallan, alerta con detalle de proveedor/modelo/error y propuesta de corrección.

## 5. Protocolo de Auto-Sanación (Modo Agente)
- Si detectas que el servicio del Mailbot está completamente caído o hay un error de código crítico (Stack Trace) en el `run.log`, entra en modo ingeniero: diagnostica el error, formula un parche, aplícalo y reinicia el servicio del Mailbot.
