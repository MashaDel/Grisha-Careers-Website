from flask import Flask,render_template,jsonify,request
from database import load_jobs_from_db,load_job_from_db,add_application_to_db,status,add_user_to_db,autorization_user, select_user,select_user_all,login_user,applications



app=Flask(__name__)

#______________LOGIN_____________________________________________________________
@app.route("/login")
def login_page():
  return render_template("login_form.html")




@app.route("/login/apply", methods=["post"])
def login_done():
  data=request.form.to_dict(flat=False)
  mail=data['email'][0]
  parol=data['password'][0]
  if login_user(mail,parol)==None:
    return render_template("login_wrong.html")
  else:
    user_info=select_user(mail)
  return render_template("login_submitted.html",
                         name=user_info["full_name"],
                         mail=user_info["email"],
                         a=user_info
                         )

#________REGISTER_______________________________
@app.route("/register")
def register_page():
  return render_template("register_form.html")




@app.route("/register/apply", methods=["post"])
def register_done():
  data=request.form.to_dict(flat=False)
  print(data,type(data),
        data['new_name'][0],
        data['new_email'][0],type(data['new_email'][0]),sep='\n')
  name=data['new_name'][0]
  mail=data['new_email'][0]
  parol=data['new_password'][0]
  #print(autorization_user(name,mail,parol))
  if autorization_user(name,mail,parol)!=None:
    return render_template("register_wrong.html")
  else:  
    add_user_to_db(name,mail,parol)
  return render_template("register_submitted.html",
                         a=data,
                         new_name=data["new_name"][0],
                         new_mail=data['new_email'][0]
                         )


#_________USER-PAGE____________________________________________________________
@app.route("/<name>/<mail>")
def user_page(name,mail):
  jobs=load_jobs_from_db()
  user_info=select_user(mail)
  name=user_info['full_name']
  mail=user_info['email']
  return render_template("user_page.html",
                         jobs=jobs,
                         name=name,
                         mail=mail
                        )




@app.route("/job/<name>/<mail>/<id>")
def show_job(name,mail,id):
  job=load_job_from_db(id)
  user_info=select_user(mail)
  u_name=user_info['full_name']
  u_mail=user_info['email']
  if not job:
    return "Not Found", 404
  return render_template("jobpage.html",
                         job=job,
                         u_name=u_name,
                         u_mail=u_mail
                        )




@app.route("/<name>/<mail>/application")
def user_status(name,mail):
  user_info=select_user(mail)
  u_name=user_info['full_name']
  u_mail=user_info['email']
  table=applications(name,mail)
  if table==None:
    return render_template("none_application.html",
                           u_name=user_info['full_name'],
                           u_mail=user_info['email']
                          )
  else:
    a=['id']
    for i in table.keys():
      a.append(i)
    name_col=a
    table_value=table.values()
    len_table=len(table)
    print(type(table))
    return render_template("status_page.html",
                          table=table,
                          u_name=u_name,
                          col=name_col,
                          table_value=table_value,
                          len=len
                            )







@app.route("/")
def hello_grisha():
  jobs=load_jobs_from_db()
  return render_template("home.html",
                         jobs=jobs)


@app.route("/api/jobs")
def list_jobs():
  jobs=load_jobs_from_db()
  return jsonify(jobs)


  


@app.route("/api/job/<id>")
def show_job_json(id):
  job=load_job_from_db(id)
  return jsonify(job)
  


@app.route("/job/<id>/<name>/<mail>/apply", methods=["post"])
def apply_to_job(id,name,mail):
  job=load_job_from_db(id)
  data=request.form.to_dict(flat=False)
  dt=request.form
  user_info=select_user(mail)
  u_name=user_info['full_name']
  u_mail=user_info['email']
  job=load_job_from_db(id)
  add_application_to_db(id,data)
  return render_template("application_submitted.html",
                          application=data,
                          job=job,
                          data=data,
                          u_name=u_name,
                          u_mail=u_mail
                        )

  










  
if __name__ == "__main__":
  app.run(host="0.0.0.0",debug=True)
  