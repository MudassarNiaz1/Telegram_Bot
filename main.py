import os
import re
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import google.generativeai as genai

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    "gemini-2.5-flash",
    system_instruction=(
        "Your name is Muddy. "
        "You are friendly and helpful. "
        "Never say you are an AI or a language model. "
        "If someone asks who you are, always reply: 'I am Muddy.'"
    )
)


# Gibberish detector function
def is_gibberish(text):
    cleaned = re.sub(r"[^a-zA-Z]", "", text).lower()
    if len(cleaned) < 3:
        return False

    # Too many consonants
    vowels = set("aeiou")
    consonant_ratio = sum(1 for c in cleaned if c not in vowels) / len(cleaned)
    if consonant_ratio > 0.7:
        return True

    # Repeating characters like "asfkjaskfjasfj"
    if re.search(r"(.)\1{2,}", cleaned):
        return True

    return False


# /start command
async def start(update, context):
    await update.message.reply_text("Hello! I am Muddy \nAsk me anything!")

# Main AI message handler
async def chat(update, context):
    user_message = update.message.text

    # Check if message is nonsense
    if is_gibberish(user_message):
        await update.message.reply_text("I do not understand what you wrote...")
        return

    try:
        response = model.generate_content(user_message)
        reply = response.text
    except Exception:
        reply = "Sorry, something went wrong. Try again."

    await update.message.reply_text(reply)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()





































































# from typing import Final 
# from telegram import Update
# from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# TOKEN = "8550247076:AAEr8C86aNqIj1-LfjN50lpbSHHDCjOTBFU"
# BOT_Username: Final = "@MuddyMuddybot" 

# #Commands
# async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text('Hello! Thanks for chatting with me! I am Muddy!')


# async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text('I am Muddy! Please type something so I can respond!')


# async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text('This is a custom command!')

# # Responses

# def handle_response(text:str) -> str:
#     processed: str = text.lower()


#     if 'hello' in processed:
#         return "Hey there!"
    
#     if 'how are you' in processed:
#         return "I am good!"
    
#     if 'i love python' in processed:
#         return "Remember to Subscribe!"
    
    
#     return 'I do not understand what you wrote...'



# async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     message_type: str = update.message.chat.type
#     text: str = update.message.text

#     print(f'User({update.message.chat.id}) in {message_type}: "{text}" ')

#     if message_type == 'group':
#         if BOT_Username in text:
#             new_text: str = text.replace(BOT_Username, '').strip()
#             response: str = handle_response(new_text)
        
#         else:
#             return
    
#     else:
#         response: str = handle_response(text)
    
#     print('Bot:', response)
#     await update.message.reply_text(response)


# async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     print(f'Update {update} caused error {context.error}')



# if __name__ == '__main__':
#     print('Starting bot...')
#     app = Application.builder().token(TOKEN).build()

#     #Command
#     app.add_handler(CommandHandler('start', start_command))
#     app.add_handler(CommandHandler('help', help_command))
#     app.add_handler(CommandHandler('custom', custom_command))


#     # Messages
#     app.add_handler(MessageHandler(filters.TEXT, handle_message))

#     #Errors
#     app.add_error_handler(error)

#     # Check every 3 second for new messages/Polls
#     print('Polling...')
#     app.run_polling(poll_interval=3) 