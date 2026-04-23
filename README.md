# Smart Resume Screening System

## 🚀 Overview
This project is a machine learning-based web application that automates the resume screening process. It ranks candidates based on how well their resumes match a given job description, helping recruiters shortlist candidates efficiently.

---

## ⚙️ Features
- Upload and process multiple resumes (PDF format)
- Extract text from resumes using PyPDF2
- Rank candidates using TF-IDF vectorization and cosine similarity
- Basic NLP-based extraction of candidate details (name, email)
- Export ranked results as CSV
- Role-based system with Admin and User authentication

---

## 🧠 How It Works
1. User enters a job description  
2. Uploads multiple resumes  
3. System extracts text from each resume  
4. Converts text into numerical vectors using TF-IDF  
5. Computes similarity score using cosine similarity  
6. Ranks candidates based on relevance  

---

## 🛠️ Tech Stack
- **Backend:** Python, Django  
- **Machine Learning:** Scikit-learn (TF-IDF, Cosine Similarity)  
- **NLP:** Regex, spaCy (basic usage)  
- **File Handling:** PyPDF2  
- **Database:** SQLite  

---

## 📂 Project Structure

Hiring_and_Recruitment/
│
├── manage.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── Hiring_Recruitment/
├── users/
├── admins/
├── assets/


---

## ▶️ How to Run the Project
```bash
git clone <your-repo-link>
cd Hiring_and_Recruitment
pip install -r requirements.txt
python manage.py runserver

Then open:
http://127.0.0.1:8000/

📈 Future Improvements
Skill-based matching (Python, Java, etc.)
Improved NLP using advanced spaCy models
Better UI/UX dashboard for recruiters
Resume classification using ML models
💡 Use Case

This system can be used by HR teams and recruiters to reduce manual effort in screening large volumes of resumes and improve hiring efficiency.

📌 Note

This project demonstrates the application of basic machine learning and NLP techniques in a real-world recruitment scenario.