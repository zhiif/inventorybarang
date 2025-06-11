from flask import Flask, render_template, request, redirect, flash, session, jsonify # Import jsonify
from flaskext.mysql import MySQL
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'rahasia'
db = MySQL(app) # Inisialisasi MySQL dengan app



# Konfigurasi database
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'dbtokoa'

# Hapus db.init_app(app) jika sudah menginisialisasi dengan app di atas
# db.init_app(app) # Ini tidak perlu lagi jika sudah db = MySQL(app)

@app.route('/')
def index():
    if 'user' not in session:
        return redirect('/login')

    data_barang = []
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT id, nama, harga, stok, kategori, deskripsi, gambar_url FROM barang")
        # Mengambil semua baris dan mengonversi menjadi list of dict untuk kemudahan di Jinja2
        columns = [col[0] for col in cursor.description]
        for row in cursor.fetchall():
            barang = dict(zip(columns, row))
            # Format harga sebagai string tanpa mengubah tipe data asli di backend
            barang['harga_formatted'] = f"Rp {int(barang['harga']):,}".replace(',', '.') # Format harga dengan titik sebagai ribuan
            # Tambahkan URL gambar default jika tidak ada kolom gambar di DB Anda
            if not barang['gambar_url']:
                barang['gambar_url'] = 'https://via.placeholder.com/200/cccccc/ffffff?text=No+Image' # Corrected this line to a string, not a list

            data_barang.append(barang)
    except Exception as e:
        flash(f"Gagal mengambil data produk: {e}", "danger")
        print(f"Error fetching products: {e}") # Debugging
    return render_template('user/index.html', products=data_barang) # Teruskan data_produk ke template

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
        # Cek apakah username sudah digunakan
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
    if 'user' not in session or session.get('role') != 'admin':
        flash("Anda harus login sebagai admin untuk mengakses halaman ini.", "danger")
        return redirect('/login')

    total_users = 0
    total_barang = 0
    total_co = 0
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT COUNT(*) FROM user WHERE role = 'user'")
        total_users = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM barang")
        total_barang = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM transaksi")
        total_co = cursor.fetchone()[0]
        
    except Exception as e:
        flash(f"Gagal mengambil data dashboard: {e}", "danger")

    return render_template('admin/index.html', total_users=total_users, total_barang=total_barang, total_co=total_co)

# Contoh dari main.py Anda yang sudah benar:
@app.route('/admin/admin-kelola-barang')
def kelolabarang():
    # ... (validasi admin) ...
    if 'user' not in session or session.get('role') != 'admin':
        flash("Anda harus login sebagai admin untuk mengakses halaman ini.", "danger")
        return redirect('/login')

    data = []
    try:
        conn = db.get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nama, harga, stok, kategori, deskripsi, gambar_url FROM barang")
        
        columns = [col[0] for col in cursor.description]
        for row in cursor.fetchall():
            barang = dict(zip(columns, row)) # Ini yang menghasilkan dictionary!
            
            barang['harga_formatted'] = f"Rp {int(barang['harga']):,}".replace(',', '.')

            full_description = barang['deskripsi'] if barang['deskripsi'] else ""
            description_limit = 100 

            if len(full_description) > description_limit:
                barang['short_description'] = full_description[:description_limit] + "..."
                barang['show_read_more'] = True
            else:
                barang['short_description'] = full_description
                barang['show_read_more'] = False
            
            barang['full_description'] = full_description


            if not barang['gambar_url']:
                barang['gambar_url'] = ['https://via.placeholder.com/200/cccccc/ffffff?text=No+Image']
            # --- AKHIR LOGIKA ---

            data.append(barang)
    except Exception as e:
        flash(f"Gagal mengambil data: {e}", "danger")
        print(f"Error di /admin/admin-kelola-barang: {e}")
    finally:
        cursor.close()
    return render_template('admin/barang.html', hasil=data)


@app.route('/admin/form-tambah-barang', methods=['GET', 'POST'])
def formbarang():
    # Validasi apakah user adalah admin
    if 'user' not in session or session.get('role') != 'admin':
        flash("Anda harus login sebagai admin untuk mengakses halaman ini.", "danger")
        return redirect('/login')
    if request.method == 'POST':
        # Ambil nilai dari form dan strip spasi berlebih
        nama = request.form.get('nama', '').strip()
        harga = request.form.get('harga', '').strip()
        stok = request.form.get('stok', '').strip()
        kategori = request.form.get('kategori', '').strip()
        deskripsi = request.form.get('deskripsi', '').strip()
        gambar_url = request.form.get('gambar_url', '').strip()

        # Validasi awal
        if not nama or not harga or not stok or not kategori:
            flash("Nama, harga, stok, dan kategori wajib diisi.", "danger")
            return redirect('/admin/form-tambah-barang')

        try:
            harga = float(harga)
            stok = int(stok)
        except ValueError:
            flash("Harga harus berupa angka desimal, dan stok harus angka bulat.", "danger")
            return redirect('/admin/form-tambah-barang')

        try:
            conn = db.get_db()
            cursor = conn.cursor()
            sql = """
                INSERT INTO barang (nama, harga, stok, kategori, deskripsi, gambar_url)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            val = (nama, harga, stok, kategori, deskripsi, gambar_url)
            cursor.execute(sql, val)
            conn.commit()
            flash("Data barang berhasil ditambahkan!", "success")
            return redirect('/admin/admin-kelola-barang')
        except Exception as e:
            flash(f'Terjadi kesalahan saat menyimpan data: {e}', 'danger')
            print(f"[ERROR] Tambah barang: {e}")
            return redirect('/admin/form-tambah-barang')
        finally:
            cursor.close()

    return render_template('admin/formbarang.html')



@app.route('/admin/form-edit-barang/<id>', methods=['GET', 'POST'])
def formeditbarang(id):
    if request.method == 'POST':
        nama = request.form['nama']
        harga = request.form['harga']
        stok = request.form['stok']
        kategori = request.form['kategori']
        deskripsi = request.form['deskripsi']
        gambar_url = request.form['gambar_url']  # Jika ada input gambar_url
        # gambar_url = request.form.get('gambar_url', '') # Jika ada input gambar_url

        try:
            cursor = db.get_db().cursor()
            sql = """
                UPDATE barang
                SET nama=%s, harga=%s, stok=%s, kategori=%s, deskripsi=%s, gambar_url=%s
                WHERE id=%s
            """
            val = (nama, harga, stok, kategori, deskripsi,gambar_url, id)
            print(val)
            cursor.execute(sql, val)
            db.get_db().commit()
        except Exception as e:
            flash(f'Terjadi kesalahan saat menyimpan data: {e}', 'danger')
            print(f"Error updating product: {e}") # Debugging

        flash("Data barang berhasil diupdate!", "success")
        return redirect('/admin/admin-kelola-barang')
    data=[]
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM barang where id=%s",(id,))
        data = cursor.fetchone()
    except Exception as e:
        flash(f'Gagal mengambil data: {e}', 'danger')
        print(f"Error fetching product for edit: {e}") # Debugging
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
        print(f"Error deleting product: {e}") # Debugging

    return redirect('/admin/admin-kelola-barang')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')



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
        cursor.execute("SELECT * FROM user where id=%s",(id,))
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
@app.route('/api/barang', methods=['POST'])
def api_barang():
    data = request.get_json()
    product_id = data.get('id')
    new_stock = data.get('stok')

    if product_id is None or new_stock is None:
        print("ERROR: Data tidak lengkap di /api/barang")
        return jsonify({'message': 'Data tidak lengkap'}), 400

    conn = None
    cursor = None
    try:
        conn = db.get_db()
        cursor = conn.cursor()

        cursor.execute("UPDATE barang SET stok = %s WHERE id = %s", (new_stock, product_id))
        conn.commit()

        cursor.execute("SELECT stok FROM barang WHERE id = %s", (product_id,))
        updated_stock = cursor.fetchone()[0]
        print(f"DEBUG: Stok barang ID {product_id} berhasil diperbarui menjadi {updated_stock} via /api/barang.")
        return jsonify({'message': 'Stok berhasil diperbarui', 'stok_terbaru': updated_stock}), 200

    except Exception as e:
        print(f"ERROR: Terjadi kesalahan saat memperbarui stok via /api/barang: {e}")
        if conn:
            conn.rollback()
        return jsonify({'message': f'Terjadi kesalahan: {e}'}), 500
    finally:
        if cursor:
            cursor.close()

@app.route('/api/get_product_stock/<int:id>', methods=['GET'])
def get_product_stock(id):
    conn = None
    cursor = None
    try:
        conn = db.get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT stok FROM barang WHERE id = %s", (id,))
        stok = cursor.fetchone()

        if not stok:
            return jsonify({'message': 'Barang tidak ditemukan'}), 404

        return jsonify({'stok': stok[0]}), 200

    except Exception as e:
        return jsonify({'message': f'Terjadi kesalahan: {e}'}), 500
    finally:
        if cursor:
            cursor.close()

@app.route('/checkout', methods=['POST'])
def checkout():
    data = request.get_json()
    cart_items = data.get('cart')

    if not cart_items:
        return jsonify({"message": "Keranjang kosong, tidak ada item untuk checkout."}), 400

    total_harga_transaksi = 0
    items_to_process = []

    conn = db.get_db()
    cursor = conn.cursor()

    try:
        for item in cart_items:
            product_id = item.get('id')
            quantity = item.get('quantity')
            price = item.get('price')

            if not all([product_id, quantity, price is not None]):
                conn.rollback()
                return jsonify({"message": "Data item keranjang tidak lengkap."}), 400

            cursor.execute("SELECT id, nama, stok FROM barang WHERE id = %s", (product_id,))
            product_data = cursor.fetchone()

            if not product_data:
                conn.rollback()
                return jsonify({"message": f"Produk dengan ID {product_id} tidak ditemukan."}), 404

            product_id_db = product_data[0]
            product_name_db = product_data[1]
            current_stock_db = product_data[2]

            if current_stock_db < quantity:
                conn.rollback()
                return jsonify({"message": f"Stok tidak cukup untuk produk: {product_name_db}."}), 400

            total_harga_transaksi += float(price) * int(quantity)
            items_to_process.append({
                'product_id': product_id_db,
                'product_name': product_name_db,
                'quantity': quantity,
                'price_at_checkout': float(price)
            })

        cursor.execute("INSERT INTO transaksi (tanggal, total) VALUES (%s, %s)",
                       (datetime.now(), total_harga_transaksi))
        conn.commit()
        transaksi_id = cursor.lastrowid

        for item_data in items_to_process:
            cursor.execute(
                "INSERT INTO detail_transaksi (transaksi_id, barang_id, nama_barang, jumlah, harga) VALUES (%s, %s, %s, %s, %s)",
                (transaksi_id, item_data['product_id'], item_data['product_name'], item_data['quantity'], item_data['price_at_checkout']))

            cursor.execute("UPDATE barang SET stok = stok - %s WHERE id = %s",
                           (item_data['quantity'], item_data['product_id']))

        conn.commit()
        return jsonify({
    "message": "Checkout berhasil!",
    "redirect_url": f"/transaction_success?transaksi_id={transaksi_id}"
}), 200


    except Exception as e:
        conn.rollback()
        return jsonify({"message": f"Terjadi kesalahan saat memproses checkout: {str(e)}"}), 500

    finally:
        cursor.close()
        conn.close()

@app.route('/transaction_success')
def transaction_success():
    return render_template('user/transaction_success.html')



@app.route('/admin/kelola-transaksi')
def kelola_transaksi():
    conn = db.get_db()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id, tanggal, total FROM transaksi ORDER BY tanggal DESC")
        transaksi_rows = cursor.fetchall()

        transaksi_data = []
        detail_map = {}

        for row in transaksi_rows:
            transaksi_id = row[0]
            tanggal = row[1]
            total = row[2]

            transaksi_data.append({
                'id': transaksi_id,
                'tanggal': tanggal,
                'total': total
            })

            cursor.execute("""
                SELECT barang_id, nama_barang, harga, jumlah
                FROM detail_transaksi
                WHERE transaksi_id = %s
            """, (transaksi_id,))
            detail_rows = cursor.fetchall()

            details = []
            for d in detail_rows:
                details.append({
                    'barang_id': d[0],
                    'nama_barang': d[1],
                    'harga': d[2],
                    'jumlah': d[3]
                })
            detail_map[transaksi_id] = details

        return render_template('admin/transaksi.html', transactions=transaksi_data, detail_map=detail_map)

    except Exception as e:
        print(f"Error fetching transaction data for admin: {e}")
        return "Terjadi kesalahan saat mengambil data transaksi.", 500
    finally:
        cursor.close()
        conn.close()

@app.route('/admin/hapus-transaksi/<int:id>', methods=['POST'])
def hapus_transaksi(id):
    conn = db.get_db()
    cursor = conn.cursor()

    try:
        # Ambil kembali barang & jumlah dari detail_transaksi
        cursor.execute("SELECT barang_id, jumlah FROM detail_transaksi WHERE transaksi_id = %s", (id,))
        detail_rows = cursor.fetchall()

        # Kembalikan stok ke tabel barang
        for row in detail_rows:
            cursor.execute("UPDATE barang SET stok = stok + %s WHERE id = %s", (row[1], row[0]))

        # Hapus detail transaksi dan transaksi utama
        cursor.execute("DELETE FROM detail_transaksi WHERE transaksi_id = %s", (id,))
        cursor.execute("DELETE FROM transaksi WHERE id = %s", (id,))
        conn.commit()

        return redirect('/admin/kelola-transaksi')


    except Exception as e:
        conn.rollback()
        return f"Gagal menghapus transaksi: {e}", 500

    finally:
        cursor.close()
        conn.close()



if __name__ == '__main__':
    app.run(debug=True)
