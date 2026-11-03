# LectureLoom

> **Tamil Cross-Language Course Help Desk for Engineering Students**

## Problem

Many engineering students understand technical concepts better when they are explained in Tamil, but a large amount of high-quality and freely available engineering learning material is available in English. Students often struggle to search English lecture transcripts using Tamil questions and find the exact part of a lecture that answers their question. Different departments also need their own courses and learning materials to remain separated. LectureLoom solves this problem by allowing students to ask questions in Tamil, English, or Tanglish and retrieving relevant information from English engineering lecture transcripts.

## Who it is for

- **Engineering students** who prefer learning technical concepts in Tamil or mixed Tamil-English (Tanglish).
- **Faculty coordinators and peer-learning cells** managing course materials and doubt resolution for multiple engineering departments (CSE, ECE, EEE).

## Signature feature

LectureLoom uses multilingual embeddings to retrieve relevant English engineering lecture content for Tamil questions and provides the answer in Tamil with a source lecture and exact timestamp for **"Watch this part."**

## Hardest problem (my interview story)

The hardest part of LectureLoom is building reliable cross-language retrieval between Tamil student questions and English engineering lecture transcripts. The system must understand the meaning of a Tamil technical question, retrieve the correct English transcript section, and generate an answer that is supported by the retrieved content. I also need to make sure that the answer does not contain unsupported information, so the project includes source references, timestamps, and a fact-checking stage.

## Dataset

| Source | Link | Documents | Pages | Licence / terms |
|---|---|---:|---:|---|
| NPTEL (IIT Kharagpur / IIT Madras) | [https://nptel.ac.in/](https://nptel.ac.in/) | 5 core lecture documents | 54 pages (Week 1 prototype; target 3,000+ pages) | CC BY-NC-SA 4.0 / NPTEL open educational terms |

See [DATASET.md](DATASET.md) for full metadata, department breakdowns (CSE, ECE), and cryptographic hashes. Sample excerpts are committed under `data/sample/`.

## 10 real questions

See [docs/QUESTIONS.md](docs/QUESTIONS.md) for detailed document-page mapping and evaluation notes.

The evaluation questions include Tamil, Tanglish, and English queries representing actual student questions (with Question 10 serving as the unanswerable out-of-domain control):

1. **டிரான்சிஸ்டர் எப்படி ஸ்விட்சாக வேலை செய்கிறது?** — *Digital Electronics, pages 2–3 (Needs multi-page)*
2. **Normalization-ல் 3NF என்றால் என்ன?** — *DBMS, pages 4–5 (Needs multi-page)*
3. **What is the difference between TCP and UDP?** — *Computer Networks, pages 2–4 (Needs multi-page)*
4. **TCP ஏன் reliable protocol என்று அழைக்கப்படுகிறது?** — *Computer Networks, page 6*
5. **Process மற்றும் Thread இடையே என்ன வித்தியாசம்?** — *Operating Systems, pages 3–4 (Needs multi-page)*
6. **What is a primary key in DBMS?** — *DBMS, page 4*
7. **Deadlock என்றால் என்ன?** — *Operating Systems, page 7*
8. **What is the purpose of normalization in a database?** — *DBMS, page 2*
9. **2NF மற்றும் 3NF இடையே என்ன வித்தியாசம்?** — *DBMS, pages 4–6 (Needs multi-page)*
10. **Who won the FIFA World Cup 2022?** — *(Cannot be answered from my documents; out-of-domain control)*

## Run it

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements-dev.txt
copy .env.example .env
uvicorn app.main:app --reload
```

### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
uvicorn app.main:app --reload
```

### Health Check

Open:

```text
http://127.0.0.1:8000/health
```

Or use:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{
    "status": "ok",
    "app": "examate-rag",
    "environment": "local"
}
```

### API Documentation

Once the server is running:

```text
http://127.0.0.1:8000/docs
```

FastAPI automatically provides interactive Swagger API documentation.

## Project Architecture

```text
Student
   │
   │ Tamil / Tanglish / English Question
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
Vector Search (pgvector)
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
```

## Research Objective

The main research objective is to compare the retrieval performance of Tamil questions with equivalent English questions.

The target is:

> Tamil-question retrieval hit rate should be within **5 percentage points** of the English-question retrieval hit rate on 100 paired questions.

## Live link

Added in Week 2.
