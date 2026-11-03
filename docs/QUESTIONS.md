# 10 Real Questions My User Will Ask

Write them the way your user would type them. At least 3 must need more than one page to answer, and at least 1 must be a question your documents cannot answer.

These questions represent realistic queries that Tamil Nadu engineering students ask while reviewing lecture materials using Tamil, English, and Tanglish (Tamil-English code-mixing).

| # | Question | Where the answer is (document, page) | Needs more than one page? | Notes / Target Course |
|---|---|---|---|---|
| 1 | டிரான்சிஸ்டர் எப்படி ஸ்விட்சாக வேலை செய்கிறது? | `data/raw/ece/digital_electronics_lecture01_bjt_logic_gates.txt`, pages 2–3 | Yes | Digital Electronics (ECE) — requires Cut-off biasing (p.2) and Saturation circuit analysis (p.3) |
| 2 | Normalization-ல் 3NF என்றால் என்ன? | `data/raw/cse/dbms_lecture02_normalization.txt`, pages 4–5 | Yes | DBMS (CSE) — requires 2NF/prime attribute context (p.4) and transitive dependency elimination (p.5) |
| 3 | What is the difference between TCP and UDP? | `data/raw/cse/networks_lecture01_transport_layer_tcp_udp.txt`, pages 2–4 | Yes | Computer Networks (CSE) — spans UDP mechanics (p.2), TCP byte-stream (p.3), and comparison (p.4) |
| 4 | TCP ஏன் reliable protocol என்று அழைக்கப்படுகிறது? | `data/raw/cse/networks_lecture01_transport_layer_tcp_udp.txt`, page 6 | No | Computer Networks (CSE) — fully answered by reliability mechanisms (checksums, sequence numbers, ACKs) |
| 5 | Process மற்றும் Thread இடையே என்ன வித்தியாசம்? | `data/raw/cse/os_lecture01_processes_threads_deadlocks.txt`, pages 3–4 | Yes | Operating Systems (CSE) — requires thread definition (p.3) and memory/context switch comparison (p.4) |
| 6 | What is a primary key in DBMS? | `data/raw/cse/dbms_lecture01_intro_and_relational_model.txt`, page 4 | No | DBMS (CSE) — uniquely identifying candidate key with entity integrity constraint |
| 7 | Deadlock என்றால் என்ன? | `data/raw/cse/os_lecture01_processes_threads_deadlocks.txt`, page 7 | No | Operating Systems (CSE) — blocked state defined with the 4 Coffman conditions |
| 8 | What is the purpose of normalization in a database? | `data/raw/cse/dbms_lecture02_normalization.txt`, page 2 | No | DBMS (CSE) — eliminating redundancy and preventing insertion, update, and deletion anomalies |
| 9 | 2NF மற்றும் 3NF இடையே என்ன வித்தியாசம்? | `data/raw/cse/dbms_lecture02_normalization.txt`, pages 4–6 | Yes | DBMS (CSE) — partial dependencies (p.4) vs transitive dependencies (p.5) and direct comparison (p.6) |
| 10 | Who won the FIFA World Cup 2022? | none (cannot be answered from my documents) | No | Out-of-domain evaluation question; system must reject or state absence of supporting document |

## Evaluation Criteria Breakdown

- **Total questions**: 10
- **Multi-page questions**: 5 (Q1, Q2, Q3, Q5, Q9 — requirement was at least 3)
- **Unanswerable question**: 1 (Q10 — requirement was at least 1)
- **Language distribution**:
  - Pure Tamil / Tanglish: 5 questions (Q1, Q2, Q4, Q5, Q7, Q9)
  - English: 4 questions (Q3, Q6, Q8, Q10)
