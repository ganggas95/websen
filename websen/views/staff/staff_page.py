from flask import render_template,request,redirect,Flask,flash,url_for, jsonify
from flask_login import login_required, LoginManager, login_user, logout_user, current_user
from websen import app
from websen.databases.models import db, User, Jabatan, Jadwal, Pegawai, Absen
from datetime import timedelta
import logging, os, string, random, hashlib, datetime
from sqlalchemy import desc,asc
from werkzeug.utils import secure_filename
from websen.views.admin.admin_page import requires_roles,Breadcumb, change_foto, change_password, change_username
bulan = ["Januari", 
            "Februari", 
            "Maret", 
            "April", 
            "Mei", 
            "Juni",
            "Juli", 
            "Agustus", 
            "September", 
            "Oktober", 
            "November", 
            "Desember"]
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
    now = datetime.datetime.now()
    month = ""
    absens = None
    data_masuk = []
    data_keluar = []
    jumlah_masuk = []
    jumlah_keluar = []
    absen_masuk = []
    absen_keluar = []
    for index in range(len(bulan)):
        if index<9:
            month = "0"+str(index+1)
        else:
            month = str(index+1)
        absens = Absen.query.filter_by(pegawai_id=pegawai.id).filter(Absen.tanggal.like("%"+str(now.year)+"-"+month+"%")).all()
        if len(absens)>0:
            for absen in absens:
                if absen.keluar:
                    jumlah_keluar.append(1)
                if absen.masuk:
                    jumlah_masuk.append(1)
            absen_keluar.append(len(jumlah_keluar))
            absen_masuk.append(len(jumlah_masuk))
        else:
            absen_masuk.append(0)
            absen_keluar.append(0)
    data_keluar.append({
        "label" : "Absen Keluar",
        "backgroundColor" : "blue",
        "borderColor" : "rgba(255,255,255,.55)",
        "data" : absen_keluar
    })
    data_masuk.append({
        "label" : "Absen Masuk",
        "backgroundColor" : "blue",
        "borderColor" : "rgba(255,255,255,.55)",
        "data" : absen_masuk
    })
    date = str(now.year)+"-"+month
    return render_template("staff/dashboard.html", pegawai=pegawai, 
                                                    breadcumbs=breadcumbs,
                                                    data_bulan=bulan[now.month-1]+"-"+str(now.year),
                                                    bulan=bulan,
                                                    data_masuk=data_masuk,
                                                    data_keluar=data_keluar)

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


from calendar import monthrange
def get_weekend(date):
    mount = monthrange(int(str(date).split("-")[0]),int(str(date).split("-")[1]))
    start = datetime.date(int(str(date).split("-")[0]),int(str(date).split("-")[1]),1)
    end = datetime.date(int(str(date).split("-")[0]),int(str(date).split("-")[1]),mount[1])
    daydiff = end.weekday() - start.weekday()
    days = ((end-start).days - daydiff) / 7 * 6 + min(daydiff,6) - (max(end.weekday() - 4, 0) % 6)
    return mount[1], int(days)+1