import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from src.core.deck_builder_task import build_decks_job

scheduler = AsyncIOScheduler()

def start_scheduler():
    scheduler.add_job(
        build_decks_job,
        trigger=CronTrigger(hour=3, minute=0, timezone=pytz.timezone('Europe/Moscow')),
        id="build_decks",
        replace_existing=True
    )
    scheduler.start()

def stop_scheduler():
    scheduler.shutdown()
