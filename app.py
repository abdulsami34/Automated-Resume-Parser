import os
import re
from flask import Flask, request, jsonify, render_template
from pdfminer.high_level import extract_text
import spacy
from spacy.matcher import Matcher

app = Flask(__name__)

def extract_name(resume_text):
    nlp = spacy.load('en_core_web_sm')
    matcher = Matcher(nlp.vocab)

    # Define name patterns
    patterns = [
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}],  # First name and Last name
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}],  # First name, Middle name, and Last name
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}],  # First name, Middle name, Middle name, and Last name
        [{'IS_ALPHA': True, 'IS_UPPER': True}, {'IS_ALPHA': True, 'IS_UPPER': True}],  # Uppercase names
    ]

    for pattern in patterns:
        matcher.add('NAME', [pattern])

    doc = nlp(resume_text)
    matches = matcher(doc)

    for match_id, start, end in matches:
        span = doc[start:end]
        return span.text

    return None

def extract_contact_number_from_resume(text):
    pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
    match = re.search(pattern, text)
    return match.group() if match else None

def extract_email_from_resume(text):
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    match = re.search(pattern, text)
    return match.group() if match else None

def extract_skills_from_resume(text, skills_list):
    skills = []
    for skill in skills_list:
        pattern = r"\b{}\b".format(re.escape(skill))
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            skills.append(skill)
    return skills

def extract_education_from_resume(text):
    pattern = r"(?i)\b(?:B\.?S\.?|BSC|B\.?A\.?|B\.?TECH|B\.?COM|M\.?S\.?|MSC|M\.?A\.?|M\.?TECH|M\.?COM|PH\.?D|BACHELORS(?:'S)?|MASTERS(?:'S)?|INTERMEDIATE|SCHOOL|DIPLOMA|CERTIFICATE|DEGREE|ASSOCIATE)\b.*?(?:\([A-Za-z]+\))?.*?(?:(?:,|\bat\b)?\s*(?:[A-Z][a-z]+\s?)+,?\s*\d{4})?"
    matches = re.findall(pattern, text, re.IGNORECASE)
    return [match.strip() for match in matches]

def extract_experience_from_text(text):
    pattern = re.compile(r'EXPERIENCE(.*?)(?=(EDUCATION|SKILLS|$))', re.IGNORECASE | re.DOTALL)
    match = pattern.search(text)
    return match.group(1).strip() if match else "Experience section not found"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/parse-resume', methods=['POST'])
def parse_resume():
    if 'resume' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['resume']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and file.filename.endswith('.pdf'):
        file_path = os.path.join('/tmp', file.filename)
        file.save(file_path)

        text = extract_text(file_path)
        os.remove(file_path)

        name = extract_name(text)
        contact_number = extract_contact_number_from_resume(text)
        email = extract_email_from_resume(text)
        
        skills_list = [
            'Python', 'Data Analysis', 'Machine Learning', 'Deep Learning', 'NLP', 'Computer Vision',
            'Java', 'C++', 'C#', 'SQL', 'NoSQL', 'HTML', 'CSS', 'JavaScript', 'React', 'Angular', 
            'Node.js', 'Django', 'Flask', 'Spring', 'Ruby on Rails', 'Git', 'Docker', 'Kubernetes',
            'AWS', 'Azure', 'GCP', 'TensorFlow', 'Keras', 'PyTorch', 'OpenCV', 'scikit-learn', 
            'Pandas', 'NumPy', 'Matplotlib', 'Seaborn', 'Tableau', 'PowerBI', 'Spark', 'Hadoop',
            'Project Management', 'Agile', 'Scrum', 'Communication', 'Leadership', 'Problem Solving'
        ]
        
        skills = extract_skills_from_resume(text, skills_list)
        education = extract_education_from_resume(text)
        experience = extract_experience_from_text(text)

        return jsonify({
            'name': name,
            'contactNumber': contact_number,
            'email': email,
            'skills': skills,
            'education': education,
            'experience': experience
        })
    else:
        return jsonify({'error': 'Invalid file format'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

