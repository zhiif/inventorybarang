from flask import Flask, render_template, request, redirect, flash, session
from flaskext.mysql import MySQL
app = Flask(__name__)
app.secret_key = 'rahasia'
db=MySQL(host="localhost", user="root", passwd="", db="dbtokoa")
db.init_app(app)

@app.route('/')
def index():
    if 'user' not in session:
        return redirect('/login')
    return render_template('user/index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = db.get_db().cursor()
        cursor.execute(
            "SELECT username, role FROM user WHERE username=%s AND password=%s",
            (username, password)
        )
        user = cursor.fetchone()
        if user:
            session['user'] = username
            session['role'] = user[1]
            if user[1] == 'admin':
                return redirect('/admin/home')
            else:
                return redirect('/')  # Redirect ke halaman index user
        else:
            flash('Username atau password salah!', 'danger')
            return redirect('/login')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = db.get_db().cursor()
        # Cek apakah username sudah digunakan atau belum
        cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
        if cursor.fetchone():
            flash("Username sudah terdaftar!", "danger")
            return redirect('/register')

        try:
            cursor.execute("INSERT INTO user (username, password) VALUES (%s, %s)", (username, password))
            db.get_db().commit()
            flash("Registrasi berhasil, silakan login.", "success")
            return redirect('/login')
        except Exception as e:
            flash(f"Terjadi kesalahan saat registrasi: {e}", "danger")
            return redirect('/register')

    return render_template('register.html')

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        username = request.form['username']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password != confirm_password:
            flash('Konfirmasi sandi tidak cocok', 'danger')
            return redirect('/reset-password')

        cursor = db.get_db().cursor()
        # Cek apakah username ada
        cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
        user = cursor.fetchone()

        if not user:
            flash('Username tidak ditemukan', 'danger')
            return redirect('/reset-password')

        try:
            # Update password user
            cursor.execute("UPDATE user SET password = %s WHERE username = %s", (new_password, username))
            db.get_db().commit()
            flash('Kata sandi berhasil diubah', 'success')
            return redirect('/login')
        except Exception as e:
            flash(f'Terjadi kesalahan saat mengubah kata sandi: {e}', 'danger')
            return redirect('/reset-password')

    return render_template('reset-password.html')


@app.route('/tentang')
def tentang():
    return render_template('user/tentang.html')

@app.route('/kontak')
def kontak():
    return render_template('user/kontak.html')


#  admin
@app.route('/admin/home')
def home():
    if 'user' not in session:
        return redirect('/login')

    total_users = 0
    total_barang = 0
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT COUNT(*) FROM user WHERE role = 'user'")
        total_users = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM barang")
        total_barang = cursor.fetchone()[0]
    except Exception as e:
        flash(f"Gagal mengambil data dashboard: {e}", "danger")

    return render_template('admin/index.html', total_users=total_users, total_barang=total_barang)

@app.route('/admin/admin-kelola-barang')
def kelolabarang(): 
    data=[]
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM barang")
        data = cursor.fetchall()
    except Exception as e:
        flash(f"Gagal mengambil data: {e}", "danger")
    return render_template('admin/barang.html', hasil=data)


@app.route('/admin/form-tambah-barang', methods=['GET', 'POST'])
def formbarang():
    if request.method == 'POST':
        nama = request.form['nama']
        harga = request.form['harga']
        stok = request.form['stok']
        kategori = request.form['kategori']
        deskripsi = request.form['deskripsi']
        try:
            cursor = db.get_db().cursor()
            sql = "INSERT INTO barang (nama, harga, stok, kategori, deskripsi) VALUES (%s, %s, %s, %s, %s)"
            val = (nama, harga, stok, kategori, deskripsi)
            print(val)
            cursor.execute(sql, val)
            db.get_db().commit()
        except Exception as e:
            flash(f'Terjadi kesalahan saat menyimpan data: {e}', 'danger')
        

        flash("Data barang berhasil ditambahkan!", "success")
        return redirect('/admin/admin-kelola-barang')
    return render_template('admin/formbarang.html')


@app.route('/admin/form-edit-barang/<id>', methods=['GET', 'POST'])
def formeditbarang(id):
    if request.method == 'POST':
        nama = request.form['nama']
        harga = request.form['harga']
        stok = request.form['stok']
        kategori = request.form['kategori']
        deskripsi = request.form['deskripsi']
        try:
            cursor = db.get_db().cursor()
            sql = """
                UPDATE barang
                SET nama=%s, harga=%s, stok=%s, kategori=%s, deskripsi=%s
                WHERE id=%s
            """
            val = (nama, harga, stok, kategori, deskripsi,id)
            print(val)
            cursor.execute(sql, val)
            db.get_db().commit()
        except Exception as e:
            flash(f'Terjadi kesalahan saat menyimpan data: {e}', 'danger')
        

        flash("Data barang berhasil diupdate!", "success")
        return redirect('/admin/admin-kelola-barang')
    data=[]
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM barang where id=%s",(id))
        data = cursor.fetchone()
    except Exception as e:
        flash(f'Gagal mengambil data: {e}', 'danger')
        return redirect('/admin/admin-kelola-barang')
    return render_template('admin/formeditbarang.html', barang=data)


@app.route('/admin/hapus-barang/<int:id>', methods=['POST'])
def hapus_barang(id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute("DELETE FROM barang WHERE id = %s", (id,))
        db.get_db().commit()
        flash("Barang berhasil dihapus.", "success")
    except Exception as e:
        flash(f"Gagal menghapus barang: {e}", "danger")
   

    return redirect('/admin/admin-kelola-barang')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')




@app.route('/admin/admin-kelola-pengguna')
def kelolapengguna():
    data=[]
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM barang")
        data = cursor.fetchall()
    except Exception as e:
        flash(f"Gagal mengambil data: {e}", "danger")
    return render_template('admin/pengguna.html', hasil=data)



@app.route('/admin/admin-kelola-user')
def kelolauser():
    data=[]
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM user")
        data = cursor.fetchall()
    except Exception as e:
        flash(f"Gagal mengambil data: {e}", "danger")
    return render_template('admin/user.html', hasil=data)


@app.route('/admin/form-tambah-user', methods=['GET', 'POST'])
def formuser():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
       
        try:
            cursor = db.get_db().cursor()
            sql = "INSERT INTO user (username, password) VALUES (%s, %s)"
            val = (username, password)
            print(val)
            cursor.execute(sql, val)
            db.get_db().commit()
        except Exception as e:
            flash(f'Terjadi kesalahan saat menyimpan data: {e}', 'danger')
        

        flash("Data user berhasil ditambahkan!", "success")
        return redirect('/admin/admin-kelola-user')
    return render_template('admin/formuser.html')

@app.route('/admin/form-edit-user/<id>', methods=['GET', 'POST'])
def formedituser(id):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
       
        try:
            cursor = db.get_db().cursor()
            sql = """
                UPDATE user
                SET username=%s, password=%s
                WHERE id=%s
            """
            val = (username, password,id)
            print(val)
            cursor.execute(sql, val)
            db.get_db().commit()
        except Exception as e:
            flash(f'Terjadi kesalahan saat menyimpan data: {e}', 'danger')
        

        flash("Data user berhasil diupdate!", "success")
        return redirect('/admin/admin-kelola-user')
    data=[]
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM user where id=%s",(id))
        data = cursor.fetchone()
    except Exception as e:
        flash(f'Gagal mengambil data: {e}', 'danger')
        return redirect('/admin/admin-kelola-user')
    return render_template('admin/formedituser.html', user=data)

@app.route('/admin/hapus-user/<int:id>', methods=['POST'])
def hapus_user(id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute("DELETE FROM user WHERE id = %s", (id,))
        db.get_db().commit()
        flash("user berhasil dihapus.", "success")
    except Exception as e:
        flash(f"Gagal menghapus user: {e}", "danger")
   

    return redirect('/admin/admin-kelola-user')


if __name__ == '__main__':
    app.run(debug=True)
