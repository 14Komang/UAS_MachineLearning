# Membuat folder untuk gambar IEM dan Tuning

import os

print('=' * 80)
print('SETUP FOLDER GAMBAR')
print('=' * 80)

# Buat folder static/images jika belum ada
folders = [
    'static/images',
    'static/images/IEM',
    'static/images/Tuning',
    'static/css',
    'static/js'
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print(f'✅ Folder created: {folder}')

print('\n' + '=' * 80)
print('INFORMASI GAMBAR')
print('=' * 80)

print('\n Folder Gambar IEM: static/images/IEM/')
print('   Letakkan gambar IEM dengan format: [Nama_IEM].jpg')
print('   Contoh: TRN_MT3.jpg, CCA_CRA+.jpg')
print('   Jika gambar tidak ada, akan menggunakan placeholder otomatis.')

print('\n Folder Gambar Tuning: static/images/Tuning/')
print('   Gambar yang diperlukan:')
print('   - v-shaped.png       (untuk tuning V-Shaped)')
print('   - neutral.png        (untuk tuning Neutral)')
print('   - balanced.png       (untuk tuning Balanced)')
print('   - bright.png         (untuk tuning Bright)')
print('   - neutral-bright.png (untuk tuning Neutral-Bright)')

print('\n Tips:')
print('   - Ukuran gambar IEM: 300x200 px (landscape)')
print('   - Ukuran gambar tuning: 200x150 px (landscape)')
print('   - Format: JPG untuk IEM, PNG untuk tuning')
print('   - Jika tidak ada gambar, sistem akan menggunakan placeholder dari via.placeholder.com')

print('\n' + '=' * 80)
print(' SETUP SELESAI!')
print('=' * 80)

# Buat file README di folder images
readme_content = """# Folder Gambar

## IEM/
Letakkan gambar IEM dengan format: [Nama_IEM].jpg
Contoh: TRN_MT3.jpg, CCA_CRA+.jpg

Ukuran rekomendasi: 300x200 px (landscape)

## Tuning/
Gambar grafik tuning:
- v-shaped.png
- neutral.png
- balanced.png
- bright.png
- neutral-bright.png

Ukuran rekomendasi: 200x150 px (landscape)

## Placeholder
Jika gambar tidak tersedia, sistem akan otomatis menggunakan placeholder dari via.placeholder.com
"""

with open('static/images/README.md', 'w', encoding='utf-8') as f:
    f.write(readme_content)

print('\n📄 README.md created in static/images/')
print('\nAnda bisa menambahkan gambar IEM dan tuning ke folder tersebut.')
print('Jika tidak ada gambar, sistem akan menggunakan placeholder otomatis.')

