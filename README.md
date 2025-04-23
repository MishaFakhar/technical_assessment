🔍 JobFinder API
A FastAPI application that helps users discover job listings tailored to their preferences by integrating mock data and live job scraping (Rozee.pk), with optional intelligent filtering via OpenAI's GPT model.

🚀 Features
🔧 Input Customization: Search based on position, experience, salary, job nature, location, and skills.

🧠 AI Relevance Filtering: Uses OpenAI's GPT (if enabled) to determine job match relevance.

🌐 Live Scraping: Fetches jobs from Rozee.pk using BeautifulSoup.

📄 Mock Listings: Simulated job data from LinkedIn for demo and interview purposes.

📤 Unified API Endpoint: Returns job listings from both sources in a consistent format.

📦 Requirements
Python 3.7+

FastAPI

Uvicorn

Requests

BeautifulSoup4

OpenAI (optional for relevance filtering)

Install dependencies:

bash
Copy
Edit
pip install fastapi uvicorn requests beautifulsoup4 openai
🛠️ File Structure
graphql
Copy
Edit
.
├── main.py          # FastAPI app with scraping, AI filtering, and mock data
├── README.md        # Project documentation
🧪 How It Works
Input Schema (JobRequest)
json
Copy
Edit
{
  "position": "Software Engineer",
  "experience": "2 years",
  "salary": "100,000 PKR",
  "jobNature": "onsite",
  "location": "Karachi",
  "skills": "Python, React"
}
Output Schema (JobResponse)
Returns a list of JobListing:

json
Copy
Edit
{
  "relevant_jobs": [
    {
      "job_title": "React Developer",
      "company": "LinkedIn Partner",
      "experience": "2 years",
      "jobNature": "onsite",
      "location": "Lahore, Pakistan",
      "salary": "95,000 PKR",
      "apply_link": "https://linkedin.com/job456",
      "source": "LinkedIn"
    },
    ...
  ]
}
🔓 Optional: OpenAI Filtering
To enable GPT-based job filtering:

Uncomment the openai.api_key line in main.py.

Set your OpenAI key:

python
Copy
Edit
openai.api_key = "your-key-here"
If disabled or commented, the is_relevant function defaults to a mock version that always returns True.

🧪 Run the API
Start the FastAPI server with Uvicorn:

bash
Copy
Edit
uvicorn main:app --reload
Open your browser and go to:

arduino
Copy
Edit
http://127.0.0.1:8000/docs
Use the Swagger UI to test the /find-jobs POST endpoint.

✅ Example
Try the following in Swagger UI:

json
Copy
Edit
{
  "position": "Backend Developer",
  "experience": "3 years",
  "salary": "120,000 PKR",
  "jobNature": "remote",
  "location": "Lahore",
  "skills": "Django, PostgreSQL"
}
📌 Notes
Scraping from Rozee.pk is basic and limited to 5 jobs for demonstration.

LinkedIn jobs are mocked, not real-time scraped.

This project is structured for interview/demo purposes.

🧠 Credits
Built with ❤️ using:

FastAPI

OpenAI

BeautifulSoup

