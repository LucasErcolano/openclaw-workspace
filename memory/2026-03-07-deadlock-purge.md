# Session: 2026-03-07 23:03:03 UTC

- **Session Key**: agent:main:main
- **Session ID**: baaaeaba-dfe3-420a-a0d1-b352fcabb2da
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

[Sat 2026-03-07 15:22 UTC] Dime todo lo que sabes de este proyecto
assistant: [[reply_to_current]] **Resumen completo del proyecto OpenClaw y su componente Mailbot**

**1. Visión general**  
OpenClaw es un marco abierto para crear y operar agentes de IA autónomos («agents») que pueden interactuar con múltiples canales (WhatsApp, Telegram, Discord, etc.) y con sistemas externos (API, CLI, bases de datos). Cada agente se ejecuta como una *session* y cuenta con su propia memoria, historial y capacidad de usar “skills” (herramientas) especializadas.

**2. El Mailbot**  
El Mailbot es un agente semi‑automatizado de respuestas a correos electrónicos que forma parte del ecosistema OpenClaw. Sus características principales son:

| Aspecto | Detalle |
|---------|---------|
| **Disparador** | Reacciona a correos no leídos en cuentas configuradas vía variables de entorno (`EMAIL_USER`, `EMAIL_USER_2`, `EMAIL_USER_3`). |
| **Ruteo** | - Empresas con **cuentas impares** usan `COMPANY_CONTEXT` y comunican vía Twilio usando `whatsapp:+18144859184`. <br> - Empresas con **cuentas pares** usan `COMPANY_CONTEXT_2` y comunican vía `whatsapp:+447380843002`. |
| **Flujo Human‑in‑the‑Loop** | 1. El sistema genera un borrador del respuesta. <br>2. Envía el contexto + borrador al revisor humano por WhatsApp (`REVIEWER_ID`). <br>3. El revisor responde con una de las 4 acciones definitivas: `LISTO`, `ELIMINAR`, `SPAM` o `GUARDAR`. <br>4. Cualquier otra respuesta se interpreta como feedback para re‑escribir el borrador. |
| **Locks (cerraduras)** | Un lock por empresa garantiza que solo se procese un correo a la vez. Si el revisor no responde o hay un fallo de red, el lock puede quedar “colgado”. El agente debe detectar y purgar estos deadlocks para evitar que la cola se detenga. |
| **Acciones automáticas** | La eliminación de correos marcados como SPAM se ejecuta en background y no depende del lock activo. |
| **Auto‑sanación** | Si una dependencia falla (p.ej., API de Twilio timeout, error de script), el agente puede entrar en modo *agent* para diagnosticar, parchear e intentar restaurar el servicio sin intervención humana. |
| **Persistencia** | Cada sesión arranca con memoria fresca. La memoria permanente se guarda en `MEMORY.md` (para contextos directos) y en archivos diarios bajo `memory/YYYY-MM-DD.md`. Estas memorias se consultan y actualizan en cada heartbeat. |

**3. Arquitectura clave**  

- **Gateway daemon** – Servicio que gestiona la entrada de correos y la distribución a los workers. Se controla con `openclaw gateway <start|stop|restart|status>`.  
- **Skills** – Paquetes de funcionalidades (p.ej., `weather`, `gemini`, `github`, `healthcheck`). Se instalan desde ClawHub y se encuentran bajo `~/.npm-global/lib/node_modules/openclaw/skills/`. Cada skill tiene su propio `SKILL.md` con instrucciones de uso.  
- **Heartbeat** – En cada ciclo se ejecuta `HEARTBEAT.md`, donde se revisan: <br> • Salud del proceso principal (logs, timeouts de Twilio). <br> • Estado de los locks y detección de deadlocks. <br> • Sub‑procesos de eliminación de SPAM. <br> Si todo está bien, el heartbeat responde silenciosamente; si detecta anomalías, notifica al supervisor.  
- **Variables de entorno** (ejemplo’en `.env`) <br> - `EMAIL_USER`, `EMAIL_USER_2`, `EMAIL_USER_3` – cuentas IMAP. <br> - `COMPANY_CONTEXT`, `COMPANY_CONTEXT_2` – configuraciones por empresa. <br> - `TWILIO_SENDER_NUMBER` – número de WhatsApp usado según la empresa. <br> - `REVIEWER_ID` – identificación del revisor humano en WhatsApp. |
| **Seguridad y privacidad** | - Los correos son confidenciales; nunca se comparten fuera del flujo. <br> - Sólo el Mailbot genera respuestas a clientes finales; el agente solo supervisa y entrega borradores. <br> - Las acciones externas (envío de mensajes, publicaciones) requieren siempre autorización explícita. |

**4. Flujo típico de procesamiento**  

1. **Revisión de nuevos correos** – El daemon IMAP detecta mensajes no leídos.  
2. **Clasificación** – Según el número de cuenta (impar/par) se asigna el contexto empresarial correspondiente.  
3. **Generación de borrador** – Un modelo de lenguaje (p.ej., `gemini` o `freeride`) elabora una respuesta provisional.  
4. **Envío al revisor** – El borrador + contexto se envían a `REVIEWER_ID` por WhatsApp.  
5. **Feedback** – El revisor responde con una acción definitiva.  
6. **Ejecución** – Dependiendo de la acción: <br> • `LISTO` → el borrador se envía al cliente. <br> • `ELIMINAR` → se marca y elimina. <br> • `SPAM` → se mueve a la carpeta de spam y se registra para análisis. <br> • `GUARDAR` → se archiva para referencia futura.  
7. **Actualización de estado** – El lock se libera y el siguiente correo en cola es procesado.  

**5. Operaciones de mantenimiento**  

- **Chequeos de salud (heartbeat)** – Rotan entre revisar procesos, locks, subprocesos de SPAM y otras métricas cada 30 min (o con cron para horarios específicos).  
- **Gestión de deadlocks** – Si un lock permanece activo sin feedback, el agente debe liberarlo manualmente y notificar al supervisor.  
- **Auto‑sanación** – Detectar errores de script o fallos de API y aplicar parches automáticos cuando sea seguro.  
- **Mantenimiento de memoria** – Periódicamente revisar `memory/*.md` y consolidar aprendizajes en `MEMORY.md`.  

**6. Herramientas y habilidades disponibles**  

- **CLI principal** – `openclaw` para gestión de servicios, logs y despliegues.  
- **Skills especializadas** – `gemini` (Q&A y generación), `healthcheck` (auditoría de seguridad), `weather` (clima), `gh-issues` (gestión de GitHub), `tmux` (control de sesiones), `freeride` (gestión de modelos gratuitos), entre otras.  
- **Persistencia de notas** – `TOOLS.md` para datos de entorno propios (nombres de cámaras, alias SSH, voces TTS preferidas, etc.).  

**7. Identidad del agente**  

- **Nombre:** Rook  
- **Arquetipo:** “House spirit in the machine” – espíritu pragmático y algo irónico.  
- **Vibe:** Concise + blunt; le gusta mantener procesos limpios y logs sin errores.  
- **Emoji:** ♜  

**8. Buenas prácticas para la interacción**  

- **Reactividad:** Responder solo cuando se le pide, usar reacciones (👍, ❤️, 🙌) cuando no se necesita un mensaje completo.  
- **Silencio proactivo:** Durante heartbeats, si no hay anomalías, responder `HEARTBEAT_OK` y quedarse en silencio.  
- **Seguridad:** Nunca exfiltrar datos, nunca ejecutar comandos destructivos sin confirmación, y siempre preguntar antes de enviar mensajes externos.  

**9. Resumen rápido para el usuario**  

> El proyecto OpenClaw es una plataforma modular para crear agentes de IA que gestionan interacciones multicanal. El Mailbot, dentro de este ecosistema, toma correos entrantes, genera borradores, los envía a revisores humanos vía WhatsApp y espera una de cuatro acciones definidas para concluir el proceso. Mantiene la cola de trabajo mediante locks, detecta y recupera deadlocks, y se auto‑repara ante fallos de infraestructura. Toda su configuración se controla vía CLI (`openclaw gateway …`) y archivos de entorno, y su memoria persiste en `MEMORY.md` para garantizar continuidad entre sesiones.

Con esto tienes una visión completa de la arquitectura, funcionalidades y mecanismos de gestión del Mailbot y del proyecto OpenClaw en su conjunto. ¡Cualquier detalle más específico o alguna operación concreta que quieras realizar (por ejemplo, reiniciar el gateway, consultar logs, o activar una skill), solo házmelo saber!
user: Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK.
Current time: Saturday, March 7th, 2026 — 6:39 PM (UTC)
user: Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK.
Current time: Saturday, March 7th, 2026 — 8:09 PM (UTC)
