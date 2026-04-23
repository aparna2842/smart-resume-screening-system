from django.shortcuts import render
from .forms import UserRegistrationForm
from django.contrib import messages
from .models import UserRegistrationModel
from django.conf import settings

import PyPDF2
import re
import os
from django.core.files.storage import FileSystemStorage

from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# 🔥 Load AI model (only once)
model = SentenceTransformer('paraphrase-MiniLM-L3-v2')

# 🔥 Skills database
SKILLS_DB = [
    "python", "java", "c++", "sql", "django", "flask",
    "machine learning", "deep learning", "nlp",
    "html", "css", "javascript", "react",
    "mongodb", "mysql", "pandas", "numpy"
]


# =========================
# USER REGISTRATION
# =========================
def UserRegisterActions(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have been successfully registered')
            form = UserRegistrationForm()
            return render(request, 'UserRegistrations.html', {'form': form})
        else:
            messages.success(request, 'Email or Mobile Already Exists')
    else:
        form = UserRegistrationForm()

    return render(request, 'UserRegistrations.html', {'form': form})


# =========================
# USER LOGIN
# =========================
def UserLoginCheck(request):
    if request.method == "POST":
        loginid = request.POST.get("loginid")
        password = request.POST.get("pswd")

        try:
            user = UserRegistrationModel.objects.get(
                loginid=loginid,
                password=password
            )

            if user.status == "activated":
                request.session['id'] = user.id
                request.session['loginid'] = user.loginid
                request.session['email'] = user.email

                return render(request, 'users/UserHome.html', {})
            else:
                messages.success(request, "Your account is not activated")

        except:
            messages.success(request, 'Invalid login details')

    return render(request, 'UserLogin.html', {})


def UserHome(request):
    return render(request, "users/UserHome.html", {})


# =========================
# PDF TEXT EXTRACTION
# =========================
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text


# =========================
# EMAIL EXTRACTION
# =========================
def extract_entities(text):
    email_pattern = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
    emails = re.findall(email_pattern, text)
    return emails if emails else ["Not Found"]


# =========================
# SKILL EXTRACTION
# =========================
def extract_skills(text):
    text = text.lower()
    found_skills = []

    for skill in SKILLS_DB:
        if skill in text:
            found_skills.append(skill)

    return found_skills


# =========================
# MAIN AI RESUME SCREENING
# =========================
def index(request):
    results = []

    if request.method == 'POST':
        job_description = request.POST.get('job_description')
        job_skills = extract_skills(job_description)
        resume_files = request.FILES.getlist('resume_files')

        # Create upload folder
        upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        processed_resumes = []

        # Process resumes
        for resume_file in resume_files:
            fs = FileSystemStorage(location=upload_dir)
            filename = fs.save(resume_file.name, resume_file)
            resume_path = os.path.join(upload_dir, filename)

            resume_text = extract_text_from_pdf(resume_path)
            skills = extract_skills(resume_text)

            processed_resumes.append({
                "emails": [resume_file.name],
                "text": resume_text,
                "skills": skills
            })

        # 🔥 AI MATCHING
        job_embedding = model.encode(job_description)

        ranked_resumes = []

    for res in processed_resumes:
     resume_embedding = model.encode(res["text"])

    similarity = cosine_similarity(
        [job_embedding],
        [resume_embedding]
    )[0][0] * 100

    # Skill match score
    matched_skills = list(set(res["skills"]) & set(job_skills))
    skill_score = (len(matched_skills) / len(job_skills)) * 100 if job_skills else 0

    # Final score
    final_score = (
        0.5 * similarity +
        0.3 * skill_score +
        0.2 * similarity
    )

    ranked_resumes.append({
        "emails": res["emails"],
        "similarity": round(similarity, 2),
        "skills": res["skills"],
        "matched_skills": matched_skills,
        "final_score": round(final_score, 2)
    })

        # Sort results
    ranked_resumes.sort(key=lambda x: x["final_score"], reverse=True)

    results = ranked_resumes
    return render(request, 'users/upload_resumes.html', {'results': results})