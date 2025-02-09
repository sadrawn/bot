from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
import os
import requests

BOT_TOKEN = "7597194336:AAHXEpGWyFj2AFd7Kdl2y3ihZllpQ711DUg"
CHANNEL_ID = "sadrawN"

TITLE, VIDEO = range(2)  # States for the conversation

async def start(update: Update, context):
    await update.message.reply_text("Send me the **title** of the video you want to upload.")
    return TITLE

async def get_title(update: Update, context):
    context.user_data["title"] = update.message.text
    await update.message.reply_text(f"Title received: {context.user_data['title']}\nNow, send me the **video file**.")
    return VIDEO

async def get_video(update: Update, context):
    video_file = update.message.video or update.message.document  # Video can be sent as a file
    if not video_file:
        await update.message.reply_text("Please send a **valid video file**.")
        return VIDEO

    title = context.user_data["title"]

    # Download the video
    video_path = f"{title}.mp4"
    video_file_id = video_file.file_id
    new_file = await update.message.bot.get_file(video_file_id)
    await new_file.download_to_drive(video_path)

    # Generate an image (dummy placeholder)
    image_url = f"https://via.placeholder.com/1280x720.png?text={title.replace(' ', '+')}"
    image_path = f"{title}.jpg"
    image_response = requests.get(image_url)
    with open(image_path, "wb") as img_file:
        img_file.write(image_response.content)

    # Send video and image to the channel
    bot = context.bot
    await bot.send_photo(CHANNEL_ID, photo=open(image_path, "rb"), caption=f"📌 {title}")
    await bot.send_video(CHANNEL_ID, video=open(video_path, "rb"), caption=f"🎥 {title}")

    # Cleanup
    os.remove(video_path)
    os.remove(image_path)

    await update.message.reply_text("✅ Video and thumbnail uploaded successfully!")
    return ConversationHandler.END

async def cancel(update: Update, context):
    await update.message.reply_text("❌ Upload canceled.")
    return ConversationHandler.END

app = Application.builder().token(BOT_TOKEN).build()

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_title)],
        VIDEO: [MessageHandler(filters.VIDEO | filters.Document.VIDEO, get_video)]
    },
    fallbacks=[CommandHandler("cancel", cancel)]
)

app.add_handler(conv_handler)

print("Bot is running...")
app.run_polling()
