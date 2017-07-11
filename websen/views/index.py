from websen import app
from flask import render_template, redirect,url_for,request, flash
from websen.databases.models import Jadwal, db, Pegawai, Absen
import time, logging, datetime
class AbsenSession():
    session = None
    def setSession(self, session):
        self.session = session
    def getSession():
        return self.session

@app.route("/")
def index():
    jadwal  = Jadwal.query.all()
    return render_template("index.html", jadwal=jadwal)
@app.route("/absen", methods=['POST'])
def absen():
    if request.method == 'POST':
        timeNow = datetime.datetime.now().time()
        dateNow = datetime.datetime.now().date()
        sql = '''
            SELECT * from `jadwal` where (CURRENT_TIME()>= jadwal.jadwal_masuk_start AND CURRENT_TIME() <= jadwal.jadwal_masuk_end OR CURRENT_TIME()>= jadwal.jadwal_keluar_start AND CURRENT_TIME() <= jadwal.jadwal_keluar_end)
        '''
        kolom = ('id','nama','display_name', 'jadwal_masuk_start','jadwal_masuk_end','jadwal_keluar_start','jadwal_keluar_end')
        result = db.engine.execute(sql)
        
        if result:
            nip = request.form['nip']
            pegawai = Pegawai.query.filter_by(nip=nip).first()
            if pegawai:
                for res in result:
                    hasil = dict(zip(kolom, res))
                    if pegawai.jadwal.id == hasil['id']:
                        jadwal = Jadwal.query.get(hasil['id'])
                        if jadwal.jadwal_masuk_start<=timeNow and jadwal.jadwal_masuk_end >= timeNow:
                            absen = Absen.query.filter_by(pegawai_id = pegawai.id).filter_by(tanggal=dateNow).filter_by(masuk=True).first()
                            if absen is None:
                                do_absen = Absen(masuk=True)
                                do_absen.pegawai = pegawai
                                do_absen.tanggal = dateNow
                                db.session.add(do_absen)
                                db.session.commit()
                                flash("Absen masuk berhasil", category='success')
                            else:
                                flash("Absen masuk telah dilakukan", category='success')
                        elif jadwal.jadwal_keluar_start<=timeNow and jadwal.jadwal_keluar_end >= timeNow:
                            absen = Absen.query.filter_by(pegawai_id = pegawai.id).filter_by(tanggal=dateNow).filter_by(keluar=True).first()
                            if absen is None:
                                absen = Absen.query.filter_by(pegawai_id = pegawai.id).filter_by(tanggal=dateNow).first()
                                if absen:
                                    absen.keluar = True
                                    db.session.add(absen)
                                    db.session.commit()
                                    flash("Absen keluar berhasil", category='success')
                                else:
                                    absen = Absen(keluar=True)
                                    absen.pegawai = pegawai
                                    absen.tanggal = dateNow
                                    db.session.add(absen)
                                    db.session.commit()
                                    flash("Anda tidak melakukan absen masuk. Absen keluar berhasil", category='success')
                            else:
                                flash("Absen keluar telah dilakukan", category='success')
                        return redirect(url_for('index'))
                    else:
                        flash("Absen Gagal", category='success')
                        return redirect(url_for('index'))
            else:
                flash("Absen Gagal", category='error')
                return redirect(url_for('index'))
            
        flash("Absen Gagal", category='error')
        return redirect(url_for('index'))

def build_time(timedelta):
    times = str(timedelta).split(":")    
    return times
