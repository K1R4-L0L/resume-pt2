import PyPDF2
import docx2txt
import re
import spacy

nlp = spacy.load('en_core_web_sm')

def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
        text = ''.join([page.extract_text() for page in reader.pages])
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def extract_text_from_docx(docx_path):
    try:
        text = docx2txt.process(docx_path)
        return text
    except Exception as e:
         print(f"Error extracting text from DOCX: {e}")
         return ""
    
def clean_text(text):
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'[^\w\s]', '', text)
    return text

def analyze_resume(text):
    doc = nlp(text)
    skills = [token.text for token in doc if token.pos_ in ('NOUN', 'PROPN')]
    experience_keywords = ['experience', 'work', 'job', 'position', 'role']
    experience_sentences = [sent.text for sent in doc.sents if any(keyword in sent.text.lower() for keyword in experience_keywords)]

    return {'skills': skills, 'experience': experience_sentences} 


def score_resume(analysis_results, required_skills, min_experience_years=0):
    score = 0
    if analysis_results:
       if 'skills' in analysis_results:
            score += sum(1 for skill in analysis_results.get('skills', []) if skill.lower() in required_skills)
    if 'experience' in analysis_results:
             score += len(analysis_results.get('experience', [])) * 2
    return score

def main():
    resume_path = input("Enter the path to the resume file (PDF or DOCX): ")
    required_skills_input = input("Enter required skills (comma-separated): ")
    required_skills = [skill.strip().lower() for skill in required_skills_input.split(',')]

    # Validate user input for minimum experience years
    try:
        min_experience_years = int(input("Enter minimum required experience in years: "))
    except ValueError:
        print("Invalid input. Please enter a valid number for experience.")
        return

    if resume_path.lower().endswith('.pdf'):
        resume_text = extract_text_from_pdf(resume_path)
    elif resume_path.lower().endswith('.docx'):
        resume_text = extract_text_from_docx(resume_path)
    else:
        print("Unsupported file format. Please provide a PDF or DOCX file.")
        return
    
    if not resume_text:
        print("No text extracted from the resume. Please check the file or its content.")
        return

    cleaned_text = clean_text(resume_text)
    analysis_results = analyze_resume(cleaned_text)
    resume_score = score_resume(analysis_results, required_skills, min_experience_years)

    print("\nAnalysis Results:")
    print(f"Skills: {analysis_results.get('skills', [])}")
    print(f"Experience snippets: {analysis_results.get('experience', [])}")
    print(f"\nResume Score: {resume_score}")
    print(f"Required Skills: {required_skills}")
    print(f"Minimum Experience (Years): {min_experience_years}")
    
    if resume_score > len(required_skills) + min_experience_years * 2:
        print("Resume is a good fit.")
    else:
        print("Resume does not meet the criteria.")

if __name__ == "__main__":
    main()