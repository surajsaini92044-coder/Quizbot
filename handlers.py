from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters
from pdf_parser import extract_quiz_from_pdf
import os
import asyncio

user_quiz = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📄 PDF upload karo (quiz format me)")

async def handle_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.document.get_file()
    
    file_path = f"{update.message.chat_id}.pdf"
    await file.download_to_drive(file_path)

    questions = extract_quiz_from_pdf(file_path)

    if not questions:
        await update.message.reply_text("❌ PDF me quiz nahi mila")
        return

    user_quiz[update.message.chat_id] = questions

    await update.message.reply_text(f"✅ {len(questions)} questions mil gaye! Quiz start ho raha hai...")

    await run_quiz(context, update.message.chat_id)

    os.remove(file_path)

async def run_quiz(context, chat_id):
    questions = user_quiz.get(chat_id, [])

    for q in questions:
        poll = await context.bot.send_poll(
            chat_id=chat_id,
            question=q["q"],
            options=q["o"],
            type="quiz",
            correct_option_id=q["a"],
            is_anonymous=False
        )

        await asyncio.sleep(10)
        await context.bot.stop_poll(chat_id, poll.message_id)

def setup(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.PDF, handle_pdf))
