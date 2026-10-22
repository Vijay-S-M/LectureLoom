# LectureLoom

> **Tamil Cross-Language Course Help Desk for Engineering Students**

## Problem

Many engineering students understand technical concepts better when they are explained in Tamil, but a large amount of high-quality and freely available engineering learning material is available in English. Students often struggle to search English lecture transcripts using Tamil questions and find the exact part of a lecture that answers their question. Different departments also need their own courses and learning materials to remain separated. LectureLoom solves this problem by allowing students to ask questions in Tamil or English and retrieving relevant information from English engineering lecture transcripts.

## Who it is for

- Engineering students who prefer learning technical concepts in Tamil.
- Faculty coordinators and peer-learning cells managing course materials for multiple engineering departments.

## Signature feature

LectureLoom uses multilingual embeddings to retrieve relevant English engineering lecture content for Tamil questions and provides the answer in Tamil with a source lecture and exact timestamp for **"Watch this part."**

## Hardest problem (my interview story)

The hardest part of LectureLoom is building reliable cross-language retrieval between Tamil student questions and English engineering lecture transcripts. The system must understand the meaning of a Tamil technical question, retrieve the correct English transcript section, and generate an answer that is supported by the retrieved content. I also need to make sure that the answer does not contain unsupported information, so the project includes source references, timestamps, and a fact-checking stage.

## Dataset

| Source | Link | Documents | Pages | Licence / terms |
|---|---|---:|---:|---|
| NPTEL | NPTEL official website | Initial prototype: 5–10 lectures | Initial prototype; target 3,000+ pages | Licence / usage terms will be verified for each selected course before use |

## 10 real questions


The initial evaluation questions will include Tamil, English, and mixed-language engineering questions such as:

1. டிரான்சிஸ்டர் எப்படி ஸ்விட்சாக வேலை செய்கிறது?
2. Normalization-ல் 3NF என்றால் என்ன?
3. What is the difference between TCP and UDP?
4. TCP ஏன் reliable protocol என்று அழைக்கப்படுகிறது?
5. Process மற்றும் Thread இடையே என்ன வித்தியாசம்?
6. What is a primary key in DBMS?
7. Deadlock என்றால் என்ன?
8. What is the purpose of normalization in a database?
9. 2NF மற்றும் 3NF இடையே என்ன வித்தியாசம்?
10. What is the difference between stack and queue?

## Run it

### Windows


python -m venv .venv
.venv\Scripts\activate
pip install -r requirements-dev.txt
copy .env.example .env
uvicorn app.main:app --reload


### Linux / macOS


python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
uvicorn app.main:app --reload


### Health Check

Open:

http://127.0.0.1:8000/health

Or use:

curl http://localhost:8000/health


Expected response:

{
    "status": "healthy"
}


### API Documentation

Once the server is running:


http://127.0.0.1:8000/docs

FastAPI automatically provides interactive Swagger API documentation.

## Project Architecture


Student
   │
   │ Tamil / English Question
   ↓
LectureLoom Web Interface
   │
   ↓
FastAPI Backend
   │
   ↓
Multilingual Embedding Model
   │
   ↓
Vector Search
   │
   ↓
English NPTEL Transcript Chunks
   │
   ↓
Relevant Context
   │
   ↓
LLM Answer Generation
   │
   ↓
Fact Checking
   │
   ↓
Tamil Answer
   │
   ├── Source Lecture
   ├── Timestamp
   └── Watch This Part


## Research Objective

The main research objective is to compare the retrieval performance of Tamil questions with equivalent English questions.

The target is:

text
Tamil-question retrieval hit rate
should be within 5 percentage points
of the English-question retrieval hit rate
on 100 paired questions.


## Live link

Added in Week 2.
