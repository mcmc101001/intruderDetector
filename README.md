# Intruder alert telegram bot

This is a telegram bot that detects intruders in your house and sends you a notification with a picture of the intruder. It also allows you to send messages to the bot and broadcast it to the intruder. Tech used includes openCV, python-telegram-bot, Google's text to speech API and python threading.

## Getting Started

First, create a telegram bot using BotFather and get the API key. Use IDBot to find your telegram userID. Create a `.env` file in the root directory following the `.env.example` and replace the BOT_TOKEN with your API key and CHAT_ID with your telegram userID.

Next, activate a python virtual environment and install dependencies.

```bash
python -m venv env
env\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Usage

Run the bot using the following command:

```bash
python bot.py
```

Start the bot from telegram using the command `/start`. Afterwards, it will send you an image when it first detects an intruder. Thereafter, it will continue saving images of the intruder, while you can use the bot to send messages to the intruder. The bot will broadcast your messages to the intruder. You can also use the `/image` command on telegram to get the latest image of the intruder.

You would need to restart the script if you want to start a new session.
