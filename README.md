# 🔍 JobFinder API

A FastAPI application that helps users discover job listings tailored to their preferences. It integrates live job scraping from Rozee.pk and mock data, with optional intelligent filtering using OpenAI's GPT model.

---

## 🚀 Features

- 🔧 Input Customization: Search by position, experience, salary, job nature, location, and skills.
- 🧠 AI Relevance Filtering: Uses OpenAI GPT to determine relevance of job listings (optional).
- 🌐 Live Scraping: Retrieves job postings from Rozee.pk.
- 📄 Mock Listings: Simulated LinkedIn data for demo/interview purposes.
- 📤 Unified API Endpoint: Returns job listings from both sources.

---

## 📦 Requirements

- Python 3.7+
- FastAPI
- Uvicorn
- Requests
- BeautifulSoup4
- OpenAI (optional)

Install dependencies:
```bash
pip install fastapi uvicorn requests beautifulsoup4 openai
## 🛠️ File Structure
- bash
- Copy
- Edit
.
├── main.py       # FastAPI app
├── README.md     # Project documentation
## 🧪 How It Works
- Input (JobRequest)
- json
- Copy
- Edit
{
  "position": "Software Engineer",
  "experience": "2 years",
  "salary": "100,000 PKR",
  "jobNature": "onsite",
  "location": "Karachi",
  "skills": "Python, React"
}
Output (JobResponse)
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
    }
  ]
}
## 🔓 Optional: OpenAI Filtering
- To enable GPT-based job filtering:

- Uncomment the openai.api_key line in main.py

Set your API key:

- python
- Copy
- Edit
- openai.api_key = "your-key-here"
- If left disabled, a mock relevance check always returns True.

## 🧪 Run the API
Start the FastAPI server using:

- bash
- Copy
- Edit
- uvicorn main:app --reload
- Then open:

- arduino
- Copy
- Edit
- http://127.0.0.1:8000/docs
- Use the Swagger UI to test /find-jobs.

## ✅ Sample Request
- json
- Copy
- Edit
{
  "position": "Backend Developer",
  "experience": "3 years",
  "salary": "120,000 PKR",
  "jobNature": "remote",
  "location": "Lahore",
  "skills": "Django, PostgreSQL"
}
## 📌 Notes
- Rozee.pk scraping is limited to 5 listings for demonstration.

- LinkedIn listings are mock data.

- This is built for educational/demo purposes.

## 🧠 Credits
Built with ❤️ using:

- FastAPI

- OpenAI

- BeautifulSoup
