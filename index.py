from typing import Final
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
import requests


TOKEN: Final = "7571747047:AAGkREvCUkK_U2QMe_SKgkAAJBcidD7qqHk"
BOT_USERNAME: Final = "@parting_clouds_bot (https://t.me/parting_clouds_bot)"


# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "hi! Thanks for keeping yourself aware!\n enter your city: "
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("send your city name to get the weather update!")


def get_weather(city):
    api_key = "4c4f3b303b374761b30efcb990942734"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        temperature_in_celcius = temperature - 273.15
        return (
            f"weather in {city.capitalize()}: {description}, {temperature_in_celcius}°C"
        )
    else:
        return f"sorry, couldn't retrieve data for {city.capitalize()}"


# Responses
def handle_response(text: str) -> str:
    return f"received '{text}' - please wait while I fetch the weather"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = update.message.text
    response: str = get_weather(text)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"update {update} caused error {context.error}")


if __name__ == "__main__":
    print("starting bot")
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    # Errors
    app.add_error_handler(error)
    print("polling")
    app.run_polling(poll_interval=3)
