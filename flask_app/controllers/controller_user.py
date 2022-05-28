from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import model_user
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/user/process_login', methods=['POST'])
def process_login():
          user = model_user.User.get_one_email(email=request.form['user_input'])
          is_valid = True

          if len(request.form['user_input']) < 1:
                    flash("Must input an email address", "user_input")
                    is_valid = False

          if len(request.form['pw']) < 1:
                    flash("Must input a password", "pw")
                    is_valid = False

          if user:
                    if not bcrypt.check_password_hash(user.hash_pw, request.form['pw']):
                              is_valid = False
                              flash("Invalid Credentials", "user_input")

          if not is_valid:
                    return redirect('/')

          session['uuid'] = user.id
          return redirect('/dashboard')


@app.route('/user/create', methods=['POST'])
def create_user():
          print(request.form)
          is_valid = model_user.User.validate_user(request.form)
          if not is_valid:
                    return redirect('/register')

          hash_pw = bcrypt.generate_password_hash(request.form['pw'])

          data = {
                    **request.form,
                    'hash_pw': hash_pw
          }

          user_id = model_user.User.create(data)
          session['uuid'] = user_id

          return redirect('/dashboard')

@app.route('/logout')
def logout():
          session.pop('uuid')
          return redirect('/')