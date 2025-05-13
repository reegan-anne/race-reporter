from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from bs4 import BeautifulSoup
import requests
import os
# from dotenv import load_dotenv
from urllib.parse import quote_plus
from googleapiclient.discovery import build


# Load environment variables
# load_dotenv()

app = Flask(__name__)

# Configure Gemini
genai.configure(api_key=os.getenv('geminiapikey'))
model = genai.GenerativeModel('gemini-1.5-flash')

def get_google_search_results(query):
    # This is a simple implementation. In production, you should use the Google Custom Search API
    service = build("customsearch", "v1", developerKey=os.getenv('googleapikey'))
    res = service.cse().list(q=query, cx='b4d46548e27b646de').execute()
    return [item['link'] for item in res['items']]


def scrape_article(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text()
        
        # Clean up text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        print(f"Scraped {url}")
        return text[:5000]  # Limit text length
    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")
        return ""

def summarize_race_reports(articles, urls):
    prompt = """Please analyze these race reports and provide a comprehensive summary focusing on:
    1. Overall race organization and logistics
    2. Course difficulty and notable features
    3. Parking and number collection process
    4. Any common themes or issues mentioned by runners
    
    Focus only on factual information about the race itself. Do not mention that this information comes from individual runners.
    Present the information as established facts about the race.
    
    Here are the race reports to analyze:
    """
    
    for article in articles:
        prompt += f"\n\n{article}"

    response = model.generate_content(prompt)
    summary = response.text
    summary += f"\n\nThis summary is based on analysis of {len(articles)} race reports."
    
    # Add URLs as an appendix
    summary = f"""<div class="race-report">
{summary}
</div>
<div class="sources mt-8 pt-4 border-t border-gray-200">
<h3 class="text-lg font-semibold mb-2">Sources</h3>
<ul class="list-disc pl-5">"""
    
    for url in urls:
        # Extract domain name from URL
        domain = url.split('//')[-1].split('/')[0]
        summary += f"\n<li><a href='{url}' target='_blank' class='text-blue-600 hover:text-blue-800'>{domain}</a></li>"
    
    summary += "\n</ul>\n</div>"
    return summary

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    race_name = request.json.get('race_name')
    if not race_name:
        return jsonify({'error': 'Race name is required'}), 400
    
    # Get search results
    search_query = f"{race_name} race report blog"
    urls = get_google_search_results(search_query)
    
    # Scrape articles
    articles = []
    successful_urls = []
    for url in urls:
        content = scrape_article(url)
        if content:
            articles.append(content)
            successful_urls.append(url)
    
    if not articles:
        return jsonify({'error': 'No relevant race reports found'}), 404
    
    # Generate summary
    summary = summarize_race_reports(articles, successful_urls)
    
    return jsonify({'summary': summary})

if __name__ == '__main__':
    app.run(debug=True) 