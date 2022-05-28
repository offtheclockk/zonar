from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import model_event, model_user
from flask_app.models.model_user import User
from flask_app.models.model_event import Event
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/process/create_event', methods=['POST'])
def process_create_event():
          print(request.form)
          is_valid = model_event.Event.validate_event(request.form)
          
          if not is_valid:
                    return redirect('/create/event')
          data = {
                    **request.form,
                    "user_id": session['uuid']
          }

          event_id = model_event.Event.create_event(data)

          return redirect('/dashboard')

@app.route('/process/edit_event', methods=['POST'])
def process_edit_event():
          print(request.form)
          is_valid = model_event.Event.validate_event(request.form)
          
          if not is_valid:
                    id=request.form['id']
                    return redirect(f'/edit/{id}')
          data = {
                    **request.form,
                    "user_id": session['uuid']
          }

          event_id = model_event.Event.update_one_event(data)

          return redirect('/dashboard')

@app.route('/myevents')
def myevents():
          if 'uuid' not in session:
                    return redirect('/')
          data={
                    'id':session['uuid']
          }
          user = User.get_one(data)
          events = Event.get_user_events()
          return render_template("myevents.html", user = user, events = events)

@app.route('/create/event')
def create_event():
          if 'uuid' not in session:
                    return redirect('/')
          data={
                    'id':session['uuid']
          }
          user = User.get_one(data)
          events = Event.get_all_events()
          return render_template("create_event.html", user = user, events = events)

@app.route('/events/<int:id>')
def show(id):
          data = {
                    'id':session['uuid']
          }
          event = Event.get_event_content(id=id)
          user = User.get_one(data)
          print(user)
          return render_template("events.html", event = event, user = user)

@app.route('/edit_event/<int:id>')
def editevent(id):
          if 'uuid' not in session:
                    return redirect('/')
          event = Event.get_event_content(id=id)
          if session['uuid'] != event.user_id:
                    flash('Stop trying to mess with my page!', 'error_dfwm')
                    return redirect('/')
          data = {
                    'id':session['uuid']
          }
          user = User.get_one(data)
          return render_template("edit.html", event = event, user = user)

@app.route('/delete/<int:id>')
def delete(id):
          if 'uuid' not in session:
                    return redirect('/')
          event = Event.get_event_content(id=id)
          if session['uuid'] != event.user_id:
                    flash('Stop trying to mess with my page!', 'error_dfwm')
                    return redirect('/')
          data = {
                    "id":event.id
          }
          event = Event.delete_one_event(data)
          return redirect("/dashboard")