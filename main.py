import asyncio
from core.signal_manager import run_signal_loop
from telegram_bot.bot import start_telegram_bot

async def main():
    # تشغيل البوت والتحليل في نفس الوقت
    print("✅ بدء تشغيل المهام...")

    # تشغيل مهام في الخلفية
    bot_task = asyncio.create_task(start_telegram_bot())
    signal_task = asyncio.create_task(run_signal_loop())

    # متابعة المهام والتعامل مع الأخطاء
    tasks = [bot_task, signal_task]

    try:
        await asyncio.gather(*tasks)
    except Exception as e:
        print(f"❌ خطأ في إحدى المهام: {e}")
    finally:
        for task in tasks:
            if not task.cancelled():
                task.cancel()
        print("🛑 تم إيقاف جميع المهام")

if __name__ == "__main__":
    asyncio.run(main())
