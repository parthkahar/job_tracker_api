import streamlit as st
import requests
import ollama
import fitz

API_URL="http://localhost:8000"






st.divider()
st.sidebar.title("🚀 AI Career Assistant")
page_navigator=st.sidebar.selectbox("Navigation",["dashboard","applications","resume","ai tools"])

if page_navigator == "resume":
    st.divider()
    st.subheader("Upload Your Resume")

    resume = st.file_uploader("Upload your PDF ", type =["pdf"])

    resume_text=""
    if resume is not None:
        with fitz.open(stream=resume.read(),filetype="pdf") as doc:
            for page in doc:
                resume_text += page.get_text()

        st.success("resume uploaded successfully")
        #st.text_area(
        #   "extracted resume text",
        #  resume_text,
        #  height =300
    #)

elif page_navigator == "dashboard":

    st.header("📊 Dashboard")

    response = requests.get(f"{API_URL}/applications")
    jobs = response.json().get("data", [])

    applied_count = 0
    interview_count = 0
    offer_count = 0
    rejected_count = 0

    for job in jobs:
        if job["status"] == "applied":
            applied_count += 1

        elif job["status"] == "interview":
            interview_count += 1

        elif job["status"] == "offer":
            offer_count += 1

        elif job["status"] == "rejected":
            rejected_count += 1

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Total Applications", len(jobs))
    col2.metric("🟢Applied", applied_count)
    col3.metric("🟡Interview", interview_count)
    col4.metric("🔵Offer", offer_count)
    col5.metric("🔴Rejected", rejected_count)

    st.metric( label="Total Applications", value=len(jobs) )
    st.dataframe(jobs)
    #st.table(jobs)



elif page_navigator =="applications":
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



    st.divider()
    st.subheader("🗑️ Delete Job")

    delete_id=st.number_input("Enter Job id to delete",min_value=1,step=1)
    delete_btn =st.button("Delete Job")

    if delete_btn:
        response=requests.delete(f"{API_URL}/applications/{int(delete_id)}")

        if response.status_code==200:
            st.success("Application Deleted!!!")
            st.rerun()

        else:
            st.error("something went wrong")


    st.divider()
    st.subheader("Job id Satus updater")

    job_id=st.number_input("enter your JOB ID",min_value=1,step=1)

    job_status=st.selectbox("status",
                            ["applied","interview","offer","rejected"],
                            key="update_status_select"
                            )

    update_btn=st.button("update Job Status")


    if update_btn:
        if job_id <0:
            st.warning("enter Valid Job ID")
        else:
            response=requests.patch(f"{API_URL}/applications/{int(job_id)}/status", 
                                    json={"status": job_status}
            )

            if response.status_code==200:
                st.success("application Updated")
                st.rerun()

            else:
                st.error("id doesnot exists ")


elif page_navigator== "ai tools":

    st.divider()
    st.subheader("Followup Generator")

    company_name=st.text_input("company name")
    job_title=st.text_input("Job title pls")
    status=st.selectbox("status",
                        ["applied","interview","offer","rejected"],
                        key="followup_status_select"
                        )
    notes_=st.text_area("notes")

    follow_up_btn=st.button("followup")

    if follow_up_btn:
        response=requests.post(
            f"{API_URL}/ai/followup",
            json={

                "company_name": company_name,
                "job_title": job_title,
                "status": status,
                "notes": notes_
            }
        )

        if response.status_code ==200:
            result = response.json()
            st.markdown(result["followup"])

        else:
            st.error("failed:(")



    


    st.divider()
    st.subheader("📝 Cover Letter Generator")

    cover_jd =st.text_area("Paste Job Description",height=200)
    #background=st.text_area("write something about yourself")


    generator=st.button("Generate Cover Letter")


    if generator:
        if cover_jd.strip() == "":
            st.warning("bro i think you are missing something input please check it")

        elif not resume_text:
            st.warning("i think resume is missing buddy")

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
                    Candidate Background: {resume_text}

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










    st.divider()
    st.subheader(" JD Analyser")


    jd_text=st.text_area("paste job description here",height =200)

    analyse_btn=st.button("analyse jd")

    if analyse_btn:
        if jd_text.strip()=="":
            st.warning("bro enter something ")

        elif not resume_text:
            st.warning("please Upload your resume first ")
        else:
            response=ollama.chat(
                model="llama3.2:3b",
                messages=[{

                "role":"user",
                "content":f"""
                You are a career advisor.
                Compare this job description against the candidate's resume
                dont give me big big output just give me short and simple output

                Job Description: {jd_text}

                Candidate Resume: {resume_text}

                Return:
                1. Skills candidate HAS that match the JD in short
                2. Skills candidate is MISSING
                3. Fit score out of 10 based on actual resume
                4. give candidate a reality check that he or she should work on the missing skill
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













