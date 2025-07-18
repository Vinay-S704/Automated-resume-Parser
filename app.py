import spacy
import subprocess
try:
    spacy.load('en_core_web_sm')
except OSError:
    subprocess.run(['python', '-m', 'spacy', 'download', 'en_core_web_sm'])

import os
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from models import db, Candidate, Skill, Education
from parser import parse_resume

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return jsonify({'message': 'Automated Resume Parser API. Use /upload to POST resumes and /search to query.'})

@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['resume']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    data = parse_resume(filepath)
    candidate = Candidate(name=data['name'])
    db.session.add(candidate)
    db.session.commit()
    for skill in data['skills']:
        db.session.add(Skill(name=skill, candidate_id=candidate.id))
    for edu in data['education']:
        db.session.add(Education(institution=edu, candidate_id=candidate.id))
    db.session.commit()
    return jsonify({'message': 'Resume processed', 'candidate_id': candidate.id})

@app.route('/search', methods=['GET'])
def search_candidates():
    name = request.args.get('name')
    skill = request.args.get('skill')
    education = request.args.get('education')
    query = Candidate.query
    if name:
        query = query.filter(Candidate.name.ilike(f'%{name}%'))
    if skill:
        query = query.join(Skill).filter(Skill.name.ilike(f'%{skill}%'))
    if education:
        query = query.join(Education).filter(Education.institution.ilike(f'%{education}%'))
    results = query.all()
    output = []
    for c in results:
        output.append({
            'id': c.id,
            'name': c.name,
            'skills': [s.name for s in c.skills],
            'education': [e.institution for e in c.education]
        })
    return jsonify(output)

@app.route('/web-upload', methods=['GET', 'POST'])
def web_upload():
    if request.method == 'POST':
        if 'resume' not in request.files:
            return render_template('upload.html', error='No file part')
        file = request.files['resume']
        if file.filename == '':
            return render_template('upload.html', error='No selected file')
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        data = parse_resume(filepath)
        return render_template('upload.html', data=data)
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
