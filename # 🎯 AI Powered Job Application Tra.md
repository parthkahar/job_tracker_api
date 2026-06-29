# 🎯 AI Powered Job Application Tracker

## 📖 Overview

AI Powered Job Application Tracker helps job seekers manage and track their job applications in one place.

Users can:

- Track applications across multiple companies
- Monitor application status (Applied, Interview, Offer, Rejected)
- Upload resumes for analysis
- Compare resumes against job descriptions
- Generate AI-powered cover letters
- Generate professional follow-up messages
- Maintain an organized job search workflow

---

## ✨ Features

### 📋 Application Management

- Add new job applications
- View all applications
- Update application status
- Delete applications
- Track company, role, and application progress

### 🤖 AI-Powered Tools

#### JD Analyzer

Upload your resume and paste a job description to:

- Identify matching skills
- Identify missing skills
- Calculate a fit score out of 10

#### Cover Letter Generator

Generate a professional cover letter based on:

- Uploaded resume
- Job description

#### Follow-up Generator

Generate professional follow-up messages for:

- Applied jobs
- Interviews
- Offers
- Recruiter communication

### 📄 Resume Processing

- Upload PDF resumes
- Extract text using PyMuPDF
- Use resume content automatically in AI tools

---

## 🛠 Tech Stack

### Backend

- Python
- FastAPI
- MySQL

### Frontend

- Streamlit

### AI

- Ollama
- Llama 3.2

### PDF Processing

- PyMuPDF (fitz)

---

## 🚀 How to Run Locally

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd ai-job-tracker
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start FastAPI Server

```bash
uvicorn main:app --reload
```

### 4. Start Streamlit Application

```bash
streamlit run app.py
```

---

## 📂 Project Structure

project/
│
├── app.py          # Streamlit frontend
├── main.py         # FastAPI backend
├── db.py           # Database connection
├── ai.py           # AI/LLM functions
├── .env            # Environment variables
└── README.md

---

## 📊 Application Status Types

- 🟢 Applied
- 🟡 Interview
- 🔵 Offer
- 🔴 Rejected

---

## 🎯 Future Improvements

- Dashboard analytics
- Search and filters
- Application insights
- Resume scoring
- Interview preparation assistant
- AI career recommendations
- Email integration
- Multi-user authentication

---

## 🙌 Built With

- FastAPI
- Streamlit
- MySQL
- Ollama
- Llama 3.2
- PyMuPDF
