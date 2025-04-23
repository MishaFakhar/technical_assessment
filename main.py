# main.py

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import requests
from bs4 import BeautifulSoup
import openai

# Create FastAPI app
app = FastAPI()

# Set your OpenAI API key here
#openai.api_key = "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"  # Replace with your actual OpenAI key

# ------------- INPUT/OUTPUT SCHEMAS -------------

class JobRequest(BaseModel):
    position: str
    experience: str
    salary: str
    jobNature: str
    location: str
    skills: str

class JobListing(BaseModel):
    job_title: str
    company: str
    experience: str
    jobNature: str
    location: str
    salary: str
    apply_link: str
    source: str  # New field added

class JobResponse(BaseModel):
    relevant_jobs: List[JobListing]

# ------------- RELEVANCE FILTERING USING OPENAI -------------

def is_relevant(job_desc: str, user_input: JobRequest) -> bool:
    prompt = f"""
    User is looking for a job with the following criteria:
    Position: {user_input.position}
    Experience: {user_input.experience}
    Salary: {user_input.salary}
    Job Nature: {user_input.jobNature}
    Location: {user_input.location}
    Skills: {user_input.skills}

    Does this job match?
    Job Description: {job_desc}

    Respond with "Yes" or "No".
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a job filter assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        reply = response["choices"][0]["message"]["content"].strip().lower()
        return "yes" in reply
    except Exception as e:
        print(f"OpenAI error: {e}")
        return False

# ------------- MOCK LINKEDIN JOBS (Simulated for interview) -------------

def mock_linkedin_jobs(user_input: JobRequest) -> List[JobListing]:
    mock_jobs = [
        {
            "job_title": "Full Stack Engineer - LinkedIn",
            "company": "LinkedIn Corporation",
            "experience": "2+ years",
            "jobNature": "onsite",
            "location": "Karachi, Pakistan",
            "salary": "115,000 PKR",
            "apply_link": "https://linkedin.com/job789",
            "source": "LinkedIn"
        },
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
    
    results = []
    for job in mock_jobs:
        job_desc = f"{job['job_title']} at {job['company']} requires {job['experience']} experience."
        if is_relevant(job_desc, user_input):
            results.append(JobListing(**job))
    return results

# ------------- SCRAPER FOR ROZEE.PK -------------

def scrape_rozee_jobs(user_input: JobRequest) -> List[JobListing]:
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    search_url = f"https://www.rozee.pk/job/jsearch/q/{user_input.position.replace(' ', '%20')}/l/{user_input.location.replace(' ', '%20')}"

    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        jobs = []
        job_cards = soup.select("div.job")

        for card in job_cards[:5]:  # limit to 5 for demo
            title_tag = card.find("h3")
            company_tag = card.find("span", class_="company-name")
            link_tag = card.find("a", href=True)

            if not (title_tag and company_tag and link_tag):
                continue

            job_title = title_tag.text.strip()
            company = company_tag.text.strip()
            apply_link = "https://www.rozee.pk" + link_tag["href"]
            description = card.text.strip()

            if is_relevant(description, user_input):
                jobs.append(JobListing(
                    job_title=job_title,
                    company=company,
                    experience=user_input.experience,
                    jobNature=user_input.jobNature,
                    location=user_input.location,
                    salary=user_input.salary,
                    apply_link=apply_link,
                    source="Rozee.pk"
                ))

        return jobs

    except Exception as e:
        print(f"Error scraping Rozee: {e}")
        return []

# ------------- MAIN ENDPOINT -------------

@app.post("/find-jobs", response_model=JobResponse)
def find_jobs(user_input: JobRequest):
    linkedin_jobs = mock_linkedin_jobs(user_input)
    rozee_jobs = scrape_rozee_jobs(user_input)

    all_jobs = linkedin_jobs + rozee_jobs
    return {"relevant_jobs": all_jobs}




# # MOCK JOB LISTS ----------------------------------------------------------

# from fastapi import FastAPI
# from pydantic import BaseModel
# from typing import List
# import requests
# from bs4 import BeautifulSoup
# # import openai  # Commented out since we're mocking

# # Create FastAPI app
# app = FastAPI()

# # Set your OpenAI API key here (NOT used now)
# # openai.api_key = "your-api-key"

# # ------------- INPUT/OUTPUT SCHEMAS -------------

# class JobRequest(BaseModel):
#     position: str
#     experience: str
#     salary: str
#     jobNature: str
#     location: str
#     skills: str

# class JobListing(BaseModel):
#     job_title: str
#     company: str
#     experience: str
#     jobNature: str
#     location: str
#     salary: str
#     apply_link: str
#     source: str

# class JobResponse(BaseModel):
#     relevant_jobs: List[JobListing]

# # ------------- MOCKED RELEVANCE CHECK -------------

# def is_relevant(job_desc: str, user_input: JobRequest) -> bool:
#     # MOCKED for interview: Assume all jobs are relevant
#     print("Mock relevance check (always returns True).")
#     return True

# # ------------- MOCK LINKEDIN JOBS -------------

# def mock_linkedin_jobs(user_input: JobRequest) -> List[JobListing]:
#     mock_jobs = [
#         {
#             "job_title": "Full Stack Engineer - LinkedIn",
#             "company": "LinkedIn Corporation",
#             "experience": "2+ years",
#             "jobNature": "onsite",
#             "location": "Karachi, Pakistan",
#             "salary": "115,000 PKR",
#             "apply_link": "https://linkedin.com/job789",
#             "source": "LinkedIn"
#         },
#         {
#             "job_title": "React Developer",
#             "company": "LinkedIn Partner",
#             "experience": "2 years",
#             "jobNature": "onsite",
#             "location": "Lahore, Pakistan",
#             "salary": "95,000 PKR",
#             "apply_link": "https://linkedin.com/job456",
#             "source": "LinkedIn"
#         }
#     ]

#     results = []
#     for job in mock_jobs:
#         job_desc = f"{job['job_title']} at {job['company']} requires {job['experience']} experience."
#         if is_relevant(job_desc, user_input):
#             results.append(JobListing(**job))
#     return results

# # ------------- SCRAPER FOR ROZEE.PK -------------

# def scrape_rozee_jobs(user_input: JobRequest) -> List[JobListing]:
#     headers = {
#         "User-Agent": "Mozilla/5.0"
#     }
#     search_url = f"https://www.rozee.pk/job/jsearch/q/{user_input.position.replace(' ', '%20')}/l/{user_input.location.replace(' ', '%20')}"

#     try:
#         response = requests.get(search_url, headers=headers)
#         soup = BeautifulSoup(response.content, 'html.parser')
#         jobs = []
#         job_cards = soup.select("div.job")

#         for card in job_cards[:5]:
#             title_tag = card.find("h3")
#             company_tag = card.find("span", class_="company-name")
#             link_tag = card.find("a", href=True)

#             if not (title_tag and company_tag and link_tag):
#                 continue

#             job_title = title_tag.text.strip()
#             company = company_tag.text.strip()
#             apply_link = "https://www.rozee.pk" + link_tag["href"]
#             description = card.text.strip()

#             if is_relevant(description, user_input):
#                 jobs.append(JobListing(
#                     job_title=job_title,
#                     company=company,
#                     experience=user_input.experience,
#                     jobNature=user_input.jobNature,
#                     location=user_input.location,
#                     salary=user_input.salary,
#                     apply_link=apply_link,
#                     source="Rozee.pk"
#                 ))

#         return jobs

#     except Exception as e:
#         print(f"Error scraping Rozee: {e}")
#         return []

# # ------------- MAIN ENDPOINT -------------

# @app.post("/find-jobs", response_model=JobResponse)
# def find_jobs(user_input: JobRequest):
#     linkedin_jobs = mock_linkedin_jobs(user_input)
#     rozee_jobs = scrape_rozee_jobs(user_input)

#     all_jobs = linkedin_jobs + rozee_jobs
#     return {"relevant_jobs": all_jobs}

