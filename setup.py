import os
from app import db, app
import subprocess

def setup_db():
    with app.app_context():
        db.create_all()
        print('Database tables created.')

def download_spacy_model():
    try:
        import spacy
        spacy.load('en_core_web_sm')
        print('spaCy model already installed.')
    except Exception:
        print('Downloading spaCy en_core_web_sm model...')
        subprocess.run(['python', '-m', 'spacy', 'download', 'en_core_web_sm'])

if __name__ == '__main__':
    setup_db()
    download_spacy_model()
    print('Setup complete.')
