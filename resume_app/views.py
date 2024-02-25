# views.py

from django.shortcuts import render
from django.http import HttpResponse
import spacy
import fitz
import os

# Load the model PDF of the ideal resume
model_resume_path = r'C:\Users\deene\OneDrive\Documents\Minor_Project\model\ideal_resume.pdf'
model_resume_doc = fitz.open(model_resume_path)
model_resume_text = " ".join(page.get_text() for page in model_resume_doc)

# Load the spaCy model
nlp = spacy.load(r'C:\Users\deene\OneDrive\Documents\Minor_Project\model\output\model-best')  # Path to your trained model

def parse_resumes(request):
    if request.method == 'POST' and request.FILES.getlist('resumes'):
        resume_files = request.FILES.getlist('resumes')
        path = r'C:\Users\deene\OneDrive\Documents\Minor_Project\test'
        ranked_resumes = []

        for resume_file in resume_files:
            fname = os.path.join(path, resume_file.name)
            doc = fitz.open(fname)
            text = " ".join(page.get_text() for page in doc)

            # Process model resume text
            model_resume_doc = nlp(model_resume_text)

            # Process current resume text
            resume_doc = nlp(text)

            # Calculate similarity score
            similarity_score = model_resume_doc.similarity(resume_doc)

            # Store resume details and similarity score
            ranked_resumes.append({'filename': resume_file.name, 'score': similarity_score})

        # Rank resumes based on similarity score
        ranked_resumes = sorted(ranked_resumes, key=lambda x: x['score'], reverse=True)

        return render(request, 'result_multiple.html', {'ranked_resumes': ranked_resumes})

    return render(request, 'parse_resume.html')
