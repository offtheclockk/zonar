from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import model_clock, model_user
from flask_app.models.model_user import User
from flask_app.models.model_clock import Clock
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

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

          return redirect('/dashboard')

@app.route('/process/edit_clock', methods=['POST'])
def process_edit_clock():
          print(request.form)
          is_valid = model_clock.Clock.validate_clock(request.form)
          
          if not is_valid:
                    id=request.form['id']
                    return redirect(f'/edit/{id}')
          data = {
                    **request.form,
                    "user_id": session['uuid']
          }

          clock_id = model_clock.Clock.update_one(data)

          return redirect('/dashboard')

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

@app.route('/clocks/<int:id>')
def show(id):
          data = {
                    'id':session['uuid']
          }
          clock = Clock.get_content(id=id)
          user = User.get_one(data)
          print(user)
          return render_template("clocks.html", clock = clock, user = user)

@app.route('/edit/<int:id>')
def editclock(id):
          if 'uuid' not in session:
                    return redirect('/')
          clock = Clock.get_content(id=id)
          if session['uuid'] != clock.user_id:
                    flash('Stop trying to mess with my page!', 'error_dfwm')
                    return redirect('/')
          data = {
                    'id':session['uuid']
          }
          user = User.get_one(data)
          return render_template("edit.html", clock = clock, user = user)

@app.route('/delete/<int:id>')
def delete(id):
          if 'uuid' not in session:
                    return redirect('/')
          clock = Clock.get_content(id=id)
          if session['uuid'] != clock.user_id:
                    flash('Stop trying to mess with my page!', 'error_dfwm')
                    return redirect('/')
          data = {
                    "id":clock.id
          }
          clock = Clock.delete_one(data)
          return redirect("/dashboard")