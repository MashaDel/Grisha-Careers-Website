from flask import Flask,render_template,jsonify,request
from database import load_jobs_from_db,load_job_from_db,add_application_to_db,status



app=Flask(__name__)

#_Authorization block _________________________________________________________________________
@app.route("/login")
def login_page():
  return render_template("login_form.html")
  

@app.route("/register")
def register_page():
  return render_template("register_form.html")


@app.route("/login/apply", methods=["post"])
def login_done():
  data=request.form.to_dict(flat=False)
  jobs=load_jobs_from_db()
  print(data,type(data))
  #add_login_email_to_db(data)
  return render_template("login_submitted.html",
                         jobs=jobs,
                         a=data)


@app.route("/register/apply", methods=["post"])
def register_done():
  data=request.form.to_dict(flat=False)
  jobs=load_jobs_from_db()
  print(data,type(data))
  #add_login_email_to_db(data)
  return render_template("user_page.html",
                         a=data,
                         new_name=data["new_name"][0],
                         jobs=jobs)

@app.route("/user")
def user_page():
  jobs=load_jobs_from_db()
  return render_template("user_page.html",
                         jobs=jobs)


@app.route("/status/<name>/<mail>")
def status_page(name,mail):
  data=status(name,mail)
  #res=status(name,mail)
  return render_template("status_page.html",
                         data=data)





  
@app.route("/")
def hello_grisha():
  jobs=load_jobs_from_db()
  return render_template("home.html",
                         jobs=jobs)


@app.route("/api/jobs")
def list_jobs():
  jobs=load_jobs_from_db()
  return jsonify(jobs)


  
@app.route("/job/<id>")
def show_job(id):
  job=load_job_from_db(id)
  if not job:
    return "Not Found", 404
    
  return render_template("jobpage.html",
                         job=job )


@app.route("/api/job/<id>")
def show_job_json(id):
  job=load_job_from_db(id)
  return jsonify(job)
  


@app.route("/job/<id>/apply", methods=["post"])
def apply_to_job(id):
  id=int(id)
  data=request.form.to_dict(flat=False)
  dt=request.form
 # print('data=',data,"id=",id,"data['linkedin_url']=",data ["linkedin_url"][0],'type(data)=',type(data),'type(dt)=',type(dt),'dt=',dt,sep='\n')
  job=load_job_from_db(id)
  add_application_to_db(id,data)
  return render_template("application_submitted.html",
                          application=data,
                          job=job,
                          data=data)

  

  
if __name__ == "__main__":
  app.run(host="0.0.0.0",debug=True)
  