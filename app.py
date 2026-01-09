
# Aplikasi web untuk merekomendasikan IEM berdasarkan:
# - Budget user
# - Genre musik favorit
# - Karakter suara yang diinginkan

from flask import Flask, render_template, request, jsonify, Response
from flask_cors import CORS
import pandas as pd
import numpy as np
import joblib
import os
import requests

# Inisialisasi Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS untuk API

# Path ke folder models
MODEL_DIR = 'models'

# Load model dan preprocessing objects
print('Loading models...')
knn_model = joblib.load(os.path.join(MODEL_DIR, 'knn_model.pkl'))
scaler = joblib.load(os.path.join(MODEL_DIR, 'scaler.pkl'))
label_encoder = joblib.load(os.path.join(MODEL_DIR, 'label_encoder.pkl'))
df = pd.read_csv(os.path.join(MODEL_DIR, 'processed_dataset.csv'))
print('✅ Models loaded successfully!')

# Mapping budget range ke nilai numerik
BUDGET_MAP = {
    '< 500k': 300000,
    '500k-1jt': 750000,
    '1jt-2jt': 1500000,
    '> 2jt': 3000000
}

# Mapping karakter suara ke nilai bass, mid, treble
SOUND_CHARACTER_MAP = {
    'Bass kuat': {'bass': 5, 'mid': 3, 'treble': 3},
    'Seimbang': {'bass': 3, 'mid': 4, 'treble': 3},
    'Detail / Jernih': {'bass': 2, 'mid': 3, 'treble': 5}
}

# Mapping tuning ke gambar
TUNING_IMAGE_MAP = {
    'V-Shaped': 'V Shape.png',
    'Neutral': 'Neutral.png',
    'Balanced': 'Balanced.png',
    'Bright': 'bright.png',
    'Neutral-Bright': 'Neutral bright.png'
}


def map_user_input(budget_range, genre, sound_character):
    """
    Mapping input user ke fitur yang digunakan model
    
    Args:
        budget_range: Range budget user
        genre: Genre musik favorit
        sound_character: Karakter suara yang diinginkan
    
    Returns:
        dict: Fitur yang siap digunakan untuk prediksi
    """
    # Mapping budget
    price = BUDGET_MAP.get(budget_range, 750000)
    
    # Mapping karakter suara
    sound_features = SOUND_CHARACTER_MAP.get(sound_character, {'bass': 3, 'mid': 4, 'treble': 3})
    
    # Encode genre
    try:
        genre_encoded = label_encoder.transform([genre])[0]
    except:
        genre_encoded = 0  # Default jika genre tidak ditemukan
    
    # Buat fitur input
    user_features = {
        'price': price,
        'bass': sound_features['bass'],
        'mid': sound_features['mid'],
        'treble': sound_features['treble'],
        'genre_encoded': genre_encoded
    }
    
    return user_features


def get_iem_image_url(iem_name, brand):
    """
    Generate URL gambar IEM dari berbagai sumber
    Prioritas:
    1. Lokal (jika ada)
    2. Placeholder dengan nama IEM
    """
    # Coba cek file lokal dulu
    iem_image_name = iem_name.replace(' ', '_').replace('+', 'Plus')
    local_path = f"static/images/IEM/{iem_image_name}.jpg"

    # Jika file lokal ada, return path lokal
    if os.path.exists(local_path):
        return f"images/IEM/{iem_image_name}.jpg"

    # Jika tidak ada, gunakan placeholder dengan branding
    # Format: Brand + Model Name
    placeholder_text = f"{brand} {iem_name}"
    return f"https://via.placeholder.com/300x200/667eea/ffffff?text={placeholder_text}"


def get_recommendations(budget_range, genre, sound_character, top_n=3):
    """
    Mendapatkan rekomendasi IEM berdasarkan input user
    DENGAN FILTER BUDGET - hanya tampilkan IEM yang sesuai budget!

    Args:
        budget_range: Range budget user
        genre: Genre musik favorit
        sound_character: Karakter suara yang diinginkan
        top_n: Jumlah rekomendasi (default: 3)

    Returns:
        list: Top N rekomendasi IEM yang sesuai budget
    """
    # Mapping input user ke fitur
    user_features = map_user_input(budget_range, genre, sound_character)

    # STEP 1: FILTER DATASET BERDASARKAN BUDGET
    # Tentukan range harga berdasarkan budget yang dipilih
    if budget_range == '< 500k':
        min_price = 0
        max_price = 500000
    elif budget_range == '500k-1jt':
        min_price = 500000
        max_price = 1000000
    elif budget_range == '1jt-2jt':
        min_price = 1000000
        max_price = 2000000
    elif budget_range == '> 2jt':
        min_price = 2000000
        max_price = float('inf')
    else:
        # Default: semua harga
        min_price = 0
        max_price = float('inf')

    # Filter dataset berdasarkan budget
    df_filtered = df[(df['price'] >= min_price) & (df['price'] <= max_price)].copy()

    # Jika tidak ada IEM dalam budget, return empty list
    if len(df_filtered) == 0:
        return []

    # STEP 2: PREPARE FEATURES UNTUK KNN
    feature_cols = ['price', 'bass', 'mid', 'treble', 'genre_encoded']
    X_filtered = df_filtered[feature_cols].values

    # Normalisasi features dari dataset yang sudah difilter
    X_filtered_scaled = scaler.transform(X_filtered)

    # STEP 3: PREPARE INPUT USER
    user_array = np.array([[
        user_features['price'],
        user_features['bass'],
        user_features['mid'],
        user_features['treble'],
        user_features['genre_encoded']
    ]])

    # Normalisasi input user
    user_scaled = scaler.transform(user_array)

    # STEP 4: FIT KNN PADA DATASET YANG SUDAH DIFILTER
    from sklearn.neighbors import NearestNeighbors
    k = min(top_n, len(df_filtered))  # Pastikan k tidak lebih besar dari jumlah data
    knn_local = NearestNeighbors(n_neighbors=k, metric='euclidean')
    knn_local.fit(X_filtered_scaled)

    # STEP 5: CARI NEAREST NEIGHBORS
    distances, indices = knn_local.kneighbors(user_scaled)

    # STEP 6: AMBIL REKOMENDASI
    recommendations = []
    for local_idx, distance in zip(indices[0], distances[0]):
        # Get IEM dari df_filtered
        iem = df_filtered.iloc[local_idx]

        # Format data untuk response
        # Gunakan nama langsung dari dataset untuk gambar (nama.png)
        iem_image_path = f"images/IEM/{iem['name']}.png"
        tuning_image_path = f"images/Tuning/{TUNING_IMAGE_MAP.get(iem['tuning'], 'Neutral.png')}"

        recommendation = {
            'name': iem['name'],
            'brand': iem['brand'],
            'price': int(iem['price']),
            'price_formatted': f"Rp {int(iem['price']):,}",
            'tuning': iem['tuning'],
            'bass': int(iem['bass']),
            'mid': int(iem['mid']),
            'treble': int(iem['treble']),
            'soundstage': int(iem['soundstage']),
            'genre': iem['genre'],
            'driver_type': iem['driver_type'],
            'distance': float(distance),
            'match_score': round((1 / (1 + distance)) * 100, 1),  # Similarity score
            'iem_image': iem_image_path,
            'tuning_image': tuning_image_path
        }
        recommendations.append(recommendation)

    return recommendations


@app.route('/')
def index():
    """Halaman utama"""
    return render_template('index.html')


@app.route('/api/recommend', methods=['POST'])
def recommend():
    """
    API endpoint untuk mendapatkan rekomendasi IEM
    
    Request JSON:
        {
            "budget": "< 500k" | "500k-1jt" | "1jt-2jt" | "> 2jt",
            "genre": "Pop" | "Rock" | "EDM" | "Jazz" | "Campuran",
            "sound_character": "Bass kuat" | "Seimbang" | "Detail / Jernih"
        }
    
    Response JSON:
        {
            "success": true,
            "recommendations": [...]
        }
    """
    try:
        # Ambil data dari request
        data = request.get_json()
        budget = data.get('budget')
        genre = data.get('genre')
        sound_character = data.get('sound_character')
        
        # Validasi input
        if not all([budget, genre, sound_character]):
            return jsonify({
                'success': False,
                'error': 'Semua field harus diisi!'
            }), 400
        
        # Dapatkan rekomendasi
        recommendations = get_recommendations(budget, genre, sound_character, top_n=3)

        # Cek jika tidak ada rekomendasi (budget tidak ada IEM yang cocok)
        if len(recommendations) == 0:
            return jsonify({
                'success': False,
                'error': f'Tidak ada IEM yang tersedia dalam budget {budget}. Silakan pilih budget lain.',
                'user_input': {
                    'budget': budget,
                    'genre': genre,
                    'sound_character': sound_character
                }
            }), 404

        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'user_input': {
                'budget': budget,
                'genre': genre,
                'sound_character': sound_character
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/img')
def proxy_image():
    """
    Image proxy untuk menampilkan gambar dari URL eksternal
    Usage: /img?u=<encoded_url>
    """
    url = request.args.get('u', '')

    # Validasi URL
    if not url or not (url.startswith('http://') or url.startswith('https://')):
        return jsonify({'error': 'invalid_url'}), 400

    # Headers untuk request gambar
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'image/*,*/*',
        'Referer': 'https://www.google.com'
    }

    try:
        # Request gambar dari URL
        r = requests.get(url, headers=headers, timeout=10)

        if r.status_code != 200:
            return jsonify({'error': f'http_{r.status_code}'}), 502

        # Get content type
        content_type = r.headers.get('Content-Type', 'image/jpeg')

        # Return gambar
        return Response(r.content, content_type=content_type)

    except Exception as e:
        return jsonify({'error': str(e)}), 502


if __name__ == '__main__':
    print('=' * 80)
    print(' Starting IEM Recommendation System')
    print('=' * 80)
    print('Server running at: http://localhost:5000')
    print('Press CTRL+C to quit')
    print('=' * 80)
    app.run(debug=True, host='0.0.0.0', port=5000)

