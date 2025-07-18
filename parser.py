import os
import pdfplumber
import docx
import spacy

nlp = spacy.load('en_core_web_sm')

def extract_text_from_pdf(path):
    text = ''
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + '\n'
    return text

def extract_text_from_docx(path):
    doc = docx.Document(path)
    return '\n'.join([p.text for p in doc.paragraphs])

def parse_resume(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == '.pdf':
        text = extract_text_from_pdf(filepath)
    elif ext in ['.docx', '.doc']:
        text = extract_text_from_docx(filepath)
    else:
        raise ValueError('Unsupported file type')
    doc = nlp(text)
    name = ''
    skills = []
    education = []
    for ent in doc.ents:
        if ent.label_ == 'PERSON' and not name:
            name = ent.text
        if ent.label_ == 'ORG':
            education.append(ent.text)
    # Simple skill extraction (customize as needed)
    skill_keywords = ['python', 'java', 'sql', 'flask', 'nlp', 'machine learning', 'data analysis']
    for token in doc:
        if token.text.lower() in skill_keywords:
            skills.append(token.text)
    return {'name': name, 'skills': list(set(skills)), 'education': list(set(education))}
