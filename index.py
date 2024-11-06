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
    try:
        api_key = "4c4f3b303b374761b30efcb990942734"
        url = (
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        )
        response = requests.get(url)
        response.raise_for_status()
        if response.status_code == 200:
            data = response.json()
            description = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            temperature_in_celcius = round(temperature - 273.15, 1)
            emoji = get_weather_emoji(data)
            return f"weather in {city.capitalize()}: {description} {emoji}, {temperature_in_celcius}°C"
        else:
            return "Weather data unavailable for this city."
    except requests.exceptions.RequestException as error:
        return f"Error: {error}"


# Responses
def handle_response(text: str) -> str:
    return f"received '{text}' - please wait while I fetch the weather"


def get_weather_emoji(data):
    weather_id = data["weather"][0]["id"]
    if 200 <= weather_id <= 232:
        return "⚡"
    elif 300 <= weather_id <= 321:
        return "🌥️"
    elif 500 <= weather_id <= 531:
        return "⛈️"
    elif 600 <= weather_id <= 622:
        return "❄️"
    elif 701 <= weather_id <= 741:
        return "🌫️"
    elif weather_id == 762:
        return "🌋"
    elif weather_id == 771:
        return "💨"
    elif weather_id == 781:
        return "🌪️"
    elif weather_id == 800:
        return "☀️"
    elif 801 <= weather_id <= 804:
        return "😶‍🌫️"
    else:
        return ""


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = update.message.text
    response: str = get_weather(text)
    if response:
        await update.message.reply_text(response)
    else:
        await update.message.reply_text("sorry, couldnt fetch weather data")


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
