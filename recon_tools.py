import requests
import sys
import time
import socket

# --- FITUR 1: SUBDOMAIN DISCOVERY ---
def run_subdomain_discovery():
    print("\n[--- FITUR 1: SUBDOMAIN DISCOVERY ---]")
    # --- KONFIGURASI ---
    # Meminta input domain dari pengguna agar lebih fleksibel
    base_domain = input("Masukkan domain target (contoh: google.com): ")
    if not base_domain:
        print("❌ Error: Domain target tidak boleh kosong.")
        return
        
    wordlist_file = "subdomain_wordlist.txt"
    # ------------------

    print(f"🎯 Target Domain: {base_domain}")
    print(f"📖 Wordlist: {wordlist_file}\n")
    found_subdomains = []
    
    try:
        with open(wordlist_file, 'r', encoding='utf-8') as f:
            subdomains = [line.strip() for line in f]
    except FileNotFoundError:
        print(f"❌ Error: File wordlist '{wordlist_file}' tidak ditemukan.")
        print("Pastikan Anda memiliki file 'subdomain_wordlist.txt' di folder yang sama.")
        return
    except UnicodeDecodeError:
        print(f"❌ Error: File encoding tidak didukung. Pastikan file menggunakan UTF-8.")
        return

    for sub in subdomains:
        if not sub: continue # Lewati baris kosong
        target_domain = f"{sub}.{base_domain}"
        try:
            # Mencoba mendapatkan alamat IP dari subdomain. Jika berhasil, berarti subdomain ada.
            ip_address = socket.gethostbyname(target_domain)
            print(f"[+] DITEMUKAN: {target_domain} -> {ip_address}")
            found_subdomains.append(f"{target_domain} ({ip_address})")
        except socket.gaierror:
            # Jika terjadi error 'gaierror', berarti DNS lookup gagal (subdomain tidak ada).
            print(f"[-] Tidak ditemukan: {target_domain}")
        except Exception as e:
            # Menangani error lain, misalnya masalah jaringan.
            print(f"[*] Terjadi error saat memeriksa {target_domain}: {e}")

    print("\n" + "="*40)
    print("✅ Pencarian Selesai.")
    if found_subdomains:
        print("Subdomain yang berhasil ditemukan:")
        for found in found_subdomains:
            print(f"  -> {found}")
    else:
        print("Tidak ada subdomain yang ditemukan.")
    print("="*40)


# --- FITUR 2: DIRECTORY/FILE DISCOVERY ---
def run_directory_brute_force():
    print("\n[--- FITUR 2: DIRECTORY/FILE DISCOVERY ---]")
    # --- KONFIGURASI ---
    base_url = input("Masukkan URL target lengkap (contoh: https://google.com): ")
    if not base_url:
        print("❌ Error: URL target tidak boleh kosong.")
        return
    
    # Menambahkan http:// jika user lupa memasukkan
    if not base_url.startswith('http://') and not base_url.startswith('https://'):
        base_url = 'http://' + base_url
        print(f"INFO: Menambahkan 'http://'. URL target menjadi: {base_url}")

    wordlist_file = "common_dirs.txt"
    # ---------------------------------------------------

    print(f"🎯 Target URL: {base_url}")
    print(f"📖 Wordlist: {wordlist_file}\n")
    found_paths = []
    
    try:
        with open(wordlist_file, 'r', encoding='utf-8') as f:
            paths = [line.strip() for line in f]
    except FileNotFoundError as e:
        print(f"❌ Error: File tidak ditemukan - {e.filename}")
        print("Pastikan Anda memiliki file 'common_dirs.txt' di folder yang sama.")
        return
    except UnicodeDecodeError as e:
        print(f"❌ Error: File encoding tidak didukung. Pastikan file menggunakan UTF-8.")
        return

    for path in paths:
        if not path: continue # Lewati baris kosong
        # Membersihkan slash agar URL selalu benar
        target_url = f"{base_url.rstrip('/')}/{path.lstrip('/')}"
        try:
            response = requests.get(target_url, timeout=5)
            # cek status kode selain 404 (Not Found)
            if response.status_code != 404:
                print(f"[+] Ditemukan ({response.status_code}): {target_url}")
                found_paths.append(f"{target_url} (Status: {response.status_code})")
            else:
                 print(f"[-] Tidak ditemukan: {target_url}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Error koneksi saat mencoba {target_url}: {e}")

    print("\n" + "="*40)
    print("✅ Pencarian Selesai.")
    if found_paths:
        print("Path yang berhasil ditemukan:")
        for found in found_paths:
            print(f"  -> {found}")
    else:
        print("Tidak ada path yang ditemukan.")
    print("="*40)


# --- MENU UTAMA ---
def main():
    while True:
        print("\n" + "="*40)
        print("  Reconnaissance Tool (by labim_)".center(38))
        print("="*40)
        print("  1. Subdomain Discovery")
        print("  2. Directory/File Discovery")
        print("  3. Keluar")
        print("="*40)
        
        choice = input("Masukkan pilihan Anda (1/2/3): ")
        
        if choice == '1':
            run_subdomain_discovery()
        elif choice == '2':
            run_directory_brute_force()
        elif choice == '3':
            print("👋 Sampai jumpa!")
            break
        else:
            print("❌ Pilihan tidak valid. Silakan coba lagi.")
        
        input("\nTekan Enter untuk kembali ke menu utama...")


if __name__ == '__main__':
    main()