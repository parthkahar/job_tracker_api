import streamlit as st
import requests
import ollama

API_URL="http://localhost:8000"

st.title=("Job Application Tracker")
st.write("Track all your job application in one place")

st.subheader("My applications")
response=requests.get(f"{API_URL}/applications")
jobs=response.json().get("data", [])

if jobs:
    st.dataframe(jobs)

else:
    st.info("No applications yet. add One Belowww!!!")

st.divider()
st.subheader("+ add new application")
                

with st.form("add_job_form"):
    company=st.text_input("Company Name")
    role = st.text_input("Job Title")
    status =st.selectbox("status",["applied","interview","offer","rejected"])
    submitted =st.form_submit_button("Add Application")

    if submitted:
        if company and role:
            response =requests.post(
                f"{API_URL}/applications",
                params={
                    "company_name":company,
                    "job_title":role,
                    "status": status
                }
            )

            if response.status_code==200:
                st.success("Application added!")
                st.rerun()

            else:
                st.error("Something Went Wrong")
        else:
            st.warning("please fill company name and job title")            
7


st.divider()
st.subheader(" JD Analyser")


jd_text=st.text_area("paste job description here",height =200)

analyse_btn=st.button("analyse jd")

if analyse_btn:
    if jd_text.strip()=="":
        st.warning("bro enter something ")

    else:
        response=ollama.chat(
            model="llama3.2:3b",
            messages=[{

            "role":"user",
            "content": f"""
            Extract from this job description:
            1. Required skills as a list
            2. Nice to have skills as a list
            3. Fit score out of 10 for a Python backend developer

            Return JSON only. No extra text. No explanation.

            Job Description:
            {jd_text}
            """}
            ]
        )
            
        st.subheader("analysis Result")
        st.markdown(response["message"]["content"])

        st.download_button( 
            label="Download Analysis",
            data=response["message"]["content"],
            file_name="jd.txt"
        )

st.divider()
st.subheader("📝 Cover Letter Generator")

cover_jd =st.text_area("Paste Job Description",height=200)
background=st.text_area("write something about yourself")


generator=st.button("Generate Cover Letter")


if generator:
    if cover_jd.strip() == "" or background.strip() == "":
        st.warning("bro i think you are missing something input please check it")

    else:
        response = ollama.chat(
            model="llama3.2:3b",
            messages=[
                {
                    "role": "user",
                    "content": f"""
You are a professional cover letter writer.
Based on this job description and candidate background, 
write a professional cover letter.
Maximum 50 words. Be concise and impactful.

Job Description: {cover_jd}
Candidate Background: {background}

Write only the cover letter. No explanation.
"""
                }
            ]
        )

        st.subheader("Your Cover Letter")
        st.markdown(response["message"]["content"])

        st.download_button(
            label="Download Cover Letter",
            data=response["message"]["content"],
            file_name="cover_letter.txt"
        )


