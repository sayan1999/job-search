from dotenv import load_dotenv
import os, traceback
import google.generativeai as genai
import streamlit as st
from utils import get_jd, get_resume, get, create_mailto


RESUME_URL = "https://docs.google.com/document/d/1DEzxF0QiqXEyN63EkNvczGZQo8m2vYjD7oFuTBG5tc0/edit?usp=sharing"


def common_ui(jb_type):
    col1, col2, col3, col4 = st.columns(4)
    recruiter = col1.text_input("Recruiter name")
    to = col2.text_input("Recruiter mailid") if jb_type == "cv" else ""
    role = col3.text_input("Role applying for", "Machine learning Engineer")
    companyname = col4.text_input("Company name")
    return recruiter, to, role, companyname


def jd_resume():
    col1, col2 = st.columns(2)
    with col1:
        skills = (
            "\n\nThis is My Resume:\n"
            + st.text_area("Resume", get_resume(RESUME_URL), height=600)
            + "\n" * 3
        )
    with col2:
        jd_link = st.text_input("Job Url")
        st.markdown("OR")
        jd = (
            "\n\nThis is the Job Description:\n"
            + st.text_area("Job Description", get_jd(jd_link), height=600)
            + "\n" * 3
        )
    return skills, jd


def cover_letter_recruiter():
    recruiter, to, role, companyname = common_ui("cv")
    char_is_lim = st.checkbox("Limited Chars")
    if char_is_lim:
        character_lim = st.number_input(min_value=1, max_value=200000, value=5000)
    cv_prompt = (
        st.text_area(
            "Prompt",
            "Write a short concise confident cover letter in {} to {} with below job description for a role as {} at {}, \
highlight my skills that align with job description, avoid unnecessary white space. \
Please mention in LinkedIn id, contact number and email id in the letter. Don't use unnecessary newlines".format(
                str(character_lim) + "characters" if char_is_lim else "300 words",
                recruiter,
                role,
                companyname,
            ),
        )
        + "\n Return only the body of the mail"
    )
    cv_imprv_prompt = (
        st.text_area(
            "Improvement Prompt",
            "{} works at {}. There is a job opening for a {} at {}. I am looking for this role. \
Understand the skills demanded in Job Description and go through the Resume to understand the skills the applicant is having. \
List down the all the Hard skills-keywords the applicant is missing. \
Don't use bullete points. Use comma separated values please.".format(
                recruiter,
                companyname,
                role,
                companyname,
            ),
        )
        + "\n Return only the body of the mail"
    )
    skills, jd = jd_resume()
    if st.button("Generate cover letter"):
        with st.spinner("Generating your cover letter ..."):
            improvement_resp = get(cv_imprv_prompt + skills + jd).content
            st.markdown("Consider adding these to your resume:")
            st.markdown(improvement_resp)
            resp = get(cv_prompt + skills + jd).content
            st.markdown("Cover letter:")
            st.markdown(resp)
        st.link_button("Preview email", create_mailto(to, role, companyname, resp))


def linkedin_referral():
    recruiter, _, role, companyname = common_ui("refer")
    referral_prompt = (
        st.text_area(
            "Prompt",
            "{} works at {}. There is a job opening for a {} at {}. I am looking for this role. \
Create a formal, humble, and polite short linkedin note in 2 lines asking {} for a referral in that position. \
Don't use unnecessary newlines, the note should be in strictly less than 200 characters.".format(
                recruiter, companyname, role, companyname, recruiter
            ),
        )
        + "\n Return only the body of the mail"
    )
    skills, jd = jd_resume()
    if st.button("Generate referral note"):
        with st.spinner("Generating your referral note ..."):
            resp = get(referral_prompt + skills + jd).content
            st.markdown("Referral:")
            st.markdown(resp)


def main():
    try:
        selected_page = st.sidebar.selectbox(
            "Select a page", ["Cover Letter", "LinkedIn Referral"]
        )
        {
            "Cover Letter": cover_letter_recruiter,
            "LinkedIn Referral": linkedin_referral,
        }[selected_page]()
    except Exception as e:
        traceback.print_exc()
        print(e)
        st.error(e)


if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="Job Apply")
    st.title("JOB SEARCH")
    load_dotenv()
    key = st.session_state.get("GOOGLE_API_KEY", "") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        with st.empty():
            st.link_button(
                "Get your Gemini API key",
                "https://makersuite.google.com/app/apikey",
            )
            key = st.text_input("Enter your API key", type="password")
            if key:
                os.environ["GOOGLE_API_KEY"] = key
                st.session_state["GOOGLE_API_KEY"] = key
    main()
