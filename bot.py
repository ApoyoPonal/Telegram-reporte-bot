import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# =========================
# VARIABLES DE ENTORNO
# =========================
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID"))

# =========================
# COMANDO /start
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👮‍♂️ Bot de Reportes Anónimos\n\n"
        "Envía información sobre:\n"
        "- Personas sospechosas\n"
        "- Vehículos sospechosos\n"
        "- Situaciones irregulares\n\n"
        "✍️ Escribe el reporte en un solo mensaje.\n\n"
        "No se solicitan datos personales."
    )

# =========================
# MENSAJES DE TEXTO
# =========================
async def recibir_reporte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = update.message.text

    texto = (
        "🚨 REPORTE ANÓNIMO\n\n"
        f"{mensaje}"
    )

    await context.bot.send_message(
        chat_id=GROUP_ID,
        text=texto
    )

    await update.message.reply_text(
        "✅ Reporte recibido. Gracias por colaborar."
    )

# =========================
# FLASK KEEP ALIVE
# =========================
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot activo", 200

def run_flask():
    app.run(host="0.0.0.0", port=10000)

# =========================
# MAIN
# =========================
def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    print("🚀 BOT INICIANDO POLLING")

    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_reporte)
    )

    application.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    main()
