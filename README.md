# Persona - Penerapan String Matching dan Regular Expression dalam Pembangunan Deadline Reminder Assistant
> Persona - Penerapan String Matching dan Regular Expression dalam Pembangunan Deadline Reminder Assistant

## Daftar Isi
* [Algoritma KMP, BM, dan Regex](#algoritma-kmp-bm-dan-regex)
* [Prerequisites](#prerequisites)
* [Setup](#setup)
* [Cara Menggunakan Program](#cara-menggunakan-program)
* [Identitas Pembuat](#identitas-pembuat)

## Algoritma KMP, BM, dan Regex
Algoritma KMP merupakan algoritma yang digunakan untuk melakukan proses pencocokan string. Algoritma ini merupakan jenis Exact String Matching Algorithm yang merupakan pencocokan string secara tepat dengan susunan karakter dalam string yang dicocokkan memiliki jumlah maupun urutan karakter dalam string yang sama. Contoh : kata algoritmik akan menunjukkan kecocokan hanya dengan kata algoritmik. Pada algoritma KMP, kita simpan informasi yang digunakan untuk melakukan pergeseran lebih jauh, tidak hanya satu karakter seperti algoritma Brute Force. Algoritma ini melakukan pencocokan dari kiri ke kanan.

Algoritma Boyer-Moore melakukan pencocokan karakter dimulai dari kanan ke kiri. Karakter paling kanan pada pola merupakan karakter pertama yang akan dicocokkan dengan teks. Algoritma ini mempunyai dua fase, yaitu fase preprocessing dan fase pencarian. Pada fase preprocessing terdapat dua buah fungsi untuk menggeser pola ke arah kanan. Kedua fungsi ini disebut good-suffix-shift dan badcharacter-shift. Fungsi good-suffix-shift disimpan ke dalam sebuah tabel bmGs berukuran m+1. Sedangkan fungsi bad-character-shift disimpan ke dalam sebuah tabel bmBc yang berukuran n.

Pembentukan tabel bmBc dan bmGs mempunyai kompleksitas waktu O(m+n) dan kompleksitas ruang O(m+n). Sedangkan kompleksitas waktu untuk fase pencarian adalah O(mn) . Kasus terbaik untuk algoritma ini mempunyai kompleksitas waktu O(n/m) sedangkan pada kasus terburuk akan terjadi sebanyak 3n kali perbandingan untuk pencarian dengan pola yang tidak berulang (periodik).

Regular expression (regex) merupakan sekumpulan notasi dan karakter yang digunakan untuk mendeskripsikan suatu pola pada pencarian berbasis huruf. Dengan regex dimungkinkan untuk mengenali suatu string yang mempunya karakteristik dan pola tertentu, seperti email, tanggal, nomor kartu kredit, dll. Misal dengan notasi regex p.+ing maka akan menyaring semua kata-kata kecuali kata yang diawali huruf "p" dan mempunyai akhiran ing, seperti playing, praying, pulling, dll.

## Prerequisites
* [Python 3.9.4](https://www.python.org/downloads/release/python-394/) (versi yang digunakan pembuat).
* [Flask 1.1.2](https://pypi.org/project/Flask/) (library python) beserta segala prerequisitenya.
* [Flask-SQLAlchemy 2.5.1](https://pypi.org/project/Flask-SQLAlchemy/) (library python) beserta segala prerequisitenya.
* Browser yang men-support JavaScript.

Catatan: Penggunaan versi yang lebih lawas dari prerequisite-prerequisite Python di atas tidak disarankan oleh pembuat Persona. Meskipun demikian, Python pada umumnya cukup backward-compatible dan versi lawas seharusnya tetap bisa digunakan untuk menjalankan Persona.

## Setup
1. Install [Python 3.9.4](https://www.python.org/downloads/release/python-394/).
2. Buka Command Prompt, jalankan perintah `pip install Flask` dan `pip install Flask-SQLAlchemy` untuk menginstall prerequisites yang diperlukan.
3. Jalankan backend Persona melalui Command Prompt dengan melakukan navigasi ke direktori yang menyimpan app.py, lalu menuliskan `flask run`. Jika pada Command Prompt ditampilkan IP Address + port lokal (contoh: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)), maka instalasi berhasil dilakukan. Matikan backend persona dengan menekan Ctrl+C untuk menutup Flask.

## Cara Menggunakan Program
Untuk menggunakan Persona, buka [http://127.0.0.1:5000/](http://127.0.0.1:5000/) pada browser yang men-support JavaScript. Ketik "help" untuk melihat apa saja yang bisa diterima Persona.

Catatan: Persona menggunakan algoritma KMP, BM, dan Regex untuk mengolah masukan chat dari pengguna. Contoh yang diberikan pada "help" tidak baku, dan pengguna bisa chatting dengan Persona menggunakan kalimat sehari-hari selama sejumlah kata kunci tetap ditangkap oleh Persona.

## Identitas Pembuat
Dibuat oleh: [13519062 Feralezer L. G. Tampubolon](https://github.com/felagorn) dan [13519103 Bryan Rinaldo](https://github.com/bryanrinaldoo)

Kode sumber program dapat diunduh melalui [Google Drive](https://drive.google.com/drive/folders/1wSmW9_jVs0KMn1SMpmZR79qycx2jdSFH?usp=sharing). Kode program juga tersedia pada [repository Github](https://github.com/felagorn/Tubes3_13519062) (Repository bersifat private, tapi dapat dibuka jika perlu).