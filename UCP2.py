import sqlite3
import tkinter as tk
from tkinter import Tk, Label, Entry, Button, ttk, Toplevel

# Fungsi untuk membuat tabel jika belum ada
def create_table():
    conn = sqlite3.connect('pegawai.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pegawai (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT,
            alamat TEXT,
            posisi TEXT,
            tahun_masuk INTEGER
        )
    ''')

    conn.commit()
    conn.close()

# Fungsi CREATE
def insert_data(nama, alamat, posisi, tahun_masuk):
    conn = sqlite3.connect('pegawai.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO pegawai (nama, alamat, posisi, tahun_masuk)
        VALUES (?, ?, ?, ?)
    ''', (nama, alamat, posisi, tahun_masuk))

    conn.commit()
    conn.close()

# Fungsi READ
def read_data():
    conn = sqlite3.connect('pegawai.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM pegawai')
    rows = cursor.fetchall()

    conn.close()
    return rows

# Fungsi UPDATE
def update_data(id, nama, alamat, posisi, tahun_masuk):
    conn = sqlite3.connect('pegawai.db')
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE pegawai
        SET nama=?, alamat=?, posisi=?, tahun_masuk=?
        WHERE id=?
    ''', (nama, alamat, posisi, tahun_masuk, id))

    conn.commit()
    conn.close()

# Fungsi DELETE by ID
def delete_data(id):
    conn = sqlite3.connect('pegawai.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM pegawai WHERE id=?', (id,))

    conn.commit()
    conn.close()

# Fungsi untuk submit data pegawai baru
def submit_data():
    nama = entry_nama.get()
    alamat = entry_alamat.get()
    posisi = entry_posisi.get()
    tahun_masuk = int(entry_tahun.get())

    insert_data(nama, alamat, posisi, tahun_masuk)
    label_hasil.config(text=f'Pegawai {nama} berhasil ditambahkan.')
    tampilkan_data()

# Fungsi untuk menampilkan data pegawai
def tampilkan_data():
    rows = read_data()
    data_to_display = ''
    for row in rows:
        data_to_display += f'ID: {row[0]} | Nama: {row[1]} | Alamat: {row[2]} | Posisi: {row[3]} | Tahun Masuk: {row[4]}\n'
    label_hasil2.config(text=data_to_display)

# Fungsi untuk update data pegawai berdasarkan ID
def update_data_button():
    id = int(entry_id.get())
    nama = entry_nama.get()
    alamat = entry_alamat.get()
    posisi = entry_posisi.get()
    tahun_masuk = int(entry_tahun.get())

    update_data(id, nama, alamat, posisi, tahun_masuk)
    label_hasil.config(text=f'Data pegawai ID {id} berhasil diupdate.')
    tampilkan_data()

# Fungsi untuk hapus data pegawai berdasarkan ID
def delete_data_button():
    id = int(entry_id.get())
    delete_data(id)
    label_hasil.config(text=f'Data pegawai ID {id} berhasil dihapus.')
    tampilkan_data()

# Fungsi untuk reset tabel (hapus semua data & reset auto increment)
def reset_table():
    conn = sqlite3.connect('pegawai.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM pegawai')  # hapus semua data
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='pegawai'")  # reset auto increment

    conn.commit()
    conn.close()
    label_hasil.config(text="Tabel pegawai berhasil direset (data dihapus, ID dimulai dari 1).")
    label_hasil2.config(text='')

# Inisialisasi database
create_table()

# GUI Tkinter
root = Tk()
root.title('CRUD Pegawai')

Label(root, text='ID (untuk Update/Delete):').grid(row=0, column=0)
entry_id = Entry(root)
entry_id.grid(row=0, column=1)

Label(root, text='Nama:').grid(row=1, column=0)
entry_nama = Entry(root)
entry_nama.grid(row=1, column=1)

Label(root, text='Alamat:').grid(row=2, column=0)
entry_alamat = Entry(root)
entry_alamat.grid(row=2, column=1)

Label(root, text='Posisi:').grid(row=3, column=0)
entry_posisi = Entry(root)
entry_posisi.grid(row=3, column=1)

Label(root, text='Tahun Masuk:').grid(row=4, column=0)
entry_tahun = Entry(root)
entry_tahun.grid(row=4, column=1)

# Tombol CRUD
Button(root, text='Tambah Pegawai', command=submit_data).grid(row=5, column=0, columnspan=2)
Button(root, text='Update Pegawai', command=update_data_button).grid(row=6, column=0, columnspan=2)
Button(root, text='Delete Pegawai', command=delete_data_button).grid(row=7, column=0, columnspan=2)
Button(root, text='Tampilkan Data', command=tampilkan_data).grid(row=8, column=0, columnspan=2)

# Tombol Reset
Button(root, text='Reset Tabel Pegawai', command=reset_table).grid(row=9, column=0, columnspan=2)

# Label hasil
label_hasil = Label(root, text='')
label_hasil.grid(row=10, column=0, columnspan=2)

label_hasil2 = Label(root, text='', justify="left")
label_hasil2.grid(row=11, column=0, columnspan=2)

root.mainloop()
