import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
from datetime import datetime

TOKEN = os.getenv("BOT_TOKEN")
EXCHANGERATE_API = "https://api.exchangerate-api.com/v4/latest/"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 សូមស្វាគមន៍មកកាន់ Forex Bot!\n\n"
        "ពាក្យបញ្ជាដែលមាន៖\n"
        "/usd_khmer - តម្លៃ USD to KHR\n"
        "/eur_usd - តម្លៃ EUR to USD\n"
        "/gbp_usd - តម្លៃ GBP to USD"
    )

def get_forex_rate(from_currency: str, to_currency: str):
    try:
        url = f"{EXCHANGERATE_API}{from_currency}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if to_currency in data['rates']:
                return data['rates'][to_currency]
        return None
    except Exception as e:
        logger.error(f"Error fetching rate: {e}")
        return None

async def usd_khmer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rate = get_forex_rate("USD", "KHR")
    if rate:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await update.message.reply_text(f"💵 USD to KHR\n\n1 USD = {rate:,.2f} KHR\n⏰ {timestamp}")
    else:
        await update.message.reply_text("❌ រកមិនឃើញទិន្នន័យទេ។")

async def eur_usd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rate = get_forex_rate("EUR", "USD")
    if rate:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await update.message.reply_text(f"💶 EUR to USD\n\n1 EUR = {rate:,.2f} USD\n⏰ {timestamp}")
    else:
        await update.message.reply_text("❌ រកមិនឃើញទិន្នន័យទេ។")

async def gbp_usd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rate = get_forex_rate("GBP", "USD")
    if rate:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await update.message.reply_text(f"💷 GBP to USD\n\n1 GBP = {rate:,.2f} USD\n⏰ {timestamp}")
    else:
        await update.message.reply_text("❌ រកមិនឃើញទិន្នន័យទេ។")

def main():
    if not TOKEN:
        print("❌ រកមិនឃើញ BOT_TOKEN ទេ!")
        return

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("usd_khmer", usd_khmer))
    app.add_handler(CommandHandler("eur_usd", eur_usd))
    app.add_handler(CommandHandler("gbp_usd", gbp_usd))

    print("🚀 Bot កំពុងដំណើរការ...")
    app.run_polling()

if __name__ == '__main__':
    main()
