from datetime import datetime
import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")

saldo = 0
riwayat_transaksi = []


def load_data():
    """Muat data dari file JSON jika ada."""
    global saldo, riwayat_transaksi
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                saldo = data.get("saldo", 0)
                riwayat_transaksi = data.get("riwayat_transaksi", [])
        except Exception as e:
            print(f"⚠️ Gagal memuat data: {e}")


def save_data():
    """Simpan data saldo dan riwayat ke file JSON."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({"saldo": saldo, "riwayat_transaksi": riwayat_transaksi}, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"⚠️ Gagal menyimpan data: {e}")


def tambah_pemasukan():
    try:
        print("\n=== Tambah Pemasukan ===")
        deskripsi = input("Deskripsi pemasukan: ")
        jumlah = float(input("Jumlah uang: Rp "))
       
        if jumlah <= 0:
            print("❌ Jumlah harus lebih dari 0!")
            return
       
        global saldo
        saldo += jumlah
       
        transaksi = {
            "tanggal": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "tipe": "Pemasukan",
            "deskripsi": deskripsi,
            "jumlah": jumlah,
            "saldo_setelah": saldo
        }
        riwayat_transaksi.append(transaksi)
        save_data()
       
        print(f"✅ Pemasukan berhasil ditambahkan! Saldo sekarang: Rp {saldo:,.0f}")
    except ValueError:
        print("❌ Input tidak valid! Masukkan angka untuk jumlah uang.")


def tambah_pengeluaran():
    try:
        print("\n=== Tambah Pengeluaran ===")
        deskripsi = input("Deskripsi pengeluaran: ")
        jumlah = float(input("Jumlah uang: Rp "))
       
        if jumlah <= 0:
            print("❌ Jumlah harus lebih dari 0!")
            return
       
        global saldo
        if saldo < jumlah:
            kurang = jumlah - saldo
            print("\n" + "⚠️  " + "─" * 50)
            print("⚠️  PERINGATAN: SALDO TIDAK CUKUP!")
            print("⚠️  " + "─" * 50)
            print(f"  Saldo saat ini     : Rp {saldo:,.0f}")
            print(f"  Jumlah pengeluaran : Rp {jumlah:,.0f}")
            print(f"  Kekurangan uang    : Rp {kurang:,.0f}")
            print("⚠️  " + "─" * 50)
            print("❌ Pengeluaran dibatalkan!\n")
            return
       
        saldo -= jumlah
       
        transaksi = {
            "tanggal": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "tipe": "Pengeluaran",
            "deskripsi": deskripsi,
            "jumlah": jumlah,
            "saldo_setelah": saldo
        }
        riwayat_transaksi.append(transaksi)
        save_data()
       
        print(f"✅ Pengeluaran berhasil ditambahkan! Saldo sekarang: Rp {saldo:,.0f}")
    except ValueError:
        print("❌ Input tidak valid! Masukkan angka untuk jumlah uang.")


def lihat_saldo():
    print(f"\n=== Saldo Saat Ini ===")
    print(f"💰 Rp {saldo:,.0f}\n")


def laporan_keuangan():
    print("\n=== LAPORAN KEUANGAN ===")
   
    if not riwayat_transaksi:
        print("Belum ada transaksi.")
        print("────────────────────────────────────────────────────")
        return
   
    total_pemasukan = 0
    total_pengeluaran = 0
   
    print("────────────────────────────────────────────────────")
    print(f"{'Tanggal':<18} {'Tipe':<12} {'Deskripsi':<20} {'Jumlah':>12}")
    print("────────────────────────────────────────────────────")
   
    for transaksi in riwayat_transaksi:
        tanggal = transaksi["tanggal"]
        tipe = transaksi["tipe"]
        deskripsi = transaksi["deskripsi"][:19]
        jumlah = transaksi["jumlah"]
       
        if tipe == "Pemasukan":
            total_pemasukan += jumlah
            print(f"{tanggal:<18} {tipe:<12} {deskripsi:<20} +Rp {jumlah:>10,.0f}")
        else:
            total_pengeluaran += jumlah
            print(f"{tanggal:<18} {tipe:<12} {deskripsi:<20} -Rp {jumlah:>10,.0f}")
   
    print("────────────────────────────────────────────────────")
    print(f"{'Total Pemasukan':<48} +Rp {total_pemasukan:>10,.0f}")
    print(f"{'Total Pengeluaran':<48} -Rp {total_pengeluaran:>10,.0f}")
    print(f"{'Saldo Akhir':<48} =Rp {saldo:>10,.0f}")
    print("────────────────────────────────────────────────────\n")


def menu():
    print("\n╔════════════════════════════════════════╗")
    print("║   APLIKASI PENGELOLA UANG SAKU   ║")
    print("╚════════════════════════════════════════╝")
    print("1. Tambah pemasukan")
    print("2. Tambah pengeluaran")
    print("3. Lihat saldo")
    print("4. Laporan keuangan")
    print("5. Keluar")
    print("──────────────────────────────────────────")


if __name__ == "__main__":
    load_data()
    while True:
        menu()
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            tambah_pemasukan()
        elif pilihan == "2":
            tambah_pengeluaran()
        elif pilihan == "3":
            lihat_saldo()
        elif pilihan == "4":
            laporan_keuangan()
        elif pilihan == "5":
            print("\nTerima kasih! Sampai jumpa lagi!")
            break
        else:
            print("❌ Pilihan tidak valid! Silakan coba lagi.")


