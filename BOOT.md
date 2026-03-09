# Rutina de Inicio: Supervisor de Mailbot



Ejecuta las siguientes comprobaciones de estado una sola vez, de manera silenciosa:



1. Verifica mediante la terminal si el proceso/servicio principal del mailbot está actualmente en ejecución.

2. Revisa el sistema de *locks* de ambas empresas. Si encuentras un *lock* activo pero el log no muestra actividad reciente (indicando un posible cuelgue previo), libéralo para evitar que el *pipeline* se frene.

3. Haz un chequeo rápido (ping o lectura de logs) para confirmar que las conexiones con las APIs de Twilio (+18144859184 y +447380843002) y los correos IMAP están respondiendo.

4. Si el servicio está caído o hay un error crítico de arranque que requiera mi intervención, envíame una alerta detallada NO AL REVISOR DE WHATSAPP SI NO AL CONFIGURADO EN TELEGRAM.

5. Si todos los sistemas están en orden, finaliza esta tarea y responde estrictamente con `NO_REPLY`.
