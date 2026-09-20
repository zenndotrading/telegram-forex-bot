import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
from datetime import datetime

# ទាញយក Token ពី Environment Variable របស់ Railway យ៉ាងត្រឹមត្រូវ
TOKEN = os.getenv("BOT_TOKEN")

# API សម្រាប់ Forex
EXCHANGERATE_API = "https://api.exchangerate-api.com/v4/latest/"

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 សូមស្វាគមន៍មកកាន់ Forex Bot!\n\n"
        "ពាក្យបញ្ជាដែលមាន៖\n"
        "/usd_khmer - តម្លៃ USD to KHR\n"
        "/eur_usd - តម្លៃ EUR to USD\n"
        "/gbp_usd - តម្លៃ GBP to USD\n"
        "/help - ជំនួយលម្អិត"
    )

# /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 ជំនួយលម្អិត:\n\n"
        "ប្រើ /usd_khmer សម្រាប់តម្លៃ USD\n"
        "ប្រើ /eur_usd សម្រាប់តម្លៃ EUR\n"
        "ប្រើ /gbp_usd សម្រាប់តម្លៃ GBP\n\n"
        "ឧទាហរណ៍: /usd_khmer"
    )

# ទាញយកតម្លៃ Forex
def get_forex_rate(from_currency: str, to_currency: str):
    try:
        url = f"{EXCHANGERATE_API}{from_currency}"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if to_currency in data['rates']:
                rate = data['rates'][to_currency]
                return rate
        return None
    except Exception as e:
        logger.error(f"Error fetching rate: {e}")
        return None

# USD to KHR
async def usd_khmer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rate = get_forex_rate("USD", "KHR")
    
    if rate:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await update.message.reply_text(
            f"💵 USD to KHR\n\n"
            f"1 USD = {rate:,.2f} KHR\n"
            f"⏰ {timestamp}"
        )
    else:
        await update.message.reply_text("❌ មិនបានរកឃើញតម្លៃទេ។ សូមព្យាយាមម្តងទៀត។")

# EUR to USD
async def eur_usd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rate = get_forex_rate("EUR", "USD")
    
    if rate:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await update.message.reply_text(
            f"💶 EUR to USD\n\n"
            f"1 EUR = {rate:,.2f} USD\n"
            f"⏰ {timestamp}"
        )
    else:
        await update.message.reply_text("❌ មិនបានរកឃើញតម្លៃទេ។ សូមព្យាយាមម្តងទៀត។")

# GBP to USD
async def gbp_usd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rate = get_forex_rate("GBP", "USD")
    
    if rate:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await update.message.reply_text(
            f"💷 GBP to USD\n\n"
            f"1 GBP = {rate:,.2f} USD\n"
            f"⏰ {timestamp}"
        )
    else:
        await update.message.reply_text("❌ មិនបានរកឃើញតម្លៃទេ។ សូមព្យាយាមម្តងទៀត។")

# ដោះស្រាយ Message ផ្សេងទៀត
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.upper()
    
    if len(user_text) == 3 and user_text.isalpha():
        rate = get_forex_rate(user_text, "USD")
        if rate:
            await update.message.reply_text(
                f"💱 {user_text} to USD\n\n"
                f"1 {user_text} = {rate:,.4f} USD"
            )
        else:
            await update.message.reply_text(
                f"❌ មិនបានរកឃើញ '{user_text}'។\n"
                f"សូមប្រើ /usd_khmer, /eur_usd, /gbp_usd"
            )
    else:
        await update.message.reply_text(
            "ខ្ញុំមិនយល់ដឹង។ សូមប្រើពាក្យបញ្ជា:\n"
            "/usd_khmer\n/eur_usd\n/gbp_usd\n/help"
        )

# Error Handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.warning(f'Update "{update}" caused error "{context.error}"')

# Main
def main():
    """ចាប់ផ្តើម bot"""
    if not TOKEN:
        print("❌ រកមិនឃើញ BOT_TOKEN ទេ សូមពិនិត្យមើល Variables ក្នុង Railway ឡើងវិញ!")
        return

    app = Application.builder().token(TOKEN).build()

    # បន្ថែម Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("usd_khmer", usd_khmer))
    app.add_handler(CommandHandler("eur_usd", eur_usd))
    app.add_handler(CommandHandler("gbp_usd", gbp_usd))

    # បន្ថែម Message Handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Error handler
    app.add_error_handler(error)

    # ចាប់ផ្តើម bot
    print("🚀 Bot កំពុងដំណើរការ...")
    app.run_polling()

if __name__ == '__main__':
    main()
