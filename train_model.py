
# 1. Load dataset IEM
# 2. Preprocessing data (encoding + normalisasi)
# 3. Training model KNN
# 4. Menyimpan model dan preprocessing objects


import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.neighbors import NearestNeighbors
import joblib
import os

print('=' * 80)
print('TRAINING MODEL KNN - SISTEM REKOMENDASI IEM')
print('=' * 80)

# 1. Load Dataset
print('\n[1/5] Loading dataset...')
df = pd.read_csv('IEM_dataset.csv')
print(f' Dataset loaded: {len(df)} IEM')
print(f'Kolom: {df.columns.tolist()}')

# 2. Preprocessing - Encoding Genre
print('\n[2/5] Encoding genre...')
label_encoder = LabelEncoder()
df['genre_encoded'] = label_encoder.fit_transform(df['genre'])

print('Genre Encoding:')
genre_mapping = dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)))
for genre, code in genre_mapping.items():
    print(f'  {genre} → {code}')

# 3. Seleksi Fitur
print('\n[3/5] Selecting features...')
feature_columns = ['price', 'bass', 'mid', 'treble', 'genre_encoded']
X = df[feature_columns].values
print(f' Features selected: {feature_columns}')
print(f'Shape: {X.shape}')

# 4. Normalisasi Fitur
print('\n[4/5] Normalizing features...')
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print(' Features normalized')
print(f'Mean: {X_scaled.mean(axis=0)}')
print(f'Std: {X_scaled.std(axis=0)}')

# 5. Training Model KNN
print('\n[5/5] Training KNN model...')
knn_model = NearestNeighbors(n_neighbors=5, metric='euclidean')
knn_model.fit(X_scaled)
print(' Model trained successfully!')
print(f'Algorithm: KNN')
print(f'Neighbors: {knn_model.n_neighbors}')
print(f'Metric: {knn_model.metric}')

# 6. Menyimpan Model dan Preprocessing Objects
print('\n[6/6] Saving models...')

# Buat folder models jika belum ada
os.makedirs('models', exist_ok=True)

# Simpan model
joblib.dump(knn_model, 'models/knn_model.pkl')
print(' KNN model saved: models/knn_model.pkl')

# Simpan scaler
joblib.dump(scaler, 'models/scaler.pkl')
print(' Scaler saved: models/scaler.pkl')

# Simpan label encoder
joblib.dump(label_encoder, 'models/label_encoder.pkl')
print(' Label encoder saved: models/label_encoder.pkl')

# Simpan dataset
df.to_csv('models/processed_dataset.csv', index=False)
print(' Dataset saved: models/processed_dataset.csv')

# 7. Testing Model
print('\n' + '=' * 80)
print('TESTING MODEL')
print('=' * 80)

# Fungsi untuk testing
def test_recommendation(budget_range, genre, sound_character):
    """Test model dengan input user"""
    
    # Mapping budget
    budget_map = {
        '< 500k': 300000,
        '500k-1jt': 750000,
        '1jt-2jt': 1500000,
        '> 2jt': 3000000
    }
    
    # Mapping karakter suara
    sound_map = {
        'Bass kuat': {'bass': 5, 'mid': 3, 'treble': 3},
        'Seimbang': {'bass': 3, 'mid': 4, 'treble': 3},
        'Detail / Jernih': {'bass': 2, 'mid': 3, 'treble': 5}
    }
    
    # Encode genre
    genre_encoded = label_encoder.transform([genre])[0]
    
    # Buat fitur input
    user_array = np.array([[
        budget_map[budget_range],
        sound_map[sound_character]['bass'],
        sound_map[sound_character]['mid'],
        sound_map[sound_character]['treble'],
        genre_encoded
    ]])
    
    # Normalisasi
    user_scaled = scaler.transform(user_array)
    
    # Prediksi
    distances, indices = knn_model.kneighbors(user_scaled, n_neighbors=3)
    
    # Tampilkan hasil
    print(f'\nInput: Budget={budget_range}, Genre={genre}, Karakter={sound_character}')
    print('\nTop 3 Rekomendasi:')
    for i, (idx, dist) in enumerate(zip(indices[0], distances[0]), 1):
        iem = df.iloc[idx]
        print(f'\n{i}. {iem["name"]}')
        print(f'   Brand: {iem["brand"]}')
        print(f'   Harga: Rp {int(iem["price"]):,}')
        print(f'   Tuning: {iem["tuning"]}')
        print(f'   Bass: {iem["bass"]}, Mid: {iem["mid"]}, Treble: {iem["treble"]}')
        print(f'   Distance: {dist:.4f}')

# Test 1
print('\n--- Test 1 ---')
test_recommendation('< 500k', 'Pop', 'Bass kuat')

# Test 2
print('\n--- Test 2 ---')
test_recommendation('1jt-2jt', 'Jazz', 'Detail / Jernih')

# Test 3
print('\n--- Test 3 ---')
test_recommendation('> 2jt', 'Campuran', 'Seimbang')

print('\n' + '=' * 80)
print(' TRAINING SELESAI!')
print('=' * 80)
print('\nModel siap digunakan untuk Flask backend.')
print('Jalankan: python app.py')
print('=' * 80)

