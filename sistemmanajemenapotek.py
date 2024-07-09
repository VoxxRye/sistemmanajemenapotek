from datetime import datetime
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox

# tampilan jendela
ws  = Tk()
ws.geometry('800x500')
ws.title("Program Utama Apotek")
ws['bg'] = '#ffc8dd'

my_title = ttk.Label(ws, text='Selamat Bekerja!', font=('bold', 20))
my_title.configure(background=ws['bg'])
my_title.pack(pady=20)

# fungsi untuk window baru
def data_supplier_window():
    # tampilan jendela
    ws  = Tk()
    ws.title('Data Supplier')
    ws.geometry('800x500')
    ws['bg'] = '#ffc8dd'

    my_title = ttk.Label(ws, text='Daftar Supplier Apotek', font=(20))
    my_title.configure(background=ws['bg'])
    my_title.pack(pady=20)

    # frame untuk input
    frame_input = Frame(ws)
    frame_input.pack(pady=20)

    labels = ['Kode Supplier', 'Nama Supplier', 'Alamat Supplier', 'Nomor Telepon', 'Nama obat']

    list_text_input =[]

    for index, label_text in enumerate(labels):
        label = Label(frame_input, text=label_text)
        label.grid(row=0, column=index)
        text_input = Entry(frame_input)
        text_input.grid(row=1, column=index)
        list_text_input.append(text_input)

        frame_input.columnconfigure(index, minsize=50)



    # membuat tabel data Supplier
    data_frame = Frame(ws)
    data_frame.pack(pady=20)

    data_suplier = ttk.Treeview(data_frame)
    data_suplier['columns'] = ('Kode', 'Nama Supplier', 'Alamat', 'No HP', 'Nama obat')

    data_suplier.column('#0', width=0, stretch=NO)

    # looping untuk membuat kolom data
    for label in data_suplier['columns']:
        data_suplier.column(label, anchor=CENTER, width=150)
        data_suplier.heading(label, text=label, anchor=CENTER)

    data_suplier.pack()

    list_suplier = [
        [1, 'Adi', 'Karawang', '0813', 'Paramex'],
    ]

    global count
    count = 0

    # memasukan data ke tabel
    for i in list_suplier:
        data_suplier.insert(parent='', index='end', id=count, values=(i[0], i[1], i[2], i[3], i[4]))
        count += 1

    def update_treeview():
        data_suplier.delete(*data_suplier.get_children())
        for i in list_suplier:
            data_suplier.insert(parent='', index='end', values=i)

    # Fungsi yang akan dipanggil saat tombol "Input Record" ditekan
    def input_record():
        global count
        entry_values = [text_input.get() for text_input in list_text_input]
        list_suplier.append(entry_values)
        count += 1
        update_treeview()  # Memanggil fungsi untuk memperbarui Treeview
        # Menghapus data dari setiap kotak masukan
        for text_input in list_text_input:
            text_input.delete(0, END)
        
    #button
    Input_button = Button(ws,text = "Input Record",command= input_record)
    Input_button.pack()


    ws.mainloop()

def transaksi_pembelian_window():
    
    def tambah_transaksi():
        input_win = tk.Toplevel()
        input_win.title("Tambah Transaksi")
        hilangkan_seleksi()  # Memanggil fungsi untuk menghilangkan seleksi

        labels = ["Kode Pembelian", "Kode Obat", "Nama Obat", "Nama Supplier", "Harga", "Jumlah Beli"]
        entries = {}
        for i, label in enumerate(labels):
            tk.Label(input_win, text=label).grid(row=i, column=0, sticky="w")
            entry = tk.Entry(input_win)
            entry.grid(row=i, column=1)
            entries[label] = entry

        def simpan_transaksi():
            try:
                # Mendapatkan tanggal dan waktu saat ini
                current_date = datetime.now().strftime("%Y-%m-%d")
                
                data = [entry.get() for entry in entries.values()]
                subtotal = int(data[4]) * int(data[5])
                # Menambahkan subtotal dan tanggal transaksi ke data
                data.extend([subtotal, current_date])
                table.insert('', 'end', values=data)
                input_win.destroy()
            except ValueError:
                messagebox.showerror("Error", "Harga dan Jumlah Beli harus berupa angka.")

        tk.Button(input_win, text="Simpan Transaksi", command=simpan_transaksi).grid(row=len(labels), column=1)

    # Fungsi untuk mengubah transaksi
    def ubah_transaksi():
        selected_item = table.focus()
        if not selected_item:
            messagebox.showerror("Error", "Pilih transaksi yang ingin diubah.")
            return

        data = table.item(selected_item, 'values')
        input_win = tk.Toplevel()
        input_win.title("Ubah Transaksi")

        labels = ["Kode Pembelian", "Kode Obat", "Nama Obat", "Nama Supplier", "Harga", "Jumlah Beli", "Tanggal Transaksi"]
        entries = {}
        for i, label in enumerate(labels):
            tk.Label(input_win, text=label).grid(row=i, column=0, sticky="w")
            entry = tk.Entry(input_win)
            if label == "Tanggal Transaksi":
                entry.insert(0, data[7])
                entry.config()
            else:
                entry.insert(0, data[i])
            entry.grid(row=i, column=1)
            entries[label] = entry

        def simpan_perubahan():
            try:
                updated_data = [entry.get() for entry in entries.values()]
                # Perhitungan subtotal baru
                subtotal = int(updated_data[4]) * int(updated_data[5])
                # Memperbarui data dengan subtotal yang baru dihitung
                updated_data = updated_data[:6] + [str(subtotal), updated_data[6]]
                table.item(selected_item, values=updated_data)
                hilangkan_seleksi()  # Memanggil fungsi untuk menghilangkan seleksi
                input_win.destroy()
            except ValueError:
                messagebox.showerror("Error", "Harga dan Jumlah Beli harus berupa angka.")

        tk.Button(input_win, text="Simpan Perubahan", command=simpan_perubahan).grid(row=len(labels), column=1)

    # Fungsi untuk menghapus transaksi
    def hapus_transaksi():
        selected_item = table.focus()
        if not selected_item:
            messagebox.showerror("Error", "Pilih transaksi yang ingin dihapus.")
            return

        confirm = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus transaksi ini?")
        if confirm:
            table.delete(selected_item)

    # Fungsi untuk mengurutkan kolom tanggal
    def sort_by_date(col, reverse):
        l = [(table.set(k, col), k) for k in table.get_children('')]
        l.sort(reverse=reverse)

        # Rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            table.move(k, '', index)

        # Reverse sort next time
        table.heading(col, command=lambda: sort_by_date(col, not reverse))

    # Fungsi untuk mencari transaksi berdasarkan nama obat
    def cari_transaksi(nama_obat):
        for item in table.get_children():
            if nama_obat.lower() in table.item(item)['values'][2].lower():
                table.selection_set(item)
            else:
                table.selection_remove(item)

    # Fungsi untuk menghilangkan seleksi pada item transaksi
    def hilangkan_seleksi():
        selected_items = table.selection()
        for item in selected_items:
            table.selection_remove(item)            

    # Membuat jendela utama
    root = tk.Tk()
    root.title("Transaksi Pembelian")
    root.configure(bg="pink")

    frame = tk.Frame(root)
    frame.pack(padx=30)

    columns = ("Kode Pembelian", "Kode Obat", "Nama Obat", "Nama Supplier", "Harga", "Jumlah Beli", "Subtotal", "Tanggal Transaksi")
    table = ttk.Treeview(frame, columns=columns, show='headings', height=10)

    # Contoh data transaksi
    contoh_data = {
        "Kode Penjualan": "1",
        "Kode Obat": "OBT015",
        "Nama Obat": "Paramex",
        "Nama Supplier": "Adi",
        "Harga": 10000,
        "Jumlah Terjual": 50,
        "Subtotal": 500000,  # Dihasilkan dari Harga * Jumlah Terjual
        "Tanggal Transaksi": "2024-06-15"
    }

    # Fungsi untuk menambahkan data contoh ke dalam tabel
    def tambah_data_contoh():
        table.insert('', 'end', values=(
            contoh_data["Kode Penjualan"],
            contoh_data["Kode Obat"],
            contoh_data["Nama Obat"],
            contoh_data["Nama Supplier"],
            contoh_data["Harga"],
            contoh_data["Jumlah Terjual"],
            contoh_data["Subtotal"],
            contoh_data["Tanggal Transaksi"]
        ))

    # Memanggil fungsi untuk menambahkan data contoh ke dalam tabel
    tambah_data_contoh()

    # Mengatur lebar kolom
    table.column("Kode Pembelian", width=125)
    table.column("Kode Obat", width=125)
    table.column("Nama Obat", width=125)
    table.column("Nama Supplier", width=125)
    table.column("Harga", width=125)
    table.column("Jumlah Beli", width=125)
    table.column("Subtotal", width=125)
    table.column("Tanggal Transaksi", width=125)

    for col in columns:
        table.heading(col, text=col)
        table.column(col, anchor="center")

    table.heading('Tanggal Transaksi', text='Tanggal Transaksi', command=lambda: sort_by_date('Tanggal Transaksi', False))

    table.pack()

    # Membuat search box
    search_frame = tk.Frame(root)
    search_frame.pack(before=frame, pady=30)

    search_label = tk.Label(search_frame, text="Masukkan Nama Obat:")
    search_label.pack(side='left')

    search_entry = tk.Entry(search_frame)
    search_entry.pack(side='left')

    search_button = tk.Button(search_frame, text="Cari", command=lambda: cari_transaksi(search_entry.get()))
    search_button.pack(side='left')

    button_frame = tk.Frame(root, bg='pink')
    button_frame.pack()

    add_button = tk.Button(button_frame, text="Tambah Transaksi", command=tambah_transaksi)
    add_button.pack(side='left', expand=True, padx=30, pady=30)

    update_button = tk.Button(button_frame, text="Ubah Transaksi", command=ubah_transaksi)
    update_button.pack(side='left', expand=True, padx=30, pady=30)

    delete_button = tk.Button(button_frame, text="Hapus Transaksi", command=hapus_transaksi)
    delete_button.pack(side='left', expand=True, padx=30, pady=30)

    # Membuat judul/heading untuk jendela utama
    judul_frame = tk.Frame(root)
    judul_frame.pack(before=search_frame, pady=15)
    judul_label = tk.Label(judul_frame, text='Transaksi Pembelian', font=('Helvetica', 20, 'bold'), bg='pink')
    judul_label.pack()

    root.mainloop()       

def transaksi_penjualan_window():
    
    def tambah_transaksi():
        input_win = tk.Toplevel()
        input_win.title("Tambah Transaksi")
        hilangkan_seleksi()  # Memanggil fungsi untuk menghilangkan seleksi

        labels = ["Kode Penjualan", "Kode Obat", "Nama Obat", "Harga", "Jumlah Terjual"]
        entries = {}
        for i, label in enumerate(labels):
            tk.Label(input_win, text=label).grid(row=i, column=0, sticky="w")
            entry = tk.Entry(input_win)
            entry.grid(row=i, column=1)
            entries[label] = entry

        def simpan_transaksi():
            try:
                # Mendapatkan tanggal dan waktu saat ini
                current_date = datetime.now().strftime("%Y-%m-%d")
                
                data = [entry.get() for entry in entries.values()]
                subtotal = int(data[3]) * int(data[4])
                # Menambahkan subtotal dan tanggal transaksi ke data
                data.extend([subtotal, current_date])
                table.insert('', 'end', values=data)
                input_win.destroy()
            except ValueError:
                messagebox.showerror("Error", "Harga dan Jumlah Terjual harus berupa angka.")

        tk.Button(input_win, text="Simpan Transaksi", command=simpan_transaksi).grid(row=len(labels), column=1)

    # Fungsi untuk mengubah transaksi
    def ubah_transaksi():
        selected_item = table.focus()
        if not selected_item:
            messagebox.showerror("Error", "Pilih transaksi yang ingin diubah.")
            return

        data = table.item(selected_item, 'values')
        input_win = tk.Toplevel()
        input_win.title("Ubah Transaksi")

        labels = ["Kode Penjualan", "Kode Obat", "Nama Obat", "Harga", "Jumlah Terjual", "Tanggal Transaksi"]
        entries = {}
        tanggal_var = StringVar(input_win)  # Membuat StringVar untuk tanggal transaksi
        tanggal_var.set(data[6])  # Mengatur nilai default dari StringVar
        for i, label in enumerate(labels):
            tk.Label(input_win, text=label).grid(row=i, column=0, sticky="w")
            if label == "Tanggal Transaksi":
                entry = tk.Entry(input_win, textvariable=tanggal_var)
            else:
                entry = tk.Entry(input_win)
                entry.insert(0, data[i])
            entry.grid(row=i, column=1)
            entries[label] = entry

        def simpan_perubahan():
            try:
                updated_data = [entry.get() for label, entry in entries.items()]
                # Perhitungan subtotal dilakukan di sini tapi tidak ditambahkan ke form
                subtotal = int(updated_data[3]) * int(updated_data[4])
                # Menambahkan subtotal dan tanggal transaksi ke data yang akan disimpan
                updated_data = updated_data[:5] + [subtotal, updated_data[5]]
                table.item(selected_item, values=updated_data)
                hilangkan_seleksi()  # Memanggil fungsi untuk menghilangkan seleksi
                input_win.destroy()
            except ValueError:
                messagebox.showerror("Error", "Harga dan Jumlah Terjual harus berupa angka.")

        tk.Button(input_win, text="Simpan Perubahan", command=simpan_perubahan).grid(row=len(labels), column=1)

    # Fungsi untuk menghapus transaksi
    def hapus_transaksi():
        selected_item = table.focus()
        if not selected_item:
            messagebox.showerror("Error", "Pilih transaksi yang ingin dihapus.")
            return

        confirm = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus transaksi ini?")
        if confirm:
            table.delete(selected_item)

    # Fungsi untuk mengurutkan kolom tanggal
    def sort_by_date(col, reverse):
        l = [(table.set(k, col), k) for k in table.get_children('')]
        l.sort(reverse=reverse)

        # Rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            table.move(k, '', index)

        # Reverse sort next time
        table.heading(col, command=lambda: sort_by_date(col, not reverse))

    # Fungsi untuk mencari transaksi berdasarkan nama obat
    def cari_transaksi(nama_obat):
        for item in table.get_children():
            if nama_obat.lower() in table.item(item)['values'][2].lower():
                table.selection_set(item)
            else:
                table.selection_remove(item)

    # Fungsi untuk menghilangkan seleksi pada item transaksi
    def hilangkan_seleksi():
        selected_items = table.selection()
        for item in selected_items:
            table.selection_remove(item)            

    # Membuat jendela utama
    root = tk.Tk()
    root.title("Transaksi Penjualan")
    root.configure(bg="pink")

    frame = tk.Frame(root)
    frame.pack(padx=30)

    columns = ("Kode Penjualan", "Kode Obat", "Nama Obat", "Harga", "Jumlah Terjual", "Subtotal", "Tanggal Transaksi")
    table = ttk.Treeview(frame, columns=columns, show='headings', height=10)

    # Contoh data transaksi
    contoh_data = {
        "Kode Penjualan": "1",
        "Kode Obat": "OBT001",
        "Nama Obat": "Paracetamol",
        "Harga": 5000,
        "Jumlah Terjual": 20,
        "Subtotal": 100000,  # Dihasilkan dari Harga * Jumlah Terjual
        "Tanggal Transaksi": "2024-06-11"
    }

    # Fungsi untuk menambahkan data contoh ke dalam tabel
    def tambah_data_contoh():
        table.insert('', 'end', values=(
            contoh_data["Kode Penjualan"],
            contoh_data["Kode Obat"],
            contoh_data["Nama Obat"],
            contoh_data["Harga"],
            contoh_data["Jumlah Terjual"],
            contoh_data["Subtotal"],
            contoh_data["Tanggal Transaksi"]
        ))

    # Memanggil fungsi untuk menambahkan data contoh ke dalam tabel
    tambah_data_contoh()

    # Mengatur lebar kolom
    table.column("Kode Penjualan", width=125)
    table.column("Kode Obat", width=125)
    table.column("Nama Obat", width=125)
    table.column("Harga", width=125)
    table.column("Jumlah Terjual", width=125)
    table.column("Subtotal", width=125)
    table.column("Tanggal Transaksi", width=125)

    for col in columns:
        table.heading(col, text=col)
        table.column(col, anchor="center")

    table.heading('Tanggal Transaksi', text='Tanggal Transaksi', command=lambda: sort_by_date('Tanggal Transaksi', False))

    table.pack()

    # Membuat search box
    search_frame = tk.Frame(root)
    search_frame.pack(before=frame, pady=30)

    search_label = tk.Label(search_frame, text="Masukkan Nama Obat:")
    search_label.pack(side='left')

    search_entry = tk.Entry(search_frame)
    search_entry.pack(side='left')

    search_button = tk.Button(search_frame, text="Cari", command=lambda: cari_transaksi(search_entry.get()))
    search_button.pack(side='left')

    button_frame = tk.Frame(root, bg='pink')
    button_frame.pack()

    add_button = tk.Button(button_frame, text="Tambah Transaksi", command=tambah_transaksi)
    add_button.pack(side='left', expand=True, padx=30, pady=30)

    update_button = tk.Button(button_frame, text="Ubah Transaksi", command=ubah_transaksi)
    update_button.pack(side='left', expand=True, padx=30, pady=30)

    delete_button = tk.Button(button_frame, text="Hapus Transaksi", command=hapus_transaksi)
    delete_button.pack(side='left', expand=True, padx=30, pady=30)

    # Membuat judul/heading untuk jendela utama
    judul_frame = tk.Frame(root)
    judul_frame.pack(before=search_frame, pady=15)
    judul_label = tk.Label(judul_frame, text='Transaksi Penjualan', font=('Helvetica', 20, 'bold'), bg='pink')
    judul_label.pack()

    root.mainloop()
    
def data_obat_window():
# Inisialisasi data obat
    obat_data = [
        ('OBT001', 'Paracetamol', 5000, 50, 'Pereda demam', 'Analgesik', '2023-12-31'),
        ('OBT002', 'Ibuprofen', 10000, 100, 'Anti-inflamasi', 'Anti-inflamasi', '2024-06-30'),
        ('OBT003', 'Amoxicillin', 20000, 200, 'Antibiotik', 'Antibiotik', '2025-01-01'),
        ('OBT004', 'Cetirizine', 15000, 75, 'Antihistamin', 'Antialergi', '2024-08-15'),
        ('OBT005', 'Omeprazole', 25000, 60, 'Penghambat asam lambung', 'Gastrointestinal', '2025-03-10')
    ]

    def tambah_obat():
        # Mendapatkan nilai dari input pengguna
        kode_obat = entry_kode.get()
        nama_obat = entry_nama.get()
        harga_jual = entry_harga_jual.get()
        stok = entry_stok.get()
        keterangan = entry_keterangan.get()
        kategori = entry_kategori.get()
        tanggal_expired = entry_tanggal_expired.get()
        
        # Memastikan semua input diisi
        if kode_obat and nama_obat and harga_jual and stok and keterangan and kategori and tanggal_expired:
            # Menambahkan data ke obat_data
            new_obat = (kode_obat, nama_obat, int(harga_jual), int(stok), keterangan, kategori, tanggal_expired)
            obat_data.append(new_obat)
            
            # Menambahkan data ke tabel
            my_table.insert('', 'end', values=new_obat)
            
            # Menampilkan pesan sukses
            messagebox.showinfo("Sukses", "Obat berhasil ditambahkan!")
            
            # Mengosongkan input setelah ditambahkan
            entry_kode.delete(0, 'end')
            entry_nama.delete(0, 'end')
            entry_harga_jual.delete(0, 'end')
            entry_stok.delete(0, 'end')
            entry_keterangan.delete(0, 'end')
            entry_kategori.delete(0, 'end')
            entry_tanggal_expired.delete(0, 'end')
        else:
            # Menampilkan pesan kesalahan jika ada input yang kosong
            messagebox.showerror("Error", "Silakan isi semua kolom.")

    def update_obat():
        selected_item = my_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "Pilih data obat yang ingin diperbarui.")
            return

        # Mendapatkan nilai dari input pengguna
        kode_obat = entry_kode.get()
        nama_obat = entry_nama.get()
        harga_jual = entry_harga_jual.get()
        stok = entry_stok.get()
        keterangan = entry_keterangan.get()
        kategori = entry_kategori.get()
        tanggal_expired = entry_tanggal_expired.get()

        # Memastikan semua input diisi
        if kode_obat and nama_obat and harga_jual and stok and keterangan and kategori and tanggal_expired:
            # Mengambil indeks obat yang dipilih
            obat_index = int(selected_item[0])
            
            # Memperbarui data obat
            obat_data[obat_index] = (kode_obat, nama_obat, int(harga_jual), int(stok), keterangan, kategori, tanggal_expired)

            # Memperbarui data dalam tabel
            my_table.item(selected_item, values=(kode_obat, nama_obat, int(harga_jual), int(stok), keterangan, kategori, tanggal_expired))

            # Menampilkan pesan sukses
            messagebox.showinfo("Sukses", "Obat berhasil diperbarui!")

            # Mengosongkan input setelah diperbarui
            entry_kode.delete(0, 'end')
            entry_nama.delete(0, 'end')
            entry_harga_jual.delete(0, 'end')
            entry_stok.delete(0, 'end')
            entry_keterangan.delete(0, 'end')
            entry_kategori.delete(0, 'end')
            entry_tanggal_expired.delete(0, 'end')
        else:
            # Menampilkan pesan kesalahan jika ada input yang kosong
            messagebox.showerror("Error", "Silakan isi semua kolom.")


    def hapus_obat():
        selected_item = my_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "Pilih data obat yang ingin dihapus.")
            return
        
        for item in selected_item:
            my_table.delete(item)
            
            # Hapus data dari obat_data
            obat_index = int(item)
            del obat_data[obat_index]
            
        messagebox.showinfo("Sukses", "Obat berhasil dihapus!")

    def cari_obat():
        # Mendapatkan nilai dari input pencarian
        nama_obat_cari = entry_cari.get()
        
        # Membersihkan tabel sebelum menampilkan hasil pencarian
        for item in my_table.get_children():
            my_table.delete(item)
        
        # Memfilter data obat berdasarkan nama obat yang dicari
        hasil_pencarian = [obat for obat in obat_data if nama_obat_cari.lower() in obat[1].lower()]
        
        # Menambahkan hasil pencarian ke dalam tabel
        for i, data in enumerate(hasil_pencarian):
            my_table.insert(parent='', index='end', iid=i, text='', values=data)
        
        # Menampilkan pesan jika tidak ada hasil ditemukan
        if not hasil_pencarian:
            messagebox.showinfo("Info", "Tidak ada obat ditemukan dengan nama tersebut.")

    def exit_program():
        ws.quit()

    # Inisialisasi jendela utama
    ws = tk.Tk()
    ws.title('Manajemen Data Obat')
    ws.geometry('1000x600')
    ws['bg'] = '#FFC0CB'  # Warna pink

    # Frame utama untuk menggabungkan tabel dan form input
    main_frame = tk.Frame(ws, bg='#FFC0CB')
    main_frame.pack(pady=20, padx=20, fill='both', expand=True)

    # Frame untuk tabel
    table_frame = tk.Frame(main_frame, bg='#FFC0CB')
    table_frame.pack(side=tk.LEFT, fill='both', expand=True, padx=(0, 20))

    # Label Data Obat
    tk.Label(table_frame, text="Data Obat", bg='#FFC0CB', font=("Helvetica", 16)).pack(pady=10)

    # Treeview untuk tabel data obat
    my_table = ttk.Treeview(table_frame)

    # Definisi kolom
    my_table['columns'] = ('Kode Obat', 'Nama obat', 'Harga jual', 'Stok', 'Keterangan', 'Kategori', 'Tanggal expired')

    my_table.column("#0", width=0, stretch=tk.NO)
    my_table.heading("#0", text="", anchor=tk.CENTER)
    # Format kolom dan heading
    for i in my_table['columns']:
        my_table.column(i, anchor=tk.CENTER, width=100)
        my_table.heading(i, text=i, anchor=tk.CENTER)

    # Menambahkan data awal ke dalam tabel
    for i, data in enumerate(obat_data):
        my_table.insert(parent='', index='end', iid=i, text='', values=data)

    # Menampilkan tabel
    my_table.pack(fill='both', expand=True)

    # Frame untuk form input
    frame_input = tk.Frame(main_frame, bg='#FFC0CB')
    frame_input.pack(side=tk.RIGHT, fill='y', expand=True)

    # Frame untuk form tambah obat
    frame_tambah_obat = tk.Frame(frame_input, bg='#FFC0CB', bd=2, relief=tk.RIDGE)
    frame_tambah_obat.pack(pady=50, fill='x')

    for index, label in enumerate(my_table['columns']):
        tk.Label(frame_tambah_obat, text=label, bg='#FFC0CB').grid(row=index, column=0, padx=10, pady=5)

    # entry box obat
    entry_kode = tk.Entry(frame_tambah_obat)
    entry_nama = tk.Entry(frame_tambah_obat)
    entry_harga_jual = tk.Entry(frame_tambah_obat)
    entry_stok = tk.Entry(frame_tambah_obat)
    entry_keterangan = tk.Entry(frame_tambah_obat)
    entry_kategori = tk.Entry(frame_tambah_obat)
    entry_tanggal_expired = tk.Entry(frame_tambah_obat)

    entry_kode.grid(row=0, column=1, padx=10, pady=5)
    entry_nama.grid(row=1, column=1, padx=10, pady=5)
    entry_harga_jual.grid(row=2, column=1, padx=10, pady=5)
    entry_stok.grid(row=3, column=1, padx=10, pady=5)
    entry_keterangan.grid(row=4, column=1, padx=10, pady=5)
    entry_kategori.grid(row=5, column=1, padx=10, pady=5)
    entry_tanggal_expired.grid(row=6, column=1, padx=10, pady=5)

    # Tombol untuk menambahkan obat
    tk.Button(frame_tambah_obat, text='Tambah Obat', command=tambah_obat).grid(row=7, column=1, padx=10, pady=10)

    # Tombol untuk memperbarui obat
    tk.Button(frame_tambah_obat, text='Update Obat', command=update_obat).grid(row=7, column=2, padx=10, pady=10)

    # Frame untuk fitur hapus obat
    frame_hapus_obat = tk.Frame(frame_input, bg='#FFC0CB', bd=2, relief=tk.RIDGE)
    frame_hapus_obat.pack(pady=20, fill='x')

    # Label dan tombol hapus obat
    tk.Label(frame_hapus_obat, text="Hapus Obat yang dipilih dari tabel", bg='#FFC0CB').grid(row=0, column=0, padx=10, pady=5)
    tk.Button(frame_hapus_obat, text='Hapus Obat', command=hapus_obat).grid(row=0, column=8, padx=10, pady=5)

    # Frame untuk pencarian
    frame_cari = tk.Frame(frame_input, bg='#FFC0CB', bd=2, relief=tk.RIDGE)
    frame_cari.pack(pady=20, fill='x')

    tk.Label(frame_cari, text="Cari Nama Obat", bg='#FFC0CB').grid(row=0, column=0, padx=10, pady=5)
    entry_cari = tk.Entry(frame_cari)
    entry_cari.grid(row=0, column=1, padx=10, pady=5)

    # Tombol untuk mencari obat
    tk.Button(frame_cari, text='Cari Obat', command=cari_obat).grid(row=0, column=2, padx=10, pady=5)

    # Tombol Exit di pojok kanan bawah
    exit_button = tk.Button(ws, text='Keluar', command=exit_program, bg='#D3D3D3', fg='black')
    exit_button.pack(side=tk.BOTTOM, anchor=tk.SE, padx=10, pady=10)

    # Menjalankan aplikasi
    ws.mainloop()

# Membuat tombol Transaksi Data Obat
button1 = Button(ws, text='Data Obat', command=data_obat_window)
button1.pack(side='left', expand=True, padx=30)

# Membuat tombol Data Supplier
button2 = Button(ws, text='Data Supplier', command=data_supplier_window)
button2.pack(side='left', expand=True, padx=30)

# Membuat tombol Transaksi Pembelian
button3 = Button(ws, text='Transaksi Pembelian', command=transaksi_pembelian_window)
button3.pack(side='left', expand=True, padx=30)

# Membuat tombol Transaksi Penjualan
button4 = Button(ws, text='Transaksi Penjualan', command=transaksi_penjualan_window)
button4.pack(side='left', expand=True, padx=30)

ws.mainloop()