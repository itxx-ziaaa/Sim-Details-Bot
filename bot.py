import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Your bot token from BotFather
TOKEN = "7882428971:AAF6C003YQR7VLkFcQRWLB7TPVU_9m7ZO1g"

# API Endpoint
API_URL = "https://tmphpscripts.xyz/Tajammal.php?num="

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Welcome! Send /sim <number> to get details.")

import json

async def sim_details(update: Update, context: CallbackContext) -> None:
    if not context.args:
        await update.message.reply_text("Usage: /sim <phone_number>")
        return

    number = context.args[0]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(API_URL + number, headers=headers)

    if response.status_code == 200:
        try:
            data = response.json()

            if isinstance(data, list):  # Ensure data is a list
                formatted_details = ""
                for entry in data:
                    formatted_details += (
                        f"📞 **Mobile #:** `{entry.get('Mobile #', 'N/A')}`\n"
                        f"👤 **Name:** `{entry.get('Name', 'N/A')}`\n"
                        f"🆔 **CNIC:** `{entry.get('CNIC', 'N/A')}`\n"
                        f"📍 **Address:** `{entry.get('Address', 'N/A') or 'N/A'}`\n"
                        f"📡 **Operator:** `{entry.get('Operator', 'N/A')}`\n"
                        f"———————————————\n"
                    )

                # Send formatted response
                await update.message.reply_text(formatted_details, parse_mode="Markdown")

            else:
                await update.message.reply_text("⚠️ Unexpected response format.")

        except json.JSONDecodeError:
            await update.message.reply_text("⚠️ Error: API did not return valid JSON.")

    else:
        await update.message.reply_text("❌ Failed to fetch details. Please try again.")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("sim", sim_details))

    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
