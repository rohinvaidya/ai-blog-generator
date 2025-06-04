from flask import Flask, request, render_template, jsonify
from seo_fetcher import returnMetricsForKeyword
from ai_generator import sendDummyRequest  # Assuming this is your function to generate content
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

app = Flask(__name__)
app.app_context().push()

def job():
    keyword = "wireless earbuds"
    content = sendDummyRequest()  # Replace with actual function to generate content
    print(f"Generated content for '{keyword}': {content}")
    
    # Optionally, you can save the content to a local file
    with open(f"{keyword.replace(' ', '_')}_content.txt", "w") as f:
        f.write(content) 

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/generate', methods=['GET'])
def get_data():
    keyword = request.args.get('keyword', 'default_keyword')
    metrics = returnMetricsForKeyword(keyword)
    if not metrics:
        return jsonify({"error": "No metrics found for the keyword"}), 404
    else:
        return render_template('blog_post.html', keyword=keyword, metrics=metrics)

if __name__ == '__main__':
    try:
        scheduler = BackgroundScheduler()
        # scheduler.add_job(job, 'interval', days=1, start_date=datetime.now(), id='daily_job', replace_existing=True)
        scheduler.add_job(job, 'interval', seconds=5, start_date=datetime.now(), id='daily_job', replace_existing=True)
        print("Scheduler started. Job will run once a day.")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
    app.run(debug=True)
   