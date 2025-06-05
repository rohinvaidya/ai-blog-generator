from datetime import datetime
from flask import Flask, request, render_template, jsonify
from seo_fetcher import fetchMetrics
from ai_generator import generatePrompt, save_blog_as_html
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.app_context().push()

def job():
    keyword = "software engineering"
    metrics = fetchMetrics(keyword)
    content = generatePrompt(keyword)
    print(f"Running scheduled job for keyword: {keyword}")
    
    if not metrics:
        print(f"No metrics found for keyword '{keyword}'. Skipping HTML generation.")
    else:
        save_blog_as_html(keyword, content, metrics)

@app.route('/')
def index():
    keywords = [
        { "id" : 1, "name": "wireless earbuds" },
        { "id" : 2, "name": "best headphones" },
        { "id" : 3, "name": "smartphone accessories" }]
    
    return render_template('home.html', keywords = keywords)

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

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    try:
        scheduler.add_job(job, 'interval', days=1, start_date=datetime.now(), id='daily_job', replace_existing=True)
        print("Scheduler started. Job will run once a day.")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
    app.run(debug=True)   