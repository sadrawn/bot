import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = "7597194336:AAHXEpGWyFj2AFd7Kdl2y3ihZllpQ711DUg"

# Create the bot application
app = Application.builder().token(BOT_TOKEN).build()

# Function for starting the command handler
async def start(update: Update, context):
    await update.message.reply_text("Hello! This is Sadraw_n's bot")

# Function for echoing back what you sent
async def echo(update: Update, context):
    await update.message.reply_text(update.message.text)

# Add command and message handler
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# Run the bot
logger.info("Bot is running...")
app.run_polling()
