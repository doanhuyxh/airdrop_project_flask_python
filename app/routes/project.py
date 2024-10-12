
from flask import Flask, jsonify, request, redirect, url_for, render_template, Blueprint


project = Blueprint('project', __name__)

@project.route('/project', methods=['GET'])
def index():
    return render_template('project/index.html')

@project.route('/project/create', methods=['GET'])
def create():
    return render_template('project/create.html')