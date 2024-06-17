# ATS Resume Expert System

This Streamlit application, ATS Resume Expert System, is designed to assist HR professionals in evaluating resumes against job descriptions using AI-powered analysis. It leverages Google's Generative AI (Gemini) to provide insights into resume-job description alignment, missing skills, and areas for improvement.

## Features

- **Upload PDF Resume**: Users can upload a PDF resume, which is then analyzed against a job description provided via text input.
- **AI-powered Analysis**: Utilizes Google's Generative AI (Gemini) to analyze resumes for various aspects:
  - Summary of Resume



  - Percentage Match with Job Description
  - Missing Keywords and Skills
  - Recommendations for Skill Improvement
  - Resources to Enhance Resume
- **Interactive UI**: Buttons for different analysis options are aligned horizontally for ease of use and quick access.

## Technologies Used

- **Streamlit**: Frontend framework for creating interactive web applications using Python.
- **Google Generative AI (Gemini)**: AI model used for natural language processing and content generation.
- **PDF2Image**: Python library to convert PDF pages to images for processing.
- **PIL (Python Imaging Library)**: Python imaging library to handle image data.

## Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your/repository.git
   cd repository-folder

   ```

2. **Install Dependencies:**
   ```pip install -r requirements.txt```

3. ** Configure Environment Variables**
   ```Create a .env file in the root directory with your Google API key:
   GOOGLE_API_KEY=your_google_api_key_here```

4. **Run the Streamlit app:**
   ```streamlit run app.py```
   Replace app.py with the filename of your Streamlit application script.

5. **Use the Application:**

Access the Streamlit app via your browser at ```http://localhost:8501.```

## Usage

Upload PDF Resume: Click on the ```"Upload your resume"``` button and select a PDF file containing the resume you want to analyze.

Input Job Description: Enter the job description or requirements in the ```"Job Description"``` text area.

## Select Analysis Option:
**Summary of Resume:** ```Provides a detailed evaluation of how well the candidate's profile matches the job description.```  
**Percentage Match:** ``` Calculates the percentage match between the resume and the job description.```  
**Missing Word:** ```Identifies and highlights any missing key skills and keywords from the resume.```  
**Skill Improvement:** ```Suggests actionable steps for the candidate to improve their skills and align with the job requirements.```  
**Resource to Improve:** ```Offers resources and suggestions to enhance the candidate's resume for better alignment with the job.```  
**View Results:** ``` The analysis results are displyed in the application interface. Each analysis option generates specific insights based on the comparison between the resume and the job description.```

