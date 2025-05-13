# Marathon Race Report Analyzer

This Flask application uses Google's Gemini AI to analyze race reports for marathon events. It searches for blog posts about specific races and provides a summary of the race experience, difficulty level, and participant satisfaction.

## Features

- Search for race reports by marathon name
- AI-powered analysis of race reports
- Modern, responsive web interface
- Real-time analysis results

## Setup

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory with your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
   You can get a Gemini API key from: https://makersuite.google.com/app/apikey

4. Run the application:
   ```bash
   python app.py
   ```

5. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Enter the name of a marathon race in the search box
2. Click "Analyze Race Reports"
3. Wait for the analysis to complete
4. View the summarized results

## Notes

- The application uses web scraping to find race reports, which may be subject to rate limiting
- For production use, consider implementing proper rate limiting and error handling
- The analysis is based on publicly available race reports and may not be comprehensive

## Requirements

- Python 3.7+
- Flask
- Google Generative AI (Gemini)
- BeautifulSoup4
- Requests
- python-dotenv 