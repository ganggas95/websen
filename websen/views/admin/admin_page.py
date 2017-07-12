from flask_login import login_required, LoginManager, login_user, logout_user, current_user, UserMixin
from websen import app
from websen.databases.models import db, User, Jabatan, Jadwal, Pegawai, Absen
from datetime import timedelta
import logging, os, string, random, hashlib, datetime, uuid, base64
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
from flask import render_template, request, session, url_for, redirect, jsonify, flash, Response
from functools import wraps
ALLOWED_EXTENSIONS = set(['png', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'

class Breadcumb():
    def __init__(self):
        self.name = ""
        self.url = None
        self.active = False
    def get_name(self):
        return self.name
    def get_url(self):
        return self.url


class UserLogin(UserMixin):
    def __init__(self):
        self.user_id = None
        self.role = ""
        self.username = ""
        self.active = False
        foto = ""
    def get_id(self):
        return self.user_id
    def is_admin(self):
        return True if self.role == "admin" else False
    def is_pegawai(self):
        return True if self.role == "pegawai" else False
    def set_role(self, role):
        self.role = role
    def get_role(self):
        return self.role
    def set_username(self, username):
        self.username = username
    def get_username(self):
        return self.username
    def set_active(self, active):
        self.active = active
    def is_active(self):
        return True if self.active is True else False
    def set_foto(self, foto):
        self.foto = foto
    def get_foto(self):
        return self.foto

def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.get_role() not in roles:
                return redirect(url_for("unauthorized"))
            return f(*args, **kwargs)
        return wrapped
    return wrapper

def unauthorized():
    return render_template("unauthorized.html")

@login_manager.user_loader
def loader_user(user):
    u = User.query.get(user)
    if u:
        pegawai = Pegawai.query.filter_by(user_id=u.id).first()

        if pegawai:
            user_login = UserLogin()
            user_login.user_id = u.id
            if pegawai.jabatan.nama == "Administrator":
                user_login.set_role("admin")
            else:
                user_login.set_role("pegawai")
            if pegawai.foto:
                user_login.foto = pegawai.foto
            user_login.active = bool(u.active)
            user_login.username = u.username
            return user_login

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=1)

@login_required
@requires_roles("admin")
def admin_index():
    urls = str(url_for('admin_index')).split("/")
    urls.remove("")
    urls[0] = "Home"
    breadcumbs = []
    for url in urls:
        breadcumb = Breadcumb()
        breadcumb.name = url.capitalize()
        breadcumbs.append(breadcumb)
    return render_template("admin/dashboard.html", breadcumbs=breadcumbs)

def admin_login():
    if request.method == 'GET':
        if session.get('logged_in'):
            pegawai = Pegawai.query.join(User, Jabatan).filter(User.username == session.get("username")).first()
            if pegawai.jabatan.nama=="Administrator":
                return redirect(url_for("admin_index"))
            return redirect(url_for("staff_index"))
        return render_template("admin/login.html")
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username.lower()).first()
    if user:
        if user.is_active():
            if user.check_password(password):
                pegawai = Pegawai.query.filter_by(user_id=user.id).first()
                if pegawai:
                    session['logged_in']= True
                    session['username'] = username
                    user_login = UserLogin()
                    user_login.user_id = user.id
                    if pegawai.jabatan.nama == "Administrator":
                        user_login.set_role("admin")
                    elif pegawai.jabatan.nama == "Pegawai":
                        user_login.set_role("pegawai")
                    user_login.active = bool(user.active)
                    user_login.username = user.username
                    login_user(user_login)
                    flash("Selamat Datang {}".format(pegawai.nama), category='success')
                    if user_login.is_admin():
                        return redirect(url_for("admin_index"))
                    elif user_login.is_pegawai():
                        return redirect(url_for("staff_index"))
            else:
                flash("Login gagal. Coba lagi!!", category='error')
                return redirect(url_for("admin_login"))
        else:
            flash("User tidak aktive")
            return redirect(url_for("admin_login"))
    flash("Login gagal")
    return redirect(url_for("admin_login"))

@login_required
def admin_logout():
    session['logged_in'] = False
    session.clear()
    logout_user()
    return redirect(url_for("admin_login"))

@login_required
@requires_roles("admin")
def admin_users():
    users = User.query.all()
    if request.method == 'GET':
        urls = str(url_for('admin_users')).split("/")
        urls.remove("")
        urls[0] = "Home"
        breadcumbs = []
        for url in urls:
            breadcumb = Breadcumb()
            breadcumb.name = url.capitalize()
            breadcumbs.append(breadcumb)
        breadcumbs[0].url = url_for("admin_index")
        breadcumbs[len(breadcumbs)-1].active = True
        return render_template("admin/admin_users.html", users=users,breadcumbs=breadcumbs)
    if request.method == 'POST':
        data = request.get_json(force=True)
        user = User.query.get(data['id'])
        if user:
            if data['active'] == 'true':
                user.active = False
                flash("User dinonaktifkan", category='warning')
            elif data['active'] == 'false':
                user.active = True
                flash("User diaktifkan", category='success')
            db.session.add(user)
            db.session.commit()
            return jsonify({"active":data['active']}),200

@login_required
@requires_roles("admin")
def admin_pegawai():
    pegawais = Pegawai.query.all()
    if request.method == 'GET':
        urls = str(url_for('admin_pegawai')).split("/")
        urls.remove("")
        urls[0] = "Home"
        breadcumbs = []
        for url in urls:
            breadcumb = Breadcumb()
            breadcumb.name = url.capitalize()
            breadcumbs.append(breadcumb)
        breadcumbs[0].url = url_for("admin_index")
        breadcumbs[len(breadcumbs)-1].active = True
        return render_template("admin/admin_pegawai.html", pegawais=pegawais,breadcumbs=breadcumbs)

@login_required
@requires_roles("admin")
def delete_pegawai(pegawai_id):
    pegawai = Pegawai.query.get(pegawai_id)
    logging.warning(pegawai);
    if request.method =='DELETE':
        try:
            foto_src = str(pegawai.foto).split(".")
            fotos = (foto_src[0]).split("/")
            fotoToDel = fotos[len(fotos)-1]
            os.remove(os.path.join(app.config['UPLOAD_FOLDER']+fotoToDel+"."+foto_src[1]))
            db.session.delete(pegawai)
            db.session.commit()
            flash("Pegawai berhasil dihapus", category='success')
            return jsonify({"success": "Success hapus pegawai"}), 200 
        except IntegrityError as ex:
            logging.warning("error:{}".format(ex.__cause__))
            flash("Pegawai gagal dihapus, error: {}".format(ex.__cause__), category='success')
            return jsonify({"error": "Gagal hapus pegawai, error:{}".format(ex.__cause__)}), 304                                                               
@login_required
@requires_roles("admin")
def admin_pegawai_new():
    if request.method == 'GET':
        urls = str(url_for('admin_pegawai_new')).split("/")
        urls.remove("")
        urls[0] = "Home"
        breadcumbs = []
        for url in urls:
            breadcumb = Breadcumb()
            breadcumb.name = url.capitalize()
            breadcumbs.append(breadcumb)
        breadcumbs[0].url = url_for("admin_index")
        breadcumbs[len(breadcumbs)-1].active = True
        breadcumbs[len(breadcumbs)-2].url = url_for("admin_pegawai")
        jabatan = Jabatan.query.all()
        jadwal = Jadwal.query.all()
        return render_template("admin/admin_pegawai_new.html", breadcumbs=breadcumbs,
                                                                jabatan=jabatan,
                                                                jadwal=jadwal)
    nama_pegawai = request.form['nama_pegawai']
    nip_pegawai = request.form['nip']
    tempat_lahir = request.form['tempat_lahir']
    tanggal_lahir = request.form['tanggal_lahir']
    jabatan = request.form['jabatan']
    jadwal = request.form['jadwal']
    alamat = request.form['alamat']
    files = request.files['files']
    if nama_pegawai is None or nama_pegawai == "":
        flash('Nama pegawai tidak boleh kosong', category='warning')
        return redirect(url_for("admin_pegawai_new"))
    if nip_pegawai is None or nip_pegawai == "":
        flash('NIP pegawai tidak boleh kosong',category='warning')
        return redirect(url_for("admin_pegawai_new"))
    if not check_pegawai_nip(nip_pegawai):
        flash('NIP pegawai sudah ada. Coba yang lain!!',category='warning')
        return redirect(url_for("admin_pegawai_new"))
    if tempat_lahir is None or tempat_lahir == "":
        flash('Tempat lahir pegawai tidak boleh kosong',category='warning')
        return redirect(url_for("admin_pegawai_new"))
    if tanggal_lahir is None or tanggal_lahir == "":
        flash('Tanggal lahir pegawai tidak boleh kosong',category='warning')
        return redirect(url_for("admin_pegawai_new"))
    if jabatan is None or int(jabatan) == 0:
        flash('Jabatan pegawai tidak boleh kosong',category='warning')
        return redirect(url_for("admin_pegawai_new"))
    if jadwal is None or int(jadwal) == 0:
        flash('Jabatan pegawai tidak boleh kosong',category='warning')
        return redirect(url_for("admin_pegawai_new"))
    if files or allowed_file(files.filename):
        filename = secure_filename(files.filename)
        basedir = os.path.join(app.config['UPLOAD_FOLDER'], filename)   
        files.save(basedir)
        pegawai = Pegawai()
        pegawai.nama = nama_pegawai
        pegawai.nip = nip_pegawai
        pegawai.tanggal_lahir = tanggal_lahir
        pegawai.tempat_lahir = tempat_lahir
        jbtn = Jabatan.query.get(jabatan)
        jdwl = Jadwal.query.get(jadwal)
        if jbtn is None:
            flash('Maaf data jabatan tidak dikenali system',category='warning')
            return redirect(url_for("admin_pegawai_new"))
        if jdwl is None:
            flash('Maaf data jadwal tidak dikenali system',category='warning')
            return redirect(url_for("admin_pegawai_new"))
        pegawai.jabatan = jbtn
        pegawai.jadwal = jdwl
        pegawai.alamat = alamat
        pegawai.foto = "/static/uploads/profile/"+filename
        username = (str(nama_pegawai).split(" ")[0]).lower()+"_"+randomword(3)
        password = hashlib.md5(username.encode('ascii')).hexdigest()
        user = User(username=username,password=password)
        pegawai.user = user
        db.session.add(pegawai)
        db.session.commit()
        flash('Pegawai berhasil dibuat',category='success')
        return redirect(url_for('admin_pegawai'))

def check_pegawai_nip(nip):
    pegawai = Pegawai.query.filter_by(nip=nip).first()
    if pegawai:
        return False
    return True

@login_required
@requires_roles("admin")
def admin_pegawai_edit(pegawai_id):
    pegawai = Pegawai.query.get(pegawai_id)
    if request.method == 'GET':
        jabatan = Jabatan.query.all()
        jadwal = Jadwal.query.all()
        urls = str(url_for('admin_pegawai')+"/"+"edit").split("/")
        urls.remove("")
        urls[0] = "Home"
        breadcumbs = []
        for url in urls:
            breadcumb = Breadcumb()
            breadcumb.name = url.capitalize()
            breadcumbs.append(breadcumb)
        breadcumbs[0].url = url_for("admin_index")
        breadcumbs[len(breadcumbs)-1].active = True
        breadcumbs[len(breadcumbs)-2].url = url_for("admin_pegawai")
        return render_template("admin/admin_pegawai_edit.html", pegawai = pegawai,
                                                                jabatan=jabatan,
                                                                jadwal=jadwal,
                                                                breadcumbs=breadcumbs)
    nama_pegawai = request.form['nama_pegawai']
    tempat_lahir = request.form['tempat_lahir']
    tanggal_lahir = request.form['tanggal_lahir']
    jabatan = request.form['jabatan']
    jadwal = request.form['jadwal']
    alamat = request.form['alamat']
    if nama_pegawai is None or nama_pegawai == "":
        flash('Nama pegawai tidak boleh kosong', category='warning')
        return redirect("/admin/data/pegawai/"+str(pegawai_id)+"/edit")
    if tempat_lahir is None or tempat_lahir == "":
        flash('Tempat lahir pegawai tidak boleh kosong',category='warning')
        return redirect("/admin/data/pegawai/"+str(pegawai_id)+"/edit")
    if tanggal_lahir is None or tanggal_lahir == "":
        flash('Tanggal lahir pegawai tidak boleh kosong',category='warning')
        return redirect("/admin/data/pegawai/"+str(pegawai_id)+"/edit")
    if jabatan is None or int(jabatan) == 0:
        flash('Jabatan pegawai tidak boleh kosong',category='warning')
        return redirect("/admin/data/pegawai/"+str(pegawai_id)+"/edit")
    if jadwal is None or int(jadwal) == 0:
        flash('Jabatan pegawai tidak boleh kosong', category='warning')
        return redirect("/admin/data/pegawai/"+str(pegawai_id)+"/edit")
    pegawai.nama = str(nama_pegawai).capitalize()
    pegawai.tanggal_lahir = tanggal_lahir
    pegawai.tempat_lahir = str(tempat_lahir).capitalize()
    jbtn = Jabatan.query.get(jabatan)
    jdwl = Jadwal.query.get(jadwal)
    if jbtn is None:
        flash('Maaf data jabatan tidak dikenali system',category='warning')
        return redirect("/admin/data/pegawai/"+str(pegawai_id)+"/edit")
    if jdwl is None:
        flash('Maaf data jadwal tidak dikenali system',category='warning')
        return redirect("/admin/data/pegawai/"+str(pegawai_id)+"/edit")
    pegawai.jabatan = jbtn
    pegawai.jadwal = jdwl
    pegawai.alamat = alamat
    db.session.add(pegawai)
    db.session.commit()
    flash('Pegawai berhasil diubah',category='success')
    return redirect(url_for('admin_pegawai'))

@login_required
@requires_roles("admin")
def admin_jabatan():
    jabatan = Jabatan.query.all()
    if request.method == 'GET':
        urls = str(url_for('admin_jabatan')).split("/")
        urls.remove("")
        urls[0] = "Home"
        breadcumbs = []
        for url in urls:
            breadcumb = Breadcumb()
            breadcumb.name = url.capitalize()
            breadcumbs.append(breadcumb)
        breadcumbs[0].url = url_for("admin_index")
        breadcumbs[len(breadcumbs)-1].active = True
        return render_template("admin/admin_jabatan.html", jabatan=jabatan,breadcumbs=breadcumbs)

@login_required
@requires_roles("admin")
def delete_jabatan(jab_id):
    jabatan = Jabatan.query.get(jab_id)
    if request.method =='DELETE':
        try:
            db.session.delete(jabatan)
            db.session.commit()
            flash("Jabatan berhasil dihapus", category='success')
            return jsonify({"success": "Success hapus pegawai"}), 200 
        except IntegrityError as ex:
            logging.warning("error:{}".format(ex.__cause__))
            flash("Jabatan gagal dihapus, error: {}".format(ex.__cause__), category='success')
            return jsonify({"error": "Gagal hapus pegawai, error:{}".format(ex.__cause__)}), 304 

@login_required
@requires_roles("admin")
def admin_jabatan_new():
    if request.method == 'GET':
        urls = str(url_for('admin_jabatan_new')).split("/")
        urls.remove("")
        urls[0] = "Home"
        breadcumbs = []
        for url in urls:
            breadcumb = Breadcumb()
            breadcumb.name = url.capitalize()
            breadcumbs.append(breadcumb)
        breadcumbs[0].url = url_for("admin_index")
        breadcumbs[len(breadcumbs)-2].url = url_for("admin_jabatan")
        breadcumbs[len(breadcumbs)-1].active = True
        return render_template("admin/admin_jabatan_new.html", breadcumbs=breadcumbs)
    
    nama_jabatan = request.form['name']
    if nama_jabatan is None or nama_jabatan == "":
        flash('Data jabatan tidak boleh kosong')
        return redirect(url_for("admin_jabatan_new"))
    jabatan = Jabatan(nama=nama_jabatan)
    db.session.add(jabatan)
    db.session.commit()
    return redirect(url_for('admin_jabatan'))    

@login_required
@requires_roles("admin")
def admin_jabatan_edit(jabatan_id):
    jabatan = Jabatan.query.get(jabatan_id)
    if request.method == 'GET':
        urls = str(url_for('admin_jabatan')+"/"+"edit").split("/")
        urls.remove("")
        urls[0] = "Home"
        breadcumbs = []
        for url in urls:
            breadcumb = Breadcumb()
            breadcumb.name = url.capitalize()
            breadcumbs.append(breadcumb)
        breadcumbs[0].url = url_for("admin_index")
        breadcumbs[len(breadcumbs)-2].url = url_for("admin_jabatan")
        breadcumbs[len(breadcumbs)-1].active = True
        return render_template("admin/admin_jabatan_edit.html", jabatan=jabatan,breadcumbs=breadcumbs)
    
    nama_jabatan = request.form['name']
    if nama_jabatan is None or nama_jabatan == "":
        flash('Data jabatan tidak boleh kosong')
        return redirect(url_for("admin_jabatan_edit"))
    jabatan.nama = nama_jabatan
    db.session.add(jabatan)
    db.session.commit()
    return redirect(url_for('admin_jabatan'))     

@login_required
@requires_roles("admin")
def admin_jadwal():
    jadwal = Jadwal.query.all()
    if request.method == 'GET':
        urls = str(url_for('admin_jadwal')).split("/")
        urls.remove("")
        urls[0] = "Home"
        breadcumbs = []
        for url in urls:
            breadcumb = Breadcumb()
            breadcumb.name = url.capitalize()
            breadcumbs.append(breadcumb)
        breadcumbs[0].url = url_for("admin_index")
        breadcumbs[len(breadcumbs)-1].active = True
        return render_template("admin/admin_jadwal.html", jadwal=jadwal,breadcumbs=breadcumbs)

@login_required
@requires_roles("admin")
def delete_jadwal(jadwal_id):
    jadwal = Jadwal.query.get(jadwal_id)
    if request.method =='DELETE':
        try:
            db.session.delete(jadwal)
            db.session.commit()
            flash("Jadwal berhasil dihapus", category='success')
            return jsonify({"success": "Success hapus pegawai"}), 200 
        except IntegrityError as ex:
            logging.warning("error:{}".format(ex.__cause__))
            flash("Jadwal gagal dihapus, error: {}".format(ex.__cause__), category='success')
            return jsonify({"error": "Gagal hapus pegawai, error:{}".format(ex.__cause__)}), 304 

@login_required
@requires_roles("admin")
def admin_jadwal_new():
    if request.method == 'GET':
        urls = str(url_for('admin_jadwal_new')).split("/")
        urls.remove("")
        urls[0] = "Home"
        breadcumbs = []
        for url in urls:
            breadcumb = Breadcumb()
            breadcumb.name = url.capitalize()
            breadcumbs.append(breadcumb)
        breadcumbs[0].url = url_for("admin_index")
        breadcumbs[len(breadcumbs)-2].url = url_for("admin_jadwal")
        breadcumbs[len(breadcumbs)-1].active = True
        return render_template("admin/admin_jadwal_new.html",breadcumbs=breadcumbs)
    nama_jadwal = request.form['name_jadwal']
    jadwal_masuk_start = request.form['jam_masuk_start']
    jadwal_masuk_end = request.form['jam_masuk_end']
    jadwal_keluar_start = request.form['jam_keluar_start']
    jadwal_keluar_end = request.form['jam_keluar_end']
    if nama_jadwal is None or nama_jadwal == "":
        flash('Nama jadwal tidak boleh kosong',category='warning')
        return redirect(url_for("admin_jadwal_new"))
    if jadwal_masuk_start is None or jadwal_masuk_start == "":
        flash('Absen masuk mulai tidak boleh kosong',category='warning')
        return redirect(url_for("admin_jadwal_new"))
    if jadwal_masuk_end is None or jadwal_masuk_end == "":
        flash('Absen masuk selesai tidak boleh kosong',category='warning')
        return redirect(url_for("admin_jadwal_new"))
    if jadwal_keluar_start is None or jadwal_keluar_start == "":
        flash('Absen keluar mulai tidak boleh kosong',category='warning')
        return redirect(url_for("admin_jadwal_new"))
    if jadwal_keluar_end is None or jadwal_keluar_end == "":
        flash('Absen keluar selesai tidak boleh kosong',category='warning')
        return redirect(url_for("admin_jadwal_new"))
    jadwal = Jadwal(display_name=str(nama_jadwal).capitalize())
    name_tmp = str(nama_jadwal).split(" ")
    nama = name_tmp[0]
    if len(name_tmp)>1:
        nama = nama+name_tmp[1]
    jadwal.nama = nama.lower()
    jadwal.jadwal_masuk_start=jadwal_masuk_start
    jadwal.jadwal_masuk_end=jadwal_masuk_end
    jadwal.jadwal_keluar_start=jadwal_keluar_start
    jadwal.jadwal_keluar_end=jadwal_keluar_end
    db.session.add(jadwal)
    db.session.commit()
    flash("Jadwal berhasil dibuat", category='success')
    return redirect(url_for('admin_jadwal'))    

@login_required
@requires_roles("admin")
def admin_jadwal_edit(jadwal_id):
    jadwal = Jadwal.query.get(jadwal_id)
    if request.method == 'GET':
        urls = str(url_for('admin_jadwal')+"/"+"edit").split("/")
        urls.remove("")
        urls[0] = "Home"
        breadcumbs = []
        for url in urls:
            breadcumb = Breadcumb()
            breadcumb.name = url.capitalize()
            breadcumbs.append(breadcumb)
        breadcumbs[0].url = url_for("admin_index")
        breadcumbs[len(breadcumbs)-2].url = url_for("admin_jadwal")
        breadcumbs[len(breadcumbs)-1].active = True
        return render_template("admin/admin_jadwal_edit.html",jadwal=jadwal,breadcumbs=breadcumbs)
    nama_jadwal = request.form['name_jadwal']
    jadwal_masuk_start = request.form['jam_masuk_start']
    jadwal_masuk_end = request.form['jam_masuk_end']
    jadwal_keluar_start = request.form['jam_keluar_start']
    jadwal_keluar_end = request.form['jam_keluar_end']
    if nama_jadwal is None or nama_jadwal == "":
        flash('Nama jadwal tidak boleh kosong', category='warning')
        return redirect("/admin/setting/jadwal/"+jadwal_id+"/edit")
    if jadwal_masuk_start is None or jadwal_masuk_start == "":
        flash('Absen masuk mulai tidak boleh kosong', category='warning')
        return redirect("/admin/setting/jadwal/"+jadwal_id+"/edit")
    if jadwal_masuk_end is None or jadwal_masuk_end == "":
        flash('Absen masuk selesai tidak boleh kosong', category='warning')
        return redirect("/admin/setting/jadwal/"+jadwal_id+"/edit")
    if jadwal_keluar_start is None or jadwal_keluar_start == "":
        flash('Absen keluar mulai tidak boleh kosong', category='warning')
        return redirect("/admin/setting/jadwal/"+jadwal_id+"/edit")
    if jadwal_keluar_end is None or jadwal_keluar_end == "":
        flash('Absen keluar selesai tidak boleh kosong', category='warning')
        return redirect("/admin/setting/jadwal/"+jadwal_id+"/edit")
    name_tmp = str(nama_jadwal).split(" ")
    nama = name_tmp[0]
    if len(name_tmp)>1:
        nama = nama+name_tmp[1]
    jadwal.nama=nama.lower()
    jadwal.display_name = str(nama_jadwal).capitalize()
    jadwal.jadwal_masuk_start=jadwal_masuk_start
    jadwal.jadwal_masuk_end=jadwal_masuk_end
    jadwal.jadwal_keluar_start=jadwal_keluar_start
    jadwal.jadwal_keluar_end=jadwal_keluar_end
    db.session.add(jadwal)
    db.session.commit()
    flash("Jadwal berhasil diubah", category='success')
    return redirect(url_for('admin_jadwal'))    

@login_required
@requires_roles("admin")
def admin_absen():
    absens = None
    bulan = None
    tanggal = None
    if request.args.get("bulan"):
        date = request.args.get('bulan')
        bulan = date
        absens = Absen.query.filter(Absen.tanggal.like("%"+bulan+"%")).all()
    elif request.args.get("tanggal"):
        date = request.args.get('tanggal')
        tanggal = date
        absens = Absen.query.filter(Absen.tanggal.like("%"+date+"%")).all()
    else:
        absens = Absen.query.order_by(desc(Absen.tanggal)).all()
    if request.method == 'GET':
        urls = str(url_for('admin_absen')).split("/")
        urls.remove("")
        urls[0] = "Home"
        breadcumbs = []
        for url in urls:
            breadcumb = Breadcumb()
            breadcumb.name = url.capitalize()
            breadcumbs.append(breadcumb)
        breadcumbs[0].url = url_for("admin_index")
        breadcumbs[len(breadcumbs)-1].active = True
        return render_template("admin/admin_absen.html", absens=absens, tanggal=tanggal,bulan=bulan,breadcumbs=breadcumbs)


def randomword(length):
   return ''.join(random.choice("0123456789abcdefghijklmnopqrstuvwxyz") for i in range(length))

@login_required
@requires_roles('admin')
def admin_profile():
    user_id = current_user.user_id
    user = User.query.get(user_id)
    if request.method == 'GET':
        pegawai = Pegawai.query.filter_by(user_id=user_id).first()
        urls = str(url_for('admin_profile')).split("/")
        urls.remove("")
        urls[0] = "Home"
        breadcumbs = []
        for url in urls:
            breadcumb = Breadcumb()
            breadcumb.name = url.capitalize()
            breadcumbs.append(breadcumb)
        breadcumbs[0].url = url_for("admin_profile")
        breadcumbs[len(breadcumbs)-1].active = True
        return render_template("admin/profile.html", pegawai=pegawai, breadcumbs=breadcumbs)
    if request.method == 'POST':
        username = request.form['username']
        res, msg = change_username(username, user)
        if res:
            flash(msg, category="success")
            return redirect(url_for('admin_profile'))
        else:
            flash(msg, category="error")
            return redirect(url_for('admin_profile'))

@login_required
@requires_roles('admin')
def admin_ganti_password():
    if request.method == 'POST':
        user_id = current_user.user_id
        old_pass = request.form['old_password']
        new_pass = request.form['password_baru']
        pass_conf = request.form['password_conf']
        res, msg = change_password(old_pass,new_pass,pass_conf,user_id)
        if res:
            flash(msg, category="success")
            return redirect(url_for('admin_profile'))
        else:
            flash(msg, category="error")
            return redirect(url_for('admin_profile'))

@login_required
@requires_roles('admin')
def admin_change_foto(pegawai_id):
    res, msg = change_foto(pegawai_id)
    if res:
        flash(msg, category="success")
        return jsonify({"success":"Ganti Foto Berhasil"}),200
    else:
        flash(msg, category="error")
        return jsonify({"error":"Data tidak ditemukan"}), 302

def change_password(old_pass, new_pass, pass_conf,user_id):
    user = User.query.get(user_id)
    if user.password == hashlib.md5(str(old_pass).encode('ascii')).hexdigest():
        if new_pass == pass_conf:
            user.password = hashlib.md5(str(new_pass).encode('ascii')).hexdigest()
            db.session.add(user)
            db.session.commit()
            return True, "Password berhasil diganti"
        else:    
            return False, "Password tidak sama"
    else:    
        return False, "Password Salah"

def change_foto(pegawai_id):
    pegawai = Pegawai.query.get(pegawai_id)
    if pegawai:
        jsonData = request.get_json(force=True)
        img_data = jsonData['data']
        img_ext = jsonData['ext']
        unique_filename = uuid.uuid4()
        filename = str(unique_filename) + "." + img_ext
        foto_src = str(pegawai.foto).split(".")
        fotos = (foto_src[0]).split("/")
        fotoToDel = fotos[len(fotos)-1]
        if fotoToDel:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER']+fotoToDel+"."+foto_src[1]))
            with open(app.config['UPLOAD_FOLDER'] + filename, "wb") as fh:
                fh.write(base64.b64decode(img_data))
        
        pegawai.foto = "/static/uploads/profile/"+filename
        db.session.add(pegawai)
        db.session.commit()
        return True, "Sukses mengganti foto"
        
    else:
        return False, "Gagal mengganti foto"

def change_username(username, user):
    if username:
        user.username = username
        try:
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return True, "Sukses mengubah username"
        except IntegrityError as ex:
            return False, "Gagal mengubah username"
    else:
        return False, "Gagal mengubah username"

@login_required
@requires_roles("admin")
def download_absens():
    data = []
    bulan = None
    tanggal = None
    title = None
    subtitle = None
    tipe = None
    absens = Absen.query.order_by(desc(Absen.tanggal)).all()
    hari_kerja = None
    hari_libur = None
    jumlah_hari = None
    pegawais = Pegawai.query.all()
    if request.args.get("bulan"):
        title = "Laporan Bulanan"
        date = request.args.get('bulan')
        bulan = date
        subtitle = "Bulan : "+date
        absens = Absen.query.filter(Absen.tanggal.like("%"+bulan+"%")).all()
        tipe = "bulanan"
        mount = get_weekend(date)
        for absen in absens:
            for p in pegawais:
                if p.id == absen.pegawai.id:
                    if absen.masuk:
                        p.jumlah_masuk = p.jumlah_masuk+1
                    if absen.keluar:
                        p.jumlah_keluar = p.jumlah_keluar+1   
        hari_kerja =  mount[1]
        hari_libur = mount[0]-mount[1]
        jumlah_hari = mount[0]
    elif request.args.get("tanggal"):
        date = request.args.get('tanggal')
        title = "Laporan Harian"
        tanggal = date
        subtitle = "Tanggal : "+tanggal
        absens = Absen.query.filter(Absen.tanggal.like("%"+date+"%")).all()
        tipe = "harian"
    else:
        absens = Absen.query.all()
        tipe = "bulanan"
        for absen in absens:
            for p in pegawais:
                if p.id == absen.pegawai.id:
                    if absen.masuk:
                        p.jumlah_masuk = p.jumlah_masuk+1
                    if absen.keluar:
                        p.jumlah_keluar = p.jumlah_keluar+1
    
    return render_template("admin/report.html", absens=absens, 
                                                title=title, 
                                                subtitle=subtitle, 
                                                pegawais=pegawais, 
                                                tipe=tipe,
                                                hari_libur=hari_libur,
                                                hari_kerja=hari_kerja,
                                                jumlah_hari=jumlah_hari)
from calendar import monthrange
def get_weekend(date):
    mount = monthrange(int(str(date).split("-")[0]),int(str(date).split("-")[1]))
    start = datetime.date(int(str(date).split("-")[0]),int(str(date).split("-")[1]),1)
    end = datetime.date(int(str(date).split("-")[0]),int(str(date).split("-")[1]),mount[1])
    daydiff = end.weekday() - start.weekday()
    days = ((end-start).days - daydiff) / 7 * 6 + min(daydiff,6) - (max(end.weekday() - 4, 0) % 6)
    logging.warning(mount[0])
    logging.warning(days)
    return mount[1], int(days)+1