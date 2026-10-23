# Tarea Elda: Mesa Financiera con OpenAI

Cambios: Claude → OpenAI Responses API; Iris consulta Alpha Vantage por MCP; Vera explica como profesora de finanzas para estudiantes de 12 años; cron de 5 minutos; fallos reales ya no se convierten silenciosamente en datos demo.

## Configuración personal pendiente
En Settings → Secrets and variables → Actions:
- OPENAI_API_KEY (API de OpenAI, distinta de la suscripción a ChatGPT)
- ALPHAVANTAGE_API_KEY
- TELEGRAM_BOT_TOKEN
- TELEGRAM_CHAT_ID

No escribir valores reales en el código, capturas, documentación ni chats.

## Prueba sin simulación
Actions → mesa-financiera → Run workflow → ticker AAPL → simulacion desmarcada.
El resultado real debe mencionar fuente «Alpha Vantage vía MCP» y al menos una herramienta utilizada. Después, envía /analiza MSFT en Telegram y captura el mensaje con la hora visible.

## Seguridad
- Mantener permisos de workflow de solo lectura.
- Autorizar únicamente el TELEGRAM_CHAT_ID asignado; no dejarlo vacío.
- Verificar ticker, registrar fallos sin revelar secretos y no inventar datos bursátiles.
- Limitar consumo de OpenAI y Alpha Vantage. Desactivar el cron al finalizar la actividad.
- Los mensajes son educativos y no son recomendaciones de inversión.

## Comprobaciones
Ejecuta el workflow pruebas; documenta el resultado verde, el before/after del prompt de Vera y la captura de Telegram. GitHub schedule puede ejecutarse con retraso respecto al cron de 5 minutos.
