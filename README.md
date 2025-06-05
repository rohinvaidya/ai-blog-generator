# AI Blog Post Generator

A tool to generate blog posts using AI.

## Setup & Installation

1. **Clone the repository**
    ```bash
    git clone https://github.com/<your-username>/ai-blog-generator-interview-RohinVaidya.git
    cd ai-blog-post-generator
    ```

    **Note: Creation of a python virtual environment for this application is recommended.**

2. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure environment variables**

    Create a `.env` file and add your API keys or configuration as needed:
    ```
    OPENAI_API_KEY=<your_openai_api_key>
    ```

4. **Run the application**
    ```bash
    python app.py --interval daily
    ```

## Requirements

- Python 3.8+
- pip
- Modern Web Browser (Safari, Chrome, Firefox, etc)
- OpenAI Developer Account
- OpenAI API Key

## Usage

### 1. To generate a blog post, run the application and start the scheduler automatically, follow the instructions:

```bash
python app.py --interval daily
```
You can specify the following options to schedule the blog post draft for a pre-determined word.

```
Example: --interval daily, --interval hourly, --interval weekly, --interval none
```

You will be asked to enter a topic or keyword for your blog post. The AI will then generate and display the blog content based on your input.

**Example:**
```
Enter a keyword The future of AI in healthcare
```

The generated blog post will be shown in the web browser. A copy of the generated blog post will also be saved to the `/articles` directory.

### 2. A daily scheduler will run in the background and generate a blog post about a pre-defined keyword (for example, `software engineering`) and save it to the `/articles` directory.

### 3. Search Engine Optimization (SEO) metrics for the entered keyword will be available on the generated blog post page.