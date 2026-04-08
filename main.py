from telegram.ext import ApplicationBuilder
from handlers import setup

TOKEN = "8752076853:AAHJ3LhQ707EnfXUWmUT5dKky8BQhxJM5Uk"   # 👈 यहाँ token डालना है

app = ApplicationBuilder().token(TOKEN).build()

setup(app)

app.run_polling()
