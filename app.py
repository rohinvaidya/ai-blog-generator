from flask import Flask, request, render_template, jsonify
from seo_fetcher import returnMetricsForKeyword

app = Flask(__name__)
app.app_context().push()

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
        # output = f"<h1>{keyword}</h1>" + jsonify(metrics).get_data(as_text=True)
        return render_template('blog_post.html', keyword=keyword, metrics=metrics)

if __name__ == '__main__':
    app.run(debug=True)