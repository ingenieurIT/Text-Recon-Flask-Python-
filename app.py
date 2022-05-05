import os
from flask import Flask, render_template, request, url_for
from reconApp import ocr_core
from flask_sqlalchemy import SQLAlchemy
import psycopg2

UPLOAD_FOLDER = '/static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgresql2021@localhost/postgres'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'myapp'

db = SQLAlchemy(app)
bd_login = {'Admin': 'd02021@21', 'First': 'fst@2021'}


class utilisateurs(db.Model):  # utiliser la tables Utilisateurs de la BD
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(30), nullable=False)
    mdp = db.Column(db.String(10), nullable=False)

    def __init__(self, login, mdp):
        self.login = login
        self.mdp = mdp


class base_donnees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    donnees = db.Column(db.String(50000), nullable=False)

    def __init__(self, donnees):
        self.donnees = donnees


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form["logind"]
        mdp = request.form["mdpd"]
        entry = utilisateurs(login, mdp)
        db.session.add(entry)
        db.session.commit()

    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    utilisateur = request.form['login']
    mdp = request.form['mdp']
    if utilisateur not in bd_login:
        return render_template('index.html', info='Utilisateur Incorrecte')
    else:
        if bd_login[utilisateur] != mdp:
            return render_template('index.html', msg='mot de passe invalide')
        else:
            return render_template('upload.html', user=utilisateur)


@app.route('/load', methods=['GET', 'POST'])  # fonction pour afficher les element de la BD
def show_data():
    show_datas = base_donnees.query.all()
    return render_template('load.html', show_datas=show_datas)


@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('upload.html', msg='aucun fichier selectionne')
        file = request.files['file']
        if file.filename == '':
            return render_template('upload.html', msg='aucun fichier selectionne')

        if file and allowed_file(file.filename):
            file.save(os.path.join(os.getcwd() + UPLOAD_FOLDER, file.filename))
            result_recon = ocr_core(file)
            return render_template('upload.html',
                                   msg='operation realisee avec succes',
                                   result_recon=result_recon,
                                   img_src=UPLOAD_FOLDER + file.filename)
    elif request.method == 'GET':
        return render_template('upload.html')


@app.route('/enregistrer', methods=['POST'])  # enregistrer dans la BD
def enregistrer():
    if request.method == 'POST':
        donnees = request.form["mytextarea"]
        entry = base_donnees(donnees)
        db.session.add(entry)
        db.session.commit()
        return render_template('upload.html', msg='enregistrement reussi')
    elif request.method == 'GET':
        return render_template('upload.html')


if __name__ == '__main__':
    db.create_all()
    app.run()
