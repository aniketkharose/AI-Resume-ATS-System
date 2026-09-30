# 🤖 AI Resume ATS System

An AI-powered Resume Applicant Tracking System (ATS) that analyzes resumes against job descriptions and provides ATS compatibility scores, skill matching, feedback, missing skills, and actionable recommendations.

🔗 **Live Demo:**  
https://ai-resume-ats-system-aniket.streamlit.app

🔗 **Backend API / Swagger Docs:**  
https://ai-resume-ats-api-tp6x.onrender.com/docs

---

## 📌 Overview

The **AI Resume ATS System** helps job seekers understand how well their resume matches a target job description.

The system processes the uploaded resume, extracts relevant information and skills, analyzes the job description, performs skill matching, calculates an ATS compatibility score, and generates feedback and recommendations.

The project combines:

- Natural Language Processing
- Resume parsing
- Skill extraction
- Job Description parsing
- Hybrid skill matching
- Lightweight semantic similarity
- ATS scoring
- Feedback generation
- Recommendation generation
- Authentication
- Analysis history
- PDF report generation

---

## ✨ Features

### 📄 Resume Analysis

- Upload resume in PDF or DOCX format
- Extract resume text
- Detect resume sections
- Analyze resume structure
- Extract technical skills
- Process resume content using NLP

### 💼 Job Description Analysis

- Parse job descriptions
- Detect job description sections
- Extract required skills
- Extract preferred skills
- Classify skills based on importance
- Identify missing skills

### 🔍 Skill Matching

The system performs multiple levels of matching:

- Exact skill matching
- Alias/normalized matching
- Lightweight semantic-style similarity
- Related technical skill detection
- Required vs preferred skill classification

### 📊 ATS Scoring

The system calculates an overall ATS compatibility score based on multiple dimensions:

- Required Skills
- Preferred Skills
- Semantic Relevance
- Resume Structure
- Content Completeness

The final score helps users understand how closely their resume aligns with the target job description.

> **Note:** The scoring weights are project-specific engineering choices and are not an industry-standard ATS formula.

### 💡 Feedback Engine

The system generates structured feedback including:

- Resume strengths
- Missing skills
- Improvement areas
- ATS-related suggestions
- Content improvement suggestions

### 🚀 Recommendation Engine

Provides actionable recommendations based on:

- Missing required skills
- Missing preferred skills
- Related skills
- Resume structure
- Resume content
- Overall ATS alignment

The system does not recommend falsely adding skills or experience that the candidate does not have.

### 🔐 Authentication

User authentication is implemented using Supabase:

- Sign Up
- Login
- Logout
- Authenticated sessions
- User-specific analysis history

### 📚 Analysis History

Users can view their previous resume analyses including:

- Resume filename
- ATS score
- Keyword match
- Missing skills
- Detailed analysis

### 📑 PDF Report

The system can generate an ATS analysis report containing the analysis results and recommendations.

---

# 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │      Streamlit       │
                    │      Frontend        │
                    └──────────┬───────────┘
                               │
                               │ HTTP Request
                               ▼
                    ┌──────────────────────┐
                    │       FastAPI        │
                    │       Backend        │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
       Resume Parser       JD Parser       NLP Processor
              │                │                │
              ▼                ▼                ▼
       Skill Extraction   JD Skills       Resume Analysis
              │                │                │
              └────────────────┼────────────────┘
                               ▼
                    ┌──────────────────────┐
                    │   Hybrid Matcher     │
                    │                      │
                    │ Exact + Related +    │
                    │ Lightweight Semantic │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     ATS Scorer       │
                    └──────────┬───────────┘
                               │
                 ┌─────────────┴─────────────┐
                 ▼                           ▼
        Feedback Engine             Recommendation Engine
                 │                           │
                 └─────────────┬─────────────┘
                               ▼
                    ┌──────────────────────┐
                    │    Analysis Result   │
                    └──────────┬───────────┘
                               │
                ┌──────────────┴──────────────┐
                ▼                             ▼
          Supabase DB                   PDF Report