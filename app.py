import argparse
from flask import Flask, request, render_template
from seo_fetcher import fetchMetrics
from ai_generator import generatePrompt, save_blog_as_html
from scheduler import initialize_scheduler, scheduler_status

app = Flask(__name__)
app.app_context().push()

# Use app.config to store the scheduler globally
app.config['job_scheduler'] = None

def parse_args():
    """
    Parses the command line arguments that were provided along
    with the python command. The --interval flag must be provided as
    that determines the scheduler interval.
    """
    ap = argparse.ArgumentParser("run.py")
    
    # Required parameter specifying for what interval the scheduler should run
    ap.add_argument('--interval', '-i', type=str, required=True,
                    help='The interval at which the job should run.'
                         'Example: --interval daily, --interval hourly, --interval weekly, --interval none')
    
    return ap.parse_args()


@app.route('/')
def index():
    keywords = [
        { "id" : 1, "name": "wireless earbuds" },
        { "id" : 2, "name": "best headphones" },
        { "id" : 3, "name": "smartphone accessories" }
        ] 
    return render_template('home.html', keywords=keywords)

@app.route('/generate', methods=['GET'])
def get_data():
    keyword = request.args.get('keyword', 'default_keyword')
    metrics = fetchMetrics(keyword)
    content = generatePrompt(keyword)

    if not keyword:
        return render_template('error.html', errorCode=400, errorMessage="Keyword is required")
    if not metrics:
        return render_template('error.html', errorCode=404, errorMessage="No metrics found for the keyword")
    if content == "":
        return render_template('error.html', errorCode=500, errorMessage="System Error: Content generation failed")
    else:
        save_blog_as_html(keyword, content, metrics)
        return render_template('blog_post.html', keyword=keyword, metrics=metrics, content=content)
    
@app.route('/scheduler', methods=['GET'])
def start_scheduler():
    interval = request.args.get('interval', 'none')
    scheduler = app.config.get('job_scheduler', None)

    if interval == 'Status':
        if scheduler_status(scheduler):
            return render_template('scheduler_status.html', statusMessage="Scheduler is running")
        else:
            return render_template('scheduler_status.html', statusMessage="Scheduler is not running")
    
    elif scheduler_status(scheduler):
        return render_template('scheduler_status.html', statusMessage="Scheduler is already running")
    
    else:
        scheduler = initialize_scheduler(interval)
        app.config.update(job_scheduler=scheduler)
        return render_template('scheduler_status.html', statusMessage="Scheduler started successfully with interval: " + interval)

if __name__ == '__main__':
    args = parse_args()
    interval = args.interval.lower()
    scheduler = initialize_scheduler(interval)
    app.config['job_scheduler'] = scheduler  # Store in app.config for global access
    
    if not scheduler_status(scheduler):
        print("Scheduler is not running.")
    
    app.run()