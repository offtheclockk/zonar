from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models import model_clock, model_user
from flask_app.models.model_user import User
from flask_app.models.model_event import Event
from flask_app.models.model_clock import Clock

@app.route('/')         
def landing_page():
          if 'uuid' in session:
                    return redirect('/dashboard')
          return render_template("landing_page.html")

@app.route('/register')         
def register_page():
          if 'uuid' in session:
                    return redirect('/dashboard')
          return render_template("register.html")

@app.route('/dashboard')
def dashboard():
          if 'uuid' not in session:
                    return redirect('/')
          data={
                    'id':session['uuid']
          }
          user = User.get_one(data)
          events = Event.get_all_events()
          return render_template("dashboard.html", user = user, events = events)

@app.route('/process', methods=['POST'])
def process_results():
          if not User.validate_user(request.form):
                    return redirect('/')
          User.add(request.form)
          session['email'] = request.form['email']
          return redirect("/success")

@app.route('/process/create_clock', methods=['POST'])
def process_create_clock():
          print(request.form)
          is_valid = model_clock.Clock.validate_clock(request.form)
          
          if not is_valid:
                    return redirect('/dashboard')
          data = {
                    **request.form,
                    "user_id": session['uuid']
          }

          clock_id = model_clock.Clock.create_clock(data)

          return redirect('/myclocks')

@app.route('/myclocks')
def myclocks():
          if 'uuid' not in session:
                    return redirect('/')
          data={
                    'id':session['uuid']
          }
          user = User.get_one(data)
          clocks = Clock.get_user_clocks()
          return render_template("myclocks.html", user = user, clocks = clocks)
