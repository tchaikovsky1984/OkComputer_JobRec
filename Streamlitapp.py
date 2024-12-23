import streamlit as st
import json
import PyPDF2
from jobspy import scrape_jobs
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PyPDF2 import PdfReader
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import string
import json
from streamlit.components.v1 import html

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt_tab')

stop_words = set(stopwords.words('english'))
punctuation = set(string.punctuation)
lemmatizer = WordNetLemmatizer()
SKILL_SET = [
    # Technical Skills
    # Programming and Development
    " Python ", " Java ", " JavaScript ", " C++ ", " SQL ", " HTML/CSS ", " PHP ", " Ruby on Rails ",
    " Swift ", " Kotlin ", " R ", " MATLAB ", " SAS ", " Go ", " Perl ", " Scala ", " Rust ", " TypeScript ",

    # Data Science and Analytics
    " Machine Learning ", " Deep Learning ", " Data Analysis ", " Data Visualization ",
    " Statistical Analysis ", " Big Data ", " Hadoop ", " Spark ", " Tableau ", " Power BI ",
    " NumPy ", " Pandas ", " Scikit-learn ", " TensorFlow ", " PyTorch ", " Natural Language Processing (NLP) ",
    " Time Series Analysis ",

    # Cloud Computing
    " Amazon Web Services (AWS) ", " Microsoft Azure ", " Google Cloud Platform (GCP) ",
    " Kubernetes ", " Docker ", " Cloud Security ", " Terraform ", " OpenStack ", " CloudFormation ",
    " Jenkins ", " CI/CD ",

    # Networking and Cybersecurity
    " Network Administration ", " Firewalls ", " VPN ", " Intrusion Detection Systems (IDS) ",
    " Intrusion Prevention Systems (IPS) ", " Ethical Hacking ", " Penetration Testing ",
    " Cryptography ", " ISO 27001 ", " SOC (Security Operations Center) ",
    " SIEM (Security Information and Event Management) ", " PKI (Public Key Infrastructure) ",

    # Engineering and Manufacturing
    " AutoCAD ", " SolidWorks ", " MATLAB ", " CATIA ", " ANSYS ", " Robotics ", " 3D Printing ",
    " CNC Programming ", " Six Sigma ", " Lean Manufacturing ", " Electrical Circuit Design ",
    " PCB Design ", " Hydraulic Systems ",

    # Healthcare and Biotech
    " Electronic Health Records (EHR) ", " Medical Coding ", " Medical Imaging ",
    " Clinical Research ", " Genomics ", " Biotechnology ", " Drug Development ",
    " Pharmacology ", " Patient Care Systems ", " Telemedicine ",

    # Business and Finance
    " Financial Modeling ", " Excel ", " QuickBooks ", " SAP ", " Oracle ERP ",
    " Risk Management ", " Budgeting ", " Tax Preparation ", " Investment Analysis ",
    " Stock Market Analysis ",

    # Creative and Media
    " Graphic Design ", " Adobe Photoshop ", " Adobe Illustrator ",
    " Adobe Premiere Pro ", " Video Editing ", " Animation ", " UI/UX Design ", " Canva ",
    " Content Writing ", " SEO ", " Social Media Management ", " Blogging ",

    # Managerial Skills
    # Leadership and Management
    " Strategic Planning ", " Team Management ", " Project Management ",
    " Time Management ", " Decision Making ", " Problem Solving ", " Delegation ",
    " Negotiation ", " Stakeholder Management ", " Change Management ", " Conflict Resolution ",

    # Communication Skills
    " Verbal Communication ", " Written Communication ", " Presentation Skills ",
    " Public Speaking ", " Active Listening ", " Emotional Intelligence ",
    " Cross-Cultural Communication ",

    # Analytical and Organizational Skills
    " Critical Thinking ", " Data Interpretation ", " Workflow Optimization ",
    " Resource Allocation ", " Goal Setting ", " Performance Tracking ", " Risk Assessment ",

    # Marketing and Sales
    " Market Research ", " Sales Strategies ", " CRM Tools (Customer Relationship Management) ",
    " Branding ", " Product Marketing ", " Pricing Strategies ", " Customer Engagement ",
    " Affiliate Marketing ", " Copywriting ",

    # Human Resources
    " Recruitment ", " Employee Relations ", " Training and Development ",
    " Performance Appraisal ", " Payroll Management ", " Diversity and Inclusion ",
    " HRIS (Human Resource Information System) ",

    # Operations Management
    " Logistics ", " Supply Chain Management ", " Procurement ",
    " Inventory Management ", " Quality Assurance ", " Vendor Management "
]

def ResumeReader(pdf_path):
    reader = PdfReader(pdf_path)
    number_of_pages = len(reader.pages)
    text = ""
    for i in range(number_of_pages):
        page = reader.pages[i]
        text += page.extract_text()
    return text

def preprocess_resume(text):
    tokens = word_tokenize(text.lower())
    tokens = [
        word for word in tokens
        if word not in stop_words and word not in punctuation and word.isalnum()
    ]
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return ' '.join(tokens)
def scraper(jobtitle=None,pref_country=None,pref_area=None,no_of_output=300):
  if jobtitle==None:
    if pref_country==None:
      if pref_area==None:
        jobs = scrape_jobs(
          site_name=["indeed", "linkedin", "zip_recruiter", "glassdoor", "google"],
          results_wanted=no_of_output,
          hours_old=72,
          )
      else:
        jobs = scrape_jobs(
          site_name=["indeed", "linkedin", "zip_recruiter", "glassdoor", "google"],
          results_wanted=no_of_output,
          hours_old=72,
          location=pref_area
          )
    else:
      if pref_area==None:
        jobs = scrape_jobs(
          site_name=["indeed", "linkedin", "zip_recruiter", "glassdoor", "google"],
          results_wanted=no_of_output,
          hours_old=72,
          country_indeed=pref_country
          )
      else:
        jobs = scrape_jobs(
          site_name=["indeed", "linkedin", "zip_recruiter", "glassdoor", "google"],
          results_wanted=no_of_output,
          hours_old=72,
          country_indeed=pref_country,
          location=pref_area
          )
  else:
    if pref_country==None:
      if pref_area==None:
        jobs = scrape_jobs(
          site_name=["indeed", "linkedin", "zip_recruiter", "glassdoor", "google"],
          search_term=jobtitle,
          google_search_term=jobtitle,
          results_wanted=no_of_output,
          hours_old=72,
          )
      else:
        jobs = scrape_jobs(
          site_name=["indeed", "linkedin", "zip_recruiter", "glassdoor", "google"],
          search_term=jobtitle,
          google_search_term=jobtitle,
          results_wanted=no_of_output,
          hours_old=72,
          location=pref_area
          )
    else:
      if pref_area==None:
        jobs = scrape_jobs(
          site_name=["indeed", "linkedin", "zip_recruiter", "glassdoor", "google"],
          search_term=jobtitle,
          google_search_term=jobtitle,
          results_wanted=no_of_output,
          hours_old=72,
          country_indeed=pref_country
          )
      else:
        jobs = scrape_jobs(
          site_name=["indeed", "linkedin", "zip_recruiter", "glassdoor", "google"],
          search_term=jobtitle,
          google_search_term=jobtitle,
          results_wanted=no_of_output,
          hours_old=72,
          country_indeed=pref_country,
          location=pref_area,
          )
  return jobs

def preprocess_scraped_data(jobs):
    new_jobs=jobs.copy()
    new_jobs['combined_text'] = new_jobs.drop(columns=['id','site', 'job_url', 'job_url_direct', 'date_posted', 'emails', 'company_url', 'company_logo', 'company_url_direct']).astype(str).apply(' '.join, axis=1)
    new_jobs['preprocessed_text'] = new_jobs['combined_text'].apply(preprocess_resume)
    new_jobs = new_jobs.drop_duplicates(subset=['combined_text'])
    return new_jobs

def predict(new_jobs, new_text):
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(new_jobs['preprocessed_text'])

    def recommend_jobs(new_text, top_n=80):
        candidate_vector = vectorizer.transform([new_text.lower()])
        similarities = cosine_similarity(candidate_vector, tfidf_matrix)
        sorted_indices = similarities.argsort()[0][::-1]
        return new_jobs.iloc[sorted_indices[:top_n]]
    return recommend_jobs(new_text, top_n=80)

def extract_skills(text, skills):
    matched_skills = []
    text_lower = text.lower()
    for skill in skills:
        if skill.lower() in text_lower:
            matched_skills.append(skill)
    return matched_skills

def match_skills(job_data, resume_text, skill_set):
    result = {}
    user_skills = extract_skills(resume_text, skill_set)

    for _, row in job_data.iterrows():
        job_id = row['id']
        job_description = row['combined_text']

        job_skills = extract_skills(job_description, skill_set)
        matched_skills = [skill for skill in job_skills if skill in user_skills]
        missing_skills = [skill for skill in job_skills if skill not in user_skills]

        result[job_id] = [matched_skills, missing_skills]

    filtered_result = {job_id: skills for job_id, skills in result.items()
                       if len(skills[0]) - len(skills[1]) >= 0 and len(skills[0])>0}

    return filtered_result

def add_skills_to_json(formatted_jobs, skill_matches):
    formatted_jobs['skills_matched'] = formatted_jobs['id'].apply(
        lambda job_id: skill_matches.get(job_id, ([], []))[0]
    )
    formatted_jobs['skills_missing'] = formatted_jobs['id'].apply(
        lambda job_id: skill_matches.get(job_id, ([], []))[1]
    )

    return formatted_jobs

def main( resume_text,job_title, job_location, num_outputs):
    job_country = None
    job_area = None

    # Split job_location if it contains a comma, else handle separately
    if job_location!=None:
        if ',' in job_location:
            job_area, job_location = job_location.strip().split(',')
            job_country = job_location.strip()
        else:
            job_area = job_location.strip() if job_location else None
            job_country = job_location.strip() if job_location else None

    # Validate job_country is one of the accepted countries
    if job_country and job_country.lower().strip() not in ['argentina', 'australia', 'austria', 'bahrain', 'belgium', 'brazil', 'canada', 'chile', 'china', 'colombia', 'costa rica', 'czech republic', 'czechia', 'denmark', 'ecuador', 'egypt', 'finland', 'france', 'germany', 'greece', 'hong kong', 'hungary', 'india', 'indonesia', 'ireland', 'israel', 'italy', 'japan', 'kuwait', 'luxembourg', 'malaysia', 'malta', 'mexico', 'morocco', 'netherlands', 'new zealand', 'nigeria', 'norway', 'oman', 'pakistan', 'panama', 'peru', 'philippines', 'poland', 'portugal', 'qatar', 'romania', 'saudi arabia', 'singapore', 'south africa', 'south korea', 'spain', 'sweden', 'switzerland', 'taiwan', 'thailand', 'türkiye', 'turkey', 'ukraine', 'united arab emirates', 'uk', 'united kingdom', 'usa', 'us', 'united states', 'uruguay', 'venezuela', 'vietnam', 'usa/ca', 'worldwide']:
        job_country = None  # Set job_country to None if not valid
    jobs = scraper(jobtitle=job_title, pref_country=job_country, pref_area=job_area,no_of_output=num_outputs)

    new_jobs = preprocess_scraped_data(jobs)

    # resume_text = ResumeReader(filepath)
    preprocessed_resume = preprocess_resume(resume_text)

    recommended_jobs = predict(new_jobs, preprocessed_resume)

    skill_matches = match_skills(recommended_jobs, preprocessed_resume, SKILL_SET)
    recommended_jobs = recommended_jobs[recommended_jobs['id'].isin(skill_matches.keys())]
    recommended_jobs = add_skills_to_json(recommended_jobs, skill_matches)
    formatted_jobs = {
        "jobs": [
            {
                "job_title": row.get("title", "N/A"),
                "job_id": row.get("id", "N/A"),
                "company": row.get("company", "N/A"),
                "site": row.get("site", "N/A"),
                "location": row.get("location", "N/A"),
                "job_type": row.get("job_type", "N/A"),
                "interval": row.get("interval", "N/A"),
                "job_url": row.get("job_url", "N/A"),
                "description": row.get("description", "N/A"),
                "skills_matched": row.get("skills_matched", []),
                "skills_missing": row.get("skills_missing", [])
            }
            for _, row in recommended_jobs.iterrows()
        ]
    }

    json_result = json.dumps(formatted_jobs, indent=4)

    return json_result

# Function to extract text from a resume PDF
def extract_resume_text(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def color_skills(post):
    matched = ", ".join(post.get("skills_matched", []))
    missing = ", ".join(post.get("skills_missing", []))
    return matched, missing

# Sidebar for user inputs
with st.sidebar:
    st.write("### Enter Details")
    pdf_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    job_title = st.text_input("Job Title (Optional)", placeholder="e.g., Data Scientist")
    job_location = st.text_input("Job Location (Optional)", placeholder="e.g., New York")
    domain = st.slider("Job Search Domain", 300, 3000, 300)
    search_button = st.button("Get Job Postings")

# Main view for displaying job results
st.write("## Job Search Results")

if search_button:
    if pdf_file:
        # Extract text from the resume PDF
        resume_text = extract_resume_text(pdf_file)

        # Assign None to job_title and job_location if left empty
        if not job_title:
            job_title = None
        if not job_location:
            job_location = None

        # Fetch job postings using the model function
        job_posts = main(resume_text, job_title, job_location, domain)

        try:
            # Parse the JSON string if necessary
            if isinstance(job_posts, str):
                job_posts = json.loads(job_posts)

            job_list = job_posts.get("jobs", [])
            if job_list:
                # Prepare data for the table
                table_data = []
                for post in job_list:
                    matched, missing = color_skills(post)
                    table_data.append({
                        "Job Title": post.get("job_title", "N/A"),
                        "Company": post.get("company", "N/A"),
                        "Location": post.get("location", "N/A"),
                        "Matching Skills": matched,
                        "Missing Skills": missing,
                    })

                # Convert to a DataFrame
                df = pd.DataFrame(table_data)

                # Display the table with interactive styling
                st.write("### Job Postings")
                st.write(df)

                # Expandable details
                for i, post in enumerate(job_list, start=1):
                    with st.expander(f"{post.get('job_title', 'N/A')} at {post.get('company', '')},{post.get('location','')}"):
                        st.write(f"**Job Title:** {post.get('job_title', 'N/A')}")
                        st.write(f"**Company:** {post.get('company', 'N/A')}")
                        st.write(f"**Location:** {post.get('location', 'N/A')}")
                        st.write(f"**Job Type:** {post.get('job_type', 'N/A')}")
                        st.write(f"**Description:** {post.get('description', 'N/A')}")
                        st.write(f"**Matching Skills:** {', '.join(post.get('skills_matched', []))}")
                        st.write(f"**Missing Skills:** {', '.join(post.get('skills_missing', []))}")
                        st.write(f"[**Job URL**]({post.get('job_url', '#')})")
            else:
                st.write("No job postings found.")
        except json.JSONDecodeError:
            st.error("Failed to parse the job postings. Please check the model's output.")
    else:
        st.warning("Please fill in all the fields and upload a valid resume PDF.")
