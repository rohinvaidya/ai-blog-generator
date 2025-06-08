from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from seo_fetcher import fetchMetrics
from ai_generator import generatePrompt, save_blog_as_html

def job():
    keyword = "software engineering"
    metrics = fetchMetrics(keyword)
    content = generatePrompt(keyword)
    print(f"Running scheduled job for keyword: {keyword}")
    
    if not metrics:
        print(f"No metrics found for keyword '{keyword}'. Skipping HTML generation.")
    else:
        save_blog_as_html(keyword, content, metrics)
        print(f"[{datetime.now()}] Generated scheduled post for “{keyword}")

def initialize_scheduler(interval) -> BackgroundScheduler:
    scheduler = BackgroundScheduler()
    
    # Run the feature specified in the --feature flag
    if interval.lower() == 'hourly':
        scheduler.add_job(job, 'interval', hours=1, start_date=datetime.now(), id='hourly_job', replace_existing=True)
    
    elif interval.lower() == 'daily':
        scheduler.add_job(job, 'interval', days=1, start_date=datetime.now(), id='daily_job', replace_existing=True)

    elif interval.lower() == 'weekly':
        scheduler.add_job(job, 'interval', weeks=1, start_date=datetime.now(), id='weekly_job', replace_existing=True)
    
    elif interval.lower() == 'none':
        print('No interval specified. The job will not run automatically.')
        return scheduler
    else:
        print('Unknown interval or you need to specify the scheduler interval with the --interval flag.')
        print('Example: --interval daily, --interval hourly, --interval weekly, --interval none')
        return scheduler

    scheduler.start()
    print(f"Scheduler will run the job {interval}.")
    
    return scheduler

def scheduler_status(scheduler) -> bool:
    """
    Returns the status of the scheduler.
    """
    if scheduler and scheduler.running:
        print("Scheduler is initialized and running.")
        return True
    else:
        print("No scheduler initialized.")
        return False

def shutdown_scheduler(scheduler) -> bool:
    """
    Shuts down the scheduler gracefully.
    """
    if scheduler:
        scheduler.shutdown(wait=False)
        print("Scheduler has been shut down.")
    else:
        print("No scheduler to shut down.")

    return scheduler.running