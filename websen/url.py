from websen.helper.url_loader import url_mapper
'''

URL Untuk Admin

'''


url_mapper("/unauthorized",
                "views.admin.admin_page.unauthorized", methods=['GET'])

url_mapper("/login",
                "views.admin.admin_page.admin_login", methods=['GET', 'POST'])

url_mapper("/admin",
                "views.admin.admin_page.admin_index", methods=['GET'])

url_mapper("/logout",
                "views.admin.admin_page.admin_logout", methods=['GET'])

url_mapper("/admin/data/users",
                "views.admin.admin_page.admin_users", methods=['GET','POST'])

url_mapper("/admin/data/pegawai",
                "views.admin.admin_page.admin_pegawai", methods=['GET'])

url_mapper("/admin/data/pegawai/<int:pegawai_id>/delete",
                "views.admin.admin_page.delete_pegawai", methods=['DELETE'])

url_mapper("/admin/data/pegawai/new",
                "views.admin.admin_page.admin_pegawai_new", methods=['GET', 'POST'])

url_mapper("/admin/data/pegawai/<int:pegawai_id>/edit",
                "views.admin.admin_page.admin_pegawai_edit", methods=['GET', 'POST'])

url_mapper("/admin/data/jabatan",
                "views.admin.admin_page.admin_jabatan", methods=['GET'])

url_mapper("/admin/data/jabatan/<int:jab_id>/delete",
                "views.admin.admin_page.delete_jabatan", methods=['DELETE'])

url_mapper("/admin/data/jabatan/new",
                "views.admin.admin_page.admin_jabatan_new", methods=['GET', 'POST'])

url_mapper("/admin/data/jabatan/<int:jabatan_id>/edit",
                "views.admin.admin_page.admin_jabatan_edit", methods=['GET', 'POST'])

url_mapper("/admin/data/absen",
                "views.admin.admin_page.admin_absen", methods=['GET'])

url_mapper("/admin/setting/jadwal",
                "views.admin.admin_page.admin_jadwal", methods=['GET','DELETE'])

url_mapper("/admin/setting/jadwal/<int:jadwal_id>/delete",
                "views.admin.admin_page.delete_jadwal", methods=['DELETE'])

url_mapper("/admin/setting/jadwal/new",
                "views.admin.admin_page.admin_jadwal_new", methods=['GET', 'POST'])

url_mapper("/admin/setting/jadwal/<int:jadwal_id>/edit",
                "views.admin.admin_page.admin_jadwal_edit", methods=['GET', 'POST'])

url_mapper("/admin/profile",
                "views.admin.admin_page.admin_profile", methods=['GET','POST'])

url_mapper("/admin/profile/foto/<int:pegawai_id>/change",
                "views.admin.admin_page.admin_change_foto", methods=['POST'])

url_mapper("/admin/profile/password/change", 
                "views.admin.admin_page.admin_ganti_password", methods=["POST"])

# url_mapper("/admin/data/absen/export", 
#                 "views.admin.admin_page.download_absens", methods=["GET"])

url_mapper("/staff", "views.staff.staff_page.staff_index", methods=['GET'])
            
url_mapper("/staff/profile", "views.staff.staff_page.staf_profile", methods=['GET','POST'])
                
url_mapper("/staff/absen", "views.staff.staff_page.staf_absen", methods=['GET'])

url_mapper("/staff/profile/foto/<int:pegawai_id>/change",
                "views.staff.staff_page.staff_change_foto", methods=['POST'])

url_mapper("/staff/profile/password/change", 
                "views.staff.staff_page.staff_ganti_password", methods=["POST"])