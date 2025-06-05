import os
import dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

# Load environment variables from .env file
dotenv.load_dotenv()

# Load the OpenAI API key from the environment
api_key = os.environ.get("OPENAI_API_KEY", "")

client = OpenAI(
    api_key = api_key,
)

def sendDummyRequest():
    return "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."

def generatePrompt(keyword: str) -> str:

    if not keyword:
        return ""
    

    outline = [
        "Introduction to the topic",
        "Key features and benefits",
        "How it compares to competitors",
        "User testimonials or reviews",
        "Conclusion and call to action"
    ]

    skeleton = "\n\n".join(outline)

    system_message = ChatCompletionSystemMessageParam(
        role="system",
        content=(
            "You are an assistant that writes concise, engaging blog posts. "
            "Each response should be about 300 words (give or take a couple words)."
        ),
    )

    user_message = ChatCompletionUserMessageParam(
        role="user",
        content=f"Write a ~300-word blog post about \"{keyword}\". "
                "Make it informative, clear, and suitable for a general audience."
                "Use the following outline as a skeleton for the blog post:\n\n"
                f"{skeleton}\n\n"
                "The blog post should contain 3 affliate links represented by placeholders: "
                "{{AFF_LINK_1}}, {{AFF_LINK_2}}, {{AFF_LINK_3}}. "
                "Do not remove or alter these placeholders. "
                "Keep them exactly as written."
                
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[system_message, user_message],
        temperature=0.8,
        max_tokens=600,
    )

    content = response.choices[0].message.content
    if content is None:
        raise ValueError("The generated blog content is empty. Please try again with a different keyword.")
    
    blog_content = content.strip()

    # Validate the length of the generated content
    if len(blog_content) < 300:
        raise ValueError("The generated blog content is too short. Please try again with a different keyword.")
    
    # Replace placeholders with dummy URLs
    blog_content = replace_placeholders(blog_content)

    print(f"Generated blog content for keyword '{keyword}':\n{blog_content}\n")
    
    # Return the generated blog content 
    return blog_content

def replace_placeholders(content: str) -> str:
    """
    Locate every {{AFF_LINK_n}} (n = 1..3) in the AI content
    and replace it with a dummy URL like https://example.com/affiliate<n>.
    """
    final = content
    for i in range(1,  4):  # Assuming 3 affiliate links
        placeholder = f"{{{{AFF_LINK_{i}}}}}"
        dummy_url = f"https://example.com/affiliate{i}"
        final = final.replace(placeholder, dummy_url)
    return final

def save_blog_as_html(keyword: str, blog_content: str, metrics: str, output_dir: str = ".") -> None:
    """
    Given a keyword and the blog content, generate a simple HTML file
    and save it to the specified output directory.
    """
    # Sanitize keyword for filename (replace spaces with underscores)
    safe_name = "_".join(keyword.lower().split())
    filename = f"articles/{safe_name}_blog_post.html"
    filepath = os.path.join(output_dir, filename)

    # Read the template HTML file
    template_path = os.path.join(output_dir, "templates/example_blog_post.html")
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template file not found: {template_path}")

    with open(template_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Prepare replacements
    # Escape HTML-sensitive characters in blog_content
    paragraphs = blog_content.split("\n\n")
    body_html = ""
    for para in paragraphs:
        escaped = (
            para.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
        )
        body_html += f"{escaped.strip()}\n\n"

    body_html = replace_placeholders(body_html)

    # Replace placeholders
    html_content = html_content.replace("**keyword", keyword)
    html_content = html_content.replace("**content", body_html)
    html_content = html_content.replace("**metrics", metrics)

    # Write to file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"Blog post saved to {filepath}")