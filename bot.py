from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

async def reenviar_reporte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == "private":
        texto = update.message.text

        mensaje = (
            "🚨 REPORTE ANÓNIMO 🚨\n\n"
            f"{texto}"
        )

        await context.bot.send_message(
            chat_id=context.bot_data["GROUP_ID"],
            text=mensaje
        )

app = ApplicationBuilder().token(
    "TOKEN_AQUI"
).build()

app.bot_data["GROUP_ID"] = -1000000000000  # ID_AQUI

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reenviar_reporte))
app.run_polling()
