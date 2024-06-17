
import google.generativeai as genai
import pdf2image
from PIL import Image
import os
import streamlit as st
from dotenv import load_dotenv
import io
import base64
import time

load_dotenv()

# Configure the Google API key
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)


def get_gemini_response(input_text, pdf_content, prompt):
    # Assuming you have a GenerativeModel named "gemini-pro-vision"
    model = genai.GenerativeModel("gemini-pro-vision")
    # Generate response
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text


def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert PDF to image
        try:
            images = pdf2image.convert_from_bytes(uploaded_file.read())
        except PDFInfoNotInstalledError as e:
            st.error("PDFInfo is not installed or not in PATH.")
            raise e
        except PDFPageCountError as e:
            st.error("Unable to get page count.")
            raise e
        except Exception as e:
            st.error(f"An error occurred: {e}")
            raise e

        first_page = images[0]  # content of the first page of the PDF
        # Convert image to bytes
        image_byte_arr = io.BytesIO()
        # Saving image in JPEG format
        first_page.save(image_byte_arr, format="JPEG")
        image_byte_arr = image_byte_arr.getvalue()  # getting the value

        # Prepare PDF content for API
        pdf_parts = [{
            "mime_type": "image/jpeg",
            # Encode to base64
            "data": base64.b64encode(image_byte_arr).decode()
        }]

        return pdf_parts
    else:
        # error if file is not uploaded
        raise FileNotFoundError("No file uploaded")

# Function to display response line by line using st.empty


# Streamlit app
st.set_page_config(page_title="ATS Resume Expert System")
st.header("ATS Tracking System")

input_text = st.text_area("Job Description", key="input")
uploaded_file = st.file_uploader("Upload your resume", type=['pdf'])

if uploaded_file:
    st.write("PDF uploaded successfully!!!")


# Prompt for button1
detail_about_prompt = """

You are an experienced HR professional with technical expertise in one of the following job roles: Data Science, Full Stack Web Development, Big Data, Data Engineering, DevOps, or Data Analysis. Your task is to review the provided resume against a specific job description in one of these fields.

Please provide a professional evaluation of whether the candidate's profile aligns with the role. The evaluation should be detailed and point-wise, covering the following aspects:

1. **Overall Alignment**: A brief summary of how well the candidate’s profile matches the job description.
2. **Key Strengths**: Highlight the main strengths and relevant skills the candidate possesses that align with the job requirements.
4. **Relevant Experience**: Evaluate the candidate's work experience and how it relates to the responsibilities and requirements of the job.
5. **Technical Skills**: Assess the candidate’s technical skills and knowledge pertinent to the job role.
6. **Certifications and Education**: Review the candidate’s educational background and any relevant certifications.
7. **Soft Skills**: Comment on the candidate’s soft skills, such as communication, teamwork, and problem-solving, if mentioned in the resume.
8. **Final Recommendation**: Provide a summary of your professional opinion on the candidate’s suitability for the role and any steps they could take to improve their alignment with the job requirements.

Please ensure your evaluation is precise, thorough, and presented in a clear, point-wise manner.

"""

skill_improve_prompt = """

You are an experienced HR professional with a background in Data Science, Full Stack Web Development, Big Data, Data Engineering, DevOps, or Data Analysis. Your task is to review the provided resume against a specific job description in one of these fields.

1. Identify and highlight weaknesses or gaps in skills and experience on the resume in relation to the job description.
2. Highlight essential knowledge areas and skills that are required for the job but are missing or underrepresented in the resume.
3. Suggest practical and actionable steps the candidate can take to improve their skills and knowledge to better align with the job requirements in specific domain.

Please be detailed in your analysis and recommendations.

"""

resource_prompt = '''
You are an experienced HR professional with a background in Data Science, Full Stack Web Development, Big Data, Data Engineering, DevOps, or Data Analysis. Your task is to review the provided resume against a specific job description in one of these fields.

1. Identify and highlight weaknesses or gaps in skills and experience on the resume in relation to the job description.
2. Highlight essential knowledge areas and skills that are required for the job but are missing or underrepresented in the resume.
3. Suggest practical and actionable steps the candidate can take to improve their skills and knowledge to better align with the job requirements in specific domain.

Please be detailed in your analysis and recommendations.

'''

# Prompt for button4
missing_prompt = """

You are a skilled ATS (Applicant Tracking System) scanner with deep expertise in one of the following job roles: Data Science, Full Stack Web Development, Big Data, Data Engineering, DevOps, or Data Analysis. Additionally, you have a thorough understanding of ATS functionality and how it evaluates resumes.

Your task is to meticulously review the provided resume against the detailed job description. Specifically, you should:

1. Identify and highlight any key skills, technologies, certifications, and relevant keywords that are mentioned in the job description but are missing from the resume.
2. Focus on the critical keywords and phrases that are essential for meeting the job requirements.
3. Ensure your analysis pinpoints the exact words or phrases that need to be added to the resume to improve its match with the job description and increase the chances of passing through the ATS screening process.

Please be precise and thorough in your evaluation.


# You are a skilled ATS(Applicant Tracking System) scanner with a deep understanding of one job role Data Science or Full Stack Web Development, Big Data, Data Engineering, DevOps, Data Analyst, and deep ATS functionality.
# Your task is to evaluate the resume against the provided job description.Highlight the missing word key for meeting  the requirement of the job role.
"""


# Prompt for button4
matching_percentage_prompt = """
You are a skilled ATS (Applicant Tracking System) scanner with deep expertise in one of the following job roles: Data Science, Full Stack Web Development, Big Data, Data Engineering, DevOps, or Data Analysis. Additionally, you have a thorough understanding of ATS functionality and how it evaluates resumes.

Your task is to meticulously review the provided resume against the detailed job description. Specifically, you should:

1. Calculate the percentage match between the resume and the job description, indicating how well the resume aligns with the job requirements.
2. Identify and list the key skills, technologies, certifications, and relevant keywords that are mentioned in the job description but are missing from the resume.
3. Provide final thoughts on the overall alignment of the resume with the job description, including any general recommendations for improvement.

The output should be structured as follows:
1. Percentage match between the resume and the job description.
2. List of missing keywords.
3. Final thoughts and recommendations.

Please ensure the analysis is precise and thorough.


"""


if st.button("Summary of Resume"):
    if uploaded_file is not None:
        st.subheader("The Response is:")
        with st.spinner("Generating response...."):
            placeholder = st.empty()
            response_text = ""
            pdf_content = input_pdf_setup(uploaded_file)

            for chunk in get_gemini_response(
                    input_text, pdf_content, detail_about_prompt):
                response_text += chunk
                placeholder.write(response_text)

        # st.write(response)
    else:
        st.write("Please upload the PDF file")


if st.button("Percentage Match"):
    if uploaded_file is not None:
        st.subheader("The Response is:")
        with st.spinner("Generating response...."):
            placeholder = st.empty()
            response_text = ""
            pdf_content = input_pdf_setup(uploaded_file)

            for chunk in get_gemini_response(
                    input_text, pdf_content, matching_percentage_prompt):
                response_text += chunk
                placeholder.write(response_text)

        # st.write(response)
    else:
        st.write("Please upload the PDF file")


if st.button("Missing Word"):
    if uploaded_file is not None:
        st.subheader("The Response is:")
        with st.spinner("Generating response...."):
            placeholder = st.empty()
            response_text = ""
            pdf_content = input_pdf_setup(uploaded_file)

            for chunk in get_gemini_response(
                    input_text, pdf_content, missing_prompt):
                response_text += chunk
                placeholder.write(response_text)

        # st.write(response)
    else:
        st.write("Please upload the PDF file")


if st.button("Skill Improvement"):
    if uploaded_file is not None:
        st.subheader("The Response is:")
        with st.spinner("Generating response...."):
            placeholder = st.empty()
            response_text = ""
            pdf_content = input_pdf_setup(uploaded_file)

            for chunk in get_gemini_response(
                    input_text, pdf_content, skill_improve_prompt):
                response_text += chunk
                placeholder.write(response_text)

        # st.write(response)
    else:
        st.write("Please upload the PDF file")


if st.button("Resource to improve"):
    if uploaded_file is not None:
        st.subheader("The Response is:")
        with st.spinner("Generating response...."):
            placeholder = st.empty()
            response_text = ""
            pdf_content = input_pdf_setup(uploaded_file)

            for chunk in get_gemini_response(
                    input_text, pdf_content, resource_prompt):
                response_text += chunk
                placeholder.write(response_text)

        # st.write(response)
    else:
        st.write("Please upload the PDF file")
