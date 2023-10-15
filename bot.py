from telegram.ext import Application, CommandHandler, MessageHandler, filters

import os
import logger
import asyncio

from dotenv import load_dotenv

from soundPlayer import playCustomSound

from threading import Thread

from face_detect import initThreads, playCustomSoundMutex, sendIntruderAlertMutex

load_dotenv()

TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


async def startMonitoring(update, context):
    await context.bot.send_message(chat_id=CHAT_ID, text="Monitoring started!")
    sendIntruderAlertMutex.acquire()
    await context.bot.send_message(chat_id=CHAT_ID, text="Intruder Alert!")
    await context.bot.send_photo(chat_id=CHAT_ID, photo=open(
        'images/image.jpg', 'rb'))


async def image(update, context):
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(
        'images/image.jpg', 'rb'))


async def voice(update, context):
    fullMessage = update.message.text
    playCustomSoundMutex.acquire()
    playCustomSound(fullMessage)
    playCustomSoundMutex.release()
    await update.message.reply_text(fullMessage)


def main():

    app = Application.builder().token(TOKEN).build()

    initThreads()

    app.add_handler(CommandHandler("image", image))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, voice))
    app.add_handler(CommandHandler("start", startMonitoring))

    app.run_polling()


if __name__ == '__main__':
    main()
