from sqlalchemy import create_engine,text,insert,update
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
      text(f"SELECT * FROM jobs WHERE id ='{id}'"))
    rows=[]
    for row in result.all():
      rows.append(row._mapping)
    if len(rows)==0:
      return None
    else:
      return [dict(row) for row in rows][0]
      

#First variant of function sqlalchemy 2.0.4________________
def add_application_to_db(job_id, data):
  a=data["full_name"][0]
  b=data['email'][0]
  c=data ["linkedin_url"][0]
  d=data['education'][0]
  e=data['work_experience'][0]
  f=data['resume_url'][0]
  g="not viewed"
  with engine.connect() as conn:
    res=conn.execute(text(f"SELECT job_id,full_name,email FROM applications WHERE job_id={job_id} and full_name='{a}' and email='{b}'")).all()
    if len(res)==0:
      conn.execute(text(f"INSERT INTO applications (job_id, full_name, email, linkedin_url, education, work_experience, resume_url,status) VALUES ({job_id}, '{a}','{b}','{c}','{d}', '{e}', '{f}','{g}')"))
      return True
    else:
      return False

      
#Second variant of function sqlalchemy 1.4.6_______________
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
    text(f"SELECT * FROM applications WHERE full_name='{name}' and email='{mail}'"))
    rows=[]
    for i in result.all():
      rows.append(i._mapping)
      if len(rows)==0:
        return None
      else:
        return rows

        
#___ADD -NEW-USER-TO -DB_________________________________________
def add_user_to_db(n,m,p):
  with engine.connect() as conn:
    conn.execute(text(f"INSERT INTO register_user (full_name, email,pasword) VALUES ('{n}','{m}','{p}')"))
  
  
#___________AURORISATION OF USER______________________________
def autorization_user(n,m,p):
  with engine.connect() as conn:
    result = conn.execute(text(f"SELECT * FROM register_user WHERE full_name='{n}' and email='{m}'  and pasword='{p}'"))
    rows=[]
    for i in result.all():
      rows.append(i._mapping)
      if len(rows)==0:
        return None
      else:
        return rows

#__________SELECT -USER______________________________
def select_user(m):
  with engine.connect() as conn:
    result = conn.execute(text(f"SELECT * FROM register_user WHERE email='{m}'"))
    rows=[]
    for i in result.all():
      rows.append(i._mapping)
      if len(rows)==0:
        return None
      else:
        return [dict(row) for row in rows][0]

#__________SELECT-REGISTER-user______________________________
def select_user_all():
  with engine.connect() as conn:
    result = conn.execute(text(f"SELECT * FROM register_user"))
    rows=[]
    for i in result.all():
      rows.append(i._mapping)
      if len(rows)==0:
        return None
      else:
        return [dict(row) for row in rows][0]             
    
  
#__________LOGIN-USER_____________________
def login_user(m,p):
  with engine.connect() as conn:
    result = conn.execute(text(f"SELECT * FROM register_user WHERE email='{m}' and pasword='{p}'"))
    rows=[]
    for i in result.all():
      rows.append(i._mapping)
      if len(rows)==0:
        return None
      else:
        return rows

#_SELECT - APPLICATION____________________________________
def applications(n,m):
  with engine.connect() as conn:
    result = conn.execute(text(f"SELECT title,status FROM applications JOIN jobs on jobs.id=applications.job_id WHERE full_name='{n}' and email='{m}'"))
    rows=[]
    for i in result.all():
      if i not in rows:
        rows.append(i)
    if len(rows)==0:
      return None
    else:
        return [dict(row) for row in rows ]


      
#___APPLICATIONS_ALL_______________________________________________
def applications_all():
  with engine.connect() as conn:
    result = conn.execute(text(f"SELECT title,full_name,email,linkedin_url,education,work_experience,resume_url,status FROM applications JOIN jobs on jobs.id=applications.job_id "))
    rows=[]
    for i in result.all():
      if i not in rows:
        rows.append(i._mapping)
    if len(rows)==0:
      return None
    else:
        return [dict(row) for row in rows ]



#_REJECT-USER____________________________________
def reject(n,m,t):
  with engine.connect() as conn:
    res=conn.execute(text(f"SELECT applications.job_id FROM applications JOIN jobs on jobs.id=applications.job_id WHERE title='{t}'")).first()[0]
    result = conn.execute(text(f"UPDATE applications SET status='reject' WHERE full_name='{n}' and email='{m}' and job_id={res}"))
    return True

    
#_ACCEPT-USER____________________________________
def accept(n,m,t):
  with engine.connect() as conn:
    res=conn.execute(text(f"SELECT applications.job_id FROM applications JOIN jobs on jobs.id=applications.job_id WHERE title='{t}'")).first()[0]
    result = conn.execute(text(f"UPDATE applications SET status='accept' WHERE full_name='{n}' and email='{m}' and job_id={res}"))
    return True

#_NOT_VIEWED-USER____________________________________
def not_viewed(n,m,t):
  with engine.connect() as conn:
    res=conn.execute(text(f"SELECT applications.job_id FROM applications JOIN jobs on jobs.id=applications.job_id WHERE title='{t}'")).first()[0]
    result = conn.execute(text(f"UPDATE applications SET status='not viewed' WHERE full_name='{n}' and email='{m}' and job_id={res}"))
    return True
