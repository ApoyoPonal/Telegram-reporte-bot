import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")

async def recibir_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = update.message.text
    usuario = update.message.from_user.id

    texto = (
        "📩 *Nuevo reporte anónimo*\n\n"
        f"📝 Mensaje:\n{mensaje}"
    )

    await context.bot.send_message(
        chat_id=GROUP_ID,
        text=texto,
        parse_mode="Markdown"
    )

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_mensaje))
    app.run_polling()
