import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Telegram Bot Token
BOT_TOKEN = "7811952273:AAG_af2nxfYHlLgZfZL9N2NQ76Y-bRlvz64"

# PhishTank API (You need to register for a free API key)
PHISHTANK_API_URL = "https://safebrowsing.googleapis.com/v4/threatMatches:find?key="
PHISHTANK_API_KEY = "AIzaSyAHckpbisq5edT3OruPs2oLRDjn1mmjfCc"

async def start(update: Update, context: CallbackContext):
    """Send a welcome message when the user starts the bot."""
    await update.message.reply_text("Hello! Send me a link, and I'll check if it's a phishing site.")

async def check_link(update: Update, context: CallbackContext):
    """Check if the given link is a phishing site."""
    message_text = update.message.text

    if "http" in message_text or "www" in message_text:
        await update.message.reply_text("Checking link... Please wait.")

        # Send link to PhishTank API
        response = requests.post(PHISHTANK_API_URL, data={"format": "json", "url": message_text, "app_key": PHISHTANK_API_KEY})
        
        if response.status_code == 200:
            data = response.json()
            if data.get("results", {}).get("valid"):
                is_phishing = data["results"]["in_database"]
                if is_phishing:
                    await update.message.reply_text("⚠️ This link is flagged as **phishing**! Be careful.")
                else:
                    await update.message.reply_text("✅ This link seems **safe**.")
            else:
                await update.message.reply_text("⚠️ Couldn't verify this link. Use caution.")
        else:
            await update.message.reply_text("❌ Error checking the link. Try again later.")
    else:
        await update.message.reply_text("Please send a valid link.")

def main():
    """Main function to run the bot."""
    app = Application.builder().token(BOT_TOKEN).build()

    # Command handler
    app.add_handler(CommandHandler("start", start))
    
    # Message handler for links
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_link))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()