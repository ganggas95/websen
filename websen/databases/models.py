from websen import app
from flask_sqlalchemy import SQLAlchemy
import hashlib,json,logging

db = SQLAlchemy(app=app)

db.Model.metadata.reflect(db.engine)
class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    # id = db.Column(db.Integer, primary_key=True)
    # username = db.Column(db.String(45))
    # password = db.Column(db.String(45))
    # active = db.Column(db.Boolean, default=False)
    auth = False

    def is_active(self):
        return self.active

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.auth

    def check_password(self, password):
        self.auth = self.password == hashlib.md5(password.encode('ascii')).hexdigest()
        return self.auth
        # return True__table_args__ = {'extend_existing': True}

class Jabatan(db.Model):
    __tablename__ = 'jabatan'
    __table_args__ = {'extend_existing': True}

class Jadwal(db.Model):
    __tablename__ = 'jadwal'
    __table_args__ = {'extend_existing': True}

class Pegawai(db.Model):
    __tablename__ = 'pegawai'
    __table_args__ = {'extend_existing': True}
    jabatan_id = db.Column("jabatan_id", db.ForeignKey('jabatan.id'))
    jabatan = db.relationship('Jabatan', backref=db.backref('jabatan_pegawai', lazy='dynamic'))
    jadwal_id = db.Column("jadwal_id", db.ForeignKey('jadwal.id'))
    jadwal = db.relationship('Jadwal', backref=db.backref('jadwal_pegawai', lazy='dynamic'))
    user_id = db.Column("user_id", db.ForeignKey('users.id'))
    user = db.relationship('User', backref=db.backref('users_pegawai', lazy='dynamic'))
    jumlah_masuk = 0
    jumlah_keluar = 0

class Absen(db.Model):
    __tablename__ = 'absen'
    __table_args__ = {'extend_existing': True}
    pegawai_id = db.Column("pegawai_id", db.ForeignKey('pegawai.id'))
    pegawai = db.relationship('Pegawai', backref=db.backref('absen_pegawai', lazy='dynamic'))
    

# user = User(username="admin",password=hashlib.md5("admin".encode("ascii")).hexdigest())
# db.session.add(user)
# db.session.commit()