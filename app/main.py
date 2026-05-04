from fastapi import FastAPI
from db import get_cursor
from pydantic import BaseModel
from ai import generate_followup

app=FastAPI()


@app.get("/")
def home():
    return{"message":"Job Tracker API is running"}

@app.get("/test-db")

def test_db():
    conn,cursor=get_cursor()
    cursor.execute("SELECT 1;")
    result=cursor.fetchone()
    cursor.close()
    conn.close()
    return{"db_result":result}

@app.post("/applications")
def create_application(company_name: str, job_title: str, status: str):
    conn,cursor=get_cursor()

    query="""
    INSERT INTO applications (company_name, job_title, status)
    VALUES(%s,%s,%s)"""
    cursor.execute(query, (company_name, job_title, status)) 

    conn.commit()


    cursor.close()
    conn.close()

    return {"message":"Application added succesfully"}

@app.get("/applications")
def view_all_application():
    conn,cursor=get_cursor()
    query="SELECT * FROM applications"
    cursor.execute(query)

    data=cursor.fetchall()

    cursor.close()
    conn.close()

    return {"data":data}


@app.get("/applications/search")
def search_applications(company: str = None, role: str = None, status: str = None):
    conn, cursor = get_cursor()

    query = "SELECT * FROM applications WHERE 1=1"
    values = []

    if company:
        query += " AND company_name = %s"
        values.append(company)

    if role:
        query += " AND job_title = %s"
        values.append(role)

    if status:
        query += " AND status = %s"
        values.append(status)

    cursor.execute(query, tuple(values))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return {"data": rows}


@app.get("/applications/{id}")
def get_application_by_id(id:int):

    conn,cursor=get_cursor()
    query="SELECT * FROM applications where id =%s"
    cursor.execute(query,(id,))

    row=cursor.fetchone()
    
    cursor.close()
    conn.close()

    if not row:
        return {"message": "Application not found"}

    return row





@app.delete("/applications/{id}")
def delete_application(id:int):

    conn,cursor=get_cursor()
    query="DELETE FROM applications WHERE id =%s"
    cursor.execute(query,(id,))
    conn.commit()

    if cursor.rowcount==0:
        cursor.close()
        conn.close()

        return{"message":"no application found"}
    cursor.close()
    conn.close()

    return{"message":"application deleted"}


class StatusUpdate(BaseModel):
    status:str


@app.patch("/applications/{id}/status")

def update_status(id:int,data:StatusUpdate):
    conn,cursor=get_cursor()

    allowed = ["applied", "interview", "offer", "rejected"]

    if data.status not in allowed:
        cursor.close()
        conn.close()
        return{"message":"INVALID STATUS"}
    

    query = "SELECT * FROM applications WHERE id = %s"
    cursor.execute(query, (id,))

    row=cursor.fetchone()


    if not row:
        cursor.close()
        conn.close()
        return {"message": "Application not found"}
    

    query="""
    UPDATE applications 
    SET status=%s
    WHERE id =%s
    """
    cursor.execute(query, (data.status, id))
    conn.commit()

    cursor.execute("SELECT * FROM applications WHERE id = %s", (id,))
    updated = cursor.fetchone()

    cursor.close()
    conn.close()

    return updated



class IneractionCreate(BaseModel):
    type:str
    notes:str

@app.post("/applications/{id}/interactions")

def create_interaction(id:int,data:IneractionCreate):
    conn,cursor=get_cursor()

    #aana thi khabar pade che ke pehele id che ke nahi agar nahi to sidhu  message not found kari dev return\
    query="SELECT * FROM applications WHERE id =%s"
    cursor.execute(query,(id,))
    row=cursor.fetchone()

    if not row:
        cursor.close()
        conn.close()
        return{"message":"Application NOt Founddddd"}
    


    query="""
    INSERT INTO interactions(application_id,type,notes)
    VALUES(%s,%s,%s)
    """
    cursor.execute(query, (id, data.type, data.notes))
    conn.commit()

    interaction_id=cursor.lastrowid

    query="SELECT * FROM interactions WHERE id =%s"
    cursor.execute(query,(interaction_id,))
    new_interaction=cursor.fetchone()

    cursor.close()
    conn.close()

    return new_interaction


@app.get("/applications/{id}/interactions")
def get_interactions(id:int):
    conn,cursor =get_cursor()

    query="SELECT * FROM applications WHERE id =%s"

    cursor.execute(query, (id,))
    row=cursor.fetchone()

    if not row:
        cursor.close()
        conn.close()

        return{"message":"Application Not Foundd"}


    query = "SELECT * FROM interactions WHERE application_id = %s"
    cursor.execute(query, (id,))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return {"data": rows}





class ApplicationUpdate(BaseModel):
    company_name: str
    job_title : str
    status: str
    applied_date: str
    notes: str


@app.put("/applications/{id}")

def update_aplication(id:int, data:ApplicationUpdate):
    conn,cursor=get_cursor()

    allowed_status=["applied","interview","offer","rejected"]


    if data.status not in allowed_status:
        cursor.close()
        conn.close()
        return{'message':"invalid status"}
    


    query = """
    UPDATE applications
    SET company_name = %s,
        job_title = %s,
        status = %s,
        applied_date = %s,
        notes = %s,
        updated_at = NOW()
    WHERE id = %s
    """



    cursor.execute(
        query,
        (
            data.company_name,
            data.job_title,
            data.status,
            data.applied_date,
            data.notes,
            id
        )
    )
    conn.commit()

    query = "SELECT * FROM applications WHERE id = %s"
    cursor.execute(query, (id,))
    updated_row = cursor.fetchone()

    cursor.close()
    conn.close()

    return updated_row

class FollowupRequest(BaseModel):
    company_name:str
    job_title:str
    status:str
    notes:str


@app.post("/ai/followup")
def create_followup(data:FollowupRequest):
    followup=generate_followup(
        data.company_name,
        data.job_title,
        data.status,
        data.notes
    )


    return {"followup":followup}