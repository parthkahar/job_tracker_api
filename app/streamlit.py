import streamlit as st
import requests

API_URL="http://localhost:8000"

st.tittle=("Job Application Tracker")
st.write("Track all your job application in one place")

st.subheader("My applications")
response=requests.get(f"{API_URL}/applications")
jobs=response.json()

if jobs:
    st.dataframe(jobs)

else:
    st.info("No applications yet. add One Belowww!!!")


                