from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)  
app.secret_key = 'keep it secret, keep it safe'
from flask_bcrypt import Bcrypt

DATABASE_SCHEMA = 'zonar'