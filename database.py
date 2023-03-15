from sqlalchemy import create_engine,text,insert
import os

db_connection_string = os.environ["DB_CONNECTION_STRING"]


engine = create_engine(
  db_connection_string,
  connect_args={
    "ssl": {
      "ssl_ca": "/etc/ssl/cert.pem"
        }
    })


def load_jobs_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from jobs"))
    column_names=result.keys()
    jobs=[]
    for row in result.all():
      jobs.append(dict(zip(column_names,row)))
    return jobs

  
def load_job_from_db(id):
  with engine.connect() as conn:
    result = conn.execute(
      text(f"SELECT * FROM jobs WHERE id ={id}"))
    rows=[]
    for row in result.all():
      rows.append(row._mapping)
    if len(rows)==0:
      return None
    else:
      return [dict(row) for row in rows][0]
      

#first variant of function sqlalchemy 2.0.4
def add_application_to_db(job_id, data):
  a=data["full_name"][0]
  b=data['email'][0]
  c=data ["linkedin_url"][0]
  d=data['education'][0]
  e=data['work_experience'][0]
  f=data['resume_url'][0]
  g="not viewed"
  with engine.connect() as conn:
    conn.execute(text(f"INSERT INTO applications (job_id, full_name, email, linkedin_url, education, work_experience, resume_url,status) VALUES ({job_id}, '{a}','{b}','{c}','{d}', '{e}', '{f}','{g}')"))


#second variant of function sqlalchemy 1.4.6
def add_application_to_db_1(job_id, data):
  with engine.connect() as conn:
    query = text(f"INSERT INTO applications (job_id, full_name, email, linkedin_url, education, work_experience, resume_url,status) VALUES (:job_id, :full_name, :email, :linkedin_url, :education, :work_experience, :resume_url)")
    conn.execute(query, 
                 job_id=job_id, 
                 full_name=data['full_name'],
                 email=data['email'],
                 linkedin_url=data['linkedin_url'],
                 education=data['education'],
                 work_experience=data['work_experience'],
                 resume_url=data['resume_url']
                 )
                    


def status(name,mail):
  with engine.connect() as conn:
    result = conn.execute(
    text(f"SELECT * FROM applications WHERE full_name={name} and email={mail}"))
    rows=[]
    for i in result.all():
      rows.append(i._mapping)
      if len(rows)==0:
        return None
      else:
        return rows
        #return [dict(row) for row in rows][0]
        
                  
    





             
    
  

