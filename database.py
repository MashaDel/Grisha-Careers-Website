from sqlalchemy import create_engine,text
import os

db_connection_string = os.environ["DB_CONNECTION_STRING"]
#"mysql+pymysql://zn6vt4paz14yv5e4puws:pscale_pw_1gKCjEvtA9fKqMYhkzDMdEg4eJJ4JvtCm9ePfyTFz3i@ap-south.connect.psdb.cloud/grishacareers?charset=utf8mb4"

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
    jobs=[]
    for row in result.all():
      jobs.append(row._mapping)
    return jobs 
  

 
  