# LectureLoom Dataset

## Source

Primary source:
[https://nptel.ac.in/](https://nptel.ac.in/)

National Programme on Technology Enhanced Learning (NPTEL) is a joint initiative of the IITs and IISc offering open online courseware in engineering and science disciplines. LectureLoom uses English transcripts and lecture course materials from NPTEL.

## Dataset Goal

The full LectureLoom system targets:
- **3,000+ transcript pages** of engineering courses across semesters.
- **Departments**: Computer Science and Engineering (CSE), Electronics and Communication Engineering (ECE), and Electrical and Electronics Engineering (EEE).
- **Format**: English source lecture transcripts with timestamps, segmented into discrete lecture pages/slides.
- **Cross-language focus**: Tamil, English, and Tanglish (code-mixed) technical queries evaluated against English course transcripts.
- **Metadata**: Course code, department, lecture index, lecture title, page number, timestamp, and source URL.

## Week 1 Dataset Collection (50+ Pages)

For the Week 1 milestone, **54 pages** of high-quality engineering lecture transcripts were collected and organized across CSE and ECE courses.

| Department | Course Code | Course Name | Lecture Document | Source URL | Pages | Licence / Terms | Downloaded On |
|---|---|---|---|---|---:|---|---|
| CSE | CS8492 | Database Management Systems | `data/raw/cse/dbms_lecture01_intro_and_relational_model.txt` | [NPTEL 106105175](https://nptel.ac.in/courses/106105175) | 10 | CC BY-NC-SA 4.0 | 2026-10-23 |
| CSE | CS8492 | Database Management Systems | `data/raw/cse/dbms_lecture02_normalization.txt` | [NPTEL 106105175](https://nptel.ac.in/courses/106105175) | 10 | CC BY-NC-SA 4.0 | 2026-10-23 |
| CSE | CS8591 | Computer Networks | `data/raw/cse/networks_lecture01_transport_layer_tcp_udp.txt` | [NPTEL 106105081](https://nptel.ac.in/courses/106105081) | 12 | CC BY-NC-SA 4.0 | 2026-10-23 |
| CSE | CS8493 | Operating Systems | `data/raw/cse/os_lecture01_processes_threads_deadlocks.txt` | [NPTEL 106105214](https://nptel.ac.in/courses/106105214) | 10 | CC BY-NC-SA 4.0 | 2026-10-23 |
| ECE | EC8392 | Digital Electronic Circuits | `data/raw/ece/digital_electronics_lecture01_bjt_logic_gates.txt` | [NPTEL 108105132](https://nptel.ac.in/courses/108105132) | 12 | CC BY-NC-SA 4.0 | 2026-10-23 |
| **Total** | | | **5 Lecture Documents** | | **54** | | |

### Department Summary

| Department | Courses Included | Page Count |
|---|---|---:|
| CSE (Computer Science & Engineering) | DBMS, Computer Networks, Operating Systems | 42 |
| ECE (Electronics & Communication Engineering) | Digital Electronic Circuits | 12 |
| **Total Collected** | | **54** |

## Metadata Schema

Every record logged in `data/manifest.csv` contains the following fields:
- `department`: Engineering discipline (e.g., `CSE`, `ECE`).
- `course_code`: University/curriculum course code (e.g., `CS8492`).
- `course_name`: Official title of the course.
- `lecture_number`: Lecture index within the course.
- `lecture_title`: Specific topic covered in the lecture.
- `source_url`: NPTEL online course page.
- `file_path`: Path to the raw transcript file.
- `page_count`: Number of indexed transcript pages.
- `language`: Source language (`English`).
- `licence_status`: Usage terms (`CC BY-NC-SA 4.0`).
- `bytes`: File size in bytes.
- `sha256`: SHA-256 cryptographic checksum for data integrity.
- `downloaded_on`: Date acquired (`2026-10-23`).

## Licence & Terms of Use

All lecture materials are sourced from NPTEL under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)** licence. These materials are utilized solely for non-commercial educational and academic research purposes within the LectureLoom cross-language learning desk.

## Dataset Organization

```text
data/
├── manifest.csv         # Complete registry of all collected files with hash digests
├── raw/                 # Full lecture transcript files (54 pages, not committed to git)
│   ├── cse/
│   │   ├── dbms_lecture01_intro_and_relational_model.txt   (10 pages)
│   │   ├── dbms_lecture02_normalization.txt                (10 pages)
│   │   ├── networks_lecture01_transport_layer_tcp_udp.txt  (12 pages)
│   │   └── os_lecture01_processes_threads_deadlocks.txt    (10 pages)
│   └── ece/
│       └── digital_electronics_lecture01_bjt_logic_gates.txt (12 pages)
└── sample/              # Committed sample excerpts for evaluation
    ├── dbms_sample.txt         (Relational keys & 3NF normalization sample)
    ├── electronics_sample.txt  (Transistor as a switch & cut-off/saturation sample)
    └── networks_sample.txt     (TCP vs UDP & reliable protocol sample)
```
