from flask import render_template,request,redirect,Flask,flash,url_for, jsonify
from flask_login import login_required, LoginManager, login_user, logout_user, current_user
from websen import app
from websen.databases.models import db, User, Jabatan, Jadwal, Pegawai, Absen
from datetime import timedelta
import logging, os, string, random, hashlib, datetime
from sqlalchemy import desc
from werkzeug.utils import secure_filename
from websen.views.admin.admin_page import requires_roles,Breadcumb, change_foto, change_password, change_username

@login_required
@requires_roles('pegawai')
def staff_index():
    user_id = current_user.user_id
    pegawai = Pegawai.query.filter_by(user_id=user_id).first()
    urls = str(url_for('staff_index')).split("/")
    urls.remove("")
    urls[0] = "Home"
    breadcumbs = []
    for url in urls:
        breadcumb = Breadcumb()
        breadcumb.name = url.capitalize()
        breadcumbs.append(breadcumb)
    return render_template("staff/dashboard.html", pegawai=pegawai, breadcumbs=breadcumbs)

@login_required
@requires_roles('pegawai')
def staf_profile():
    user_id = current_user.user_id
    if request.method == 'GET':
        pegawai = Pegawai.query.filter_by(user_id=user_id).first()
        urls = str(url_for('staf_profile')).split("/")
        urls.remove("")
        urls[0] = "Home"
        breadcumbs = []
        for url in urls:
            breadcumb = Breadcumb()
            breadcumb.name = url.capitalize()
            breadcumbs.append(breadcumb)
        breadcumbs[0].url = url_for("staff_index")
        breadcumbs[len(breadcumbs)-1].active = True
        return render_template("staff/profile.html", pegawai=pegawai, breadcumbs=breadcumbs)
    if request.method == 'POST':
        user = User.query.get(user_id)
        username = request.form['username']
        res, msg = change_username(username,user)
        if res:
            flash(msg, category="success")
            return redirect(url_for('staf_profile'))
        else:
            flash(msg, category="error")
            return redirect(url_for('staf_profile'))

@login_required
@requires_roles('pegawai')
def staff_ganti_password():
    if request.method == 'POST':
        user_id = current_user.user_id
        old_pass = request.form['old_password']
        new_pass = request.form['password_baru']
        pass_conf = request.form['password_conf']
        res, msg = change_password(old_pass,new_pass,pass_conf,user_id)
        if res:
            flash(msg, category="success")
            return redirect(url_for('staf_profile'))
        else:
            flash(msg, category="error")
            return redirect(url_for('staf_profile'))

@login_required
@requires_roles('pegawai')
def staff_change_foto(pegawai_id):
    res, msg = change_foto(pegawai_id)
    if res:
        flash(msg, category="success")
        return jsonify({"success":"Ganti Foto Berhasil"}),200
    else:
        flash(msg, category="error")
        return jsonify({"error":"Data tidak ditemukan"}), 302

@login_required
@requires_roles('pegawai')
def staf_absen():
    user_id = current_user.user_id
    pegawai = Pegawai.query.filter_by(user_id=user_id).first()
    absens = None
    bulan = None
    tanggal = None
    if request.args.get("bulan"):
        date = request.args.get('bulan')
        bulan = date
        absens = Absen.query.filter_by(pegawai_id=pegawai.id).filter(Absen.tanggal.like("%"+bulan+"%")).all()
    elif request.args.get("tanggal"):
        date = request.args.get('tanggal')
        tanggal = date
        absens = Absen.query.filter_by(pegawai_id=pegawai.id).filter(Absen.tanggal.like("%"+date+"%")).all()
    else:
        absens = Absen.query.order_by(desc(Absen.tanggal)).filter_by(pegawai_id=pegawai.id).all()
    urls = str(url_for('staf_absen')).split("/")
    urls.remove("")
    urls[0] = "Home"
    breadcumbs = []
    for url in urls:
        breadcumb = Breadcumb()
        breadcumb.name = url.capitalize()
        breadcumbs.append(breadcumb)
    breadcumbs[0].url = url_for("staff_index")
    breadcumbs[len(breadcumbs)-1].active = True
    return render_template("staff/absen.html", absens=absens,breadcumbs=breadcumbs)

