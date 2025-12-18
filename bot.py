import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# ======================
# VARIABLES DE ENTORNO
# ======================
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID"))

# ======================
# BOT DE TELEGRAM
# ======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👮‍♂️ Bot de Reportes activo.\n\n"
        "✍️ Escribe tu reporte y será enviado de forma segura."
    )

async def recibir_reporte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    usuario = update.message.from_user

    mensaje = (
        "🚨 NUEVO REPORTE 🚨\n\n"
        f"👤 Usuario: {usuario.full_name}\n"
        f"🆔 ID: {usuario.id}\n\n"
        f"📝 Mensaje:\n{texto}"
    )

    await context.bot.send_message(chat_id=GROUP_ID, text=mensaje)
    await update.message.reply_text("✅ Reporte enviado correctamente.")

def iniciar_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_reporte))
    app.run_polling()

# ======================
# SERVIDOR FLASK (KEEP ALIVE)
# ======================
web = Flask(__name__)

@web.route("/")
def home():
    return "Bot de Telegram activo 🚔"

def iniciar_web():
    web.run(host="0.0.0.0", port=10000)

# ======================
# EJECUCIÓN
# ======================
if __name__ == "__main__":
    threading.Thread(target=iniciar_bot).start()
    iniciar_web()
