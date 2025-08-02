import asyncio
import threading
from flask import Flask
from core.signal_manager import run_signal_loop
from telegram_bot.bot import start_telegram_bot

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bot and Signal Manager are running on Railway!"

def run_async_tasks():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = [
        loop.create_task(start_telegram_bot()),
        loop.create_task(run_signal_loop())
    ]
    try:
        loop.run_until_complete(asyncio.gather(*tasks))
    except Exception as e:
        print(f"❌ خطأ في المهام: {e}")
    finally:
        loop.close()

if __name__ == "__main__":
    # تشغيل المهام غير المتزامنة في Thread منفصل
    threading.Thread(target=run_async_tasks, daemon=True).start()

    # تشغيل Flask (لـ Railway)
    app.run(host="0.0.0.0", port=5000)

