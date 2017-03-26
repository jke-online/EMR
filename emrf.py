# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, g
import sqlite3
app = Flask(__name__)
app.database = "main.db"

@app.route('/')
def home():
    g.db = connect_db()
    cur = g.db.execute("SELECT * from Info")
    profile = [dict(User=row[0], Institucion=row[1], Puesto=row[2], Correo=row[3], Tel=row[4], Direccion=row[5]) for row in cur.fetchall()]
    cur = g.db.execute("SELECT * from patientlist")
    patientdata = [dict(Id=row[0], Name=row[1], Tutor=row[2], Bday=row[3], Sex=row[4], Genero=row[5], Mail=row[6], Phone=row[7], Academico=row[8], Motivo=row[9], Sintomas=row[10],) for row in cur.fetchall()]
    cur = g.db.execute("SELECT * from Citas")
    Citas = [dict(Hora=row[1], Paciente=row[2]) for row in cur.fetchall()]
    return render_template("Index.html", profile=profile, patientdrop=patientdata, Citas=Citas)

@app.route('/profile', methods=['POST'])
def profile():
    useri = request.form['Useri']
    institucioni = request.form['Institucioni']
    puestoi = request.form['Puestoi']
    correoi = request.form['Correoi']
    teli = request.form['Teli']
    direccioni = request.form['Direccioni']
    g.db = connect_db()
    cur = g.db.execute("UPDATE Info SET User = (?), Institucion = (?), Puesto = (?), Correo = (?), Tel = (?), Direccion = (?)", (useri, institucioni, puestoi, correoi, teli, direccioni,))
    g.db.commit()
    return home()

@app.route('/pacientes')
def pacientes():
    g.db = connect_db()
    cur = g.db.execute("SELECT * from patientlist")
    patientdata = [dict(Id=row[0], Name=row[1], Tutor=row[2], Bday=row[3], Sex=row[4], Genero=row[5], Mail=row[6], Phone=row[7], Academico=row[8], Motivo=row[9], Sintomas=row[10],) for row in cur.fetchall()]
    return render_template("pacientes.html", patientdrop=patientdata )

@app.route('/newpatienth', methods=['POST'])
def newpatienth():
    namei = request.form['namei']
    tutori = request.form['tutori']
    bdayi = request.form['bdayi']
    sexoi = request.form['sexi']
    generoi = request.form['generoi']
    phonei = request.form['phonei']
    maili = request.form['maili']
    academi = request.form['academi']
    motivoi = request.form['motivoi']
    sintomasi = request.form['sintomasi']
    g.db = connect_db()
    cur = g.db.execute("INSERT INTO patientlist VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", ( namei, tutori, bdayi, sexoi, generoi, maili, phonei, academi, motivoi, sintomasi,))
    g.db.commit()
    return home()

@app.route('/newpatient', methods=['POST'])
def newpatient():
    namei = request.form['namei']
    tutori = request.form['tutori']
    bdayi = request.form['bdayi']
    sexoi = request.form['sexi']
    generoi = request.form['generoi']
    phonei = request.form['phonei']
    maili = request.form['maili']
    academi = request.form['academi']
    motivoi = request.form['motivoi']
    sintomasi = request.form['sintomasi']
    g.db = connect_db()
    cur = g.db.execute("INSERT INTO patientlist VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", ( namei, tutori, bdayi, sexoi, generoi, maili, phonei, academi, motivoi, sintomasi,))
    g.db.commit()
    return pacientes()

@app.route('/deletepatient', methods=['POST'])
def deletepatient():
    g.db = connect_db()
    g.db.execute('DELETE FROM patientlist WHERE id = ?', [request.form['patient_to_delete']])
    g.db.commit()
    return pacientes()

@app.route('/appointment', methods=['POST'])
def appointment():
    fecha = request.form['fecha']
    hora = request.form['hora']
    paciente = request.form['paciente']
    g.db = connect_db()
    cur = g.db.execute("INSERT INTO Citas VALUES (?, ?, ?)", ( fecha, hora, paciente,))
    g.db.commit()
    return home()

def connect_db():
    return sqlite3.connect(app.database)

if __name__ == "__main__":
    app.run()
