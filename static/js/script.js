/**
 * Sistem Rekomendasi IEM - Frontend JavaScript
 * UAS Machine Learning - Teknik Informatika
 */

// Event listener ketika DOM sudah loaded
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('recommendationForm');
    const loading = document.getElementById('loading');
    const errorMessage = document.getElementById('errorMessage');
    const resultsSection = document.getElementById('resultsSection');
    
    // Handle form submission
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Ambil nilai dari form
        const budget = document.getElementById('budget').value;
        const genre = document.getElementById('genre').value;
        const soundCharacter = document.getElementById('sound_character').value;
        
        // Validasi input
        if (!budget || !genre || !soundCharacter) {
            showError('Semua field harus diisi!');
            return;
        }
        
        // Tampilkan loading, sembunyikan error dan results
        loading.style.display = 'block';
        errorMessage.style.display = 'none';
        resultsSection.style.display = 'none';
        
        // Scroll ke loading indicator
        loading.scrollIntoView({ behavior: 'smooth', block: 'center' });
        
        try {
            // Kirim request ke backend
            const response = await fetch('/api/recommend', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    budget: budget,
                    genre: genre,
                    sound_character: soundCharacter
                })
            });
            
            const data = await response.json();
            
            // Sembunyikan loading
            loading.style.display = 'none';
            
            if (data.success) {
                // Tampilkan hasil rekomendasi
                displayResults(data.recommendations, data.user_input);
            } else {
                // Tampilkan error
                showError(data.error || 'Terjadi kesalahan saat mendapatkan rekomendasi');
            }
            
        } catch (error) {
            loading.style.display = 'none';
            showError('Terjadi kesalahan koneksi ke server: ' + error.message);
        }
    });
});

/**
 * Menampilkan error message
 */
function showError(message) {
    const errorMessage = document.getElementById('errorMessage');
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
    errorMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

/**
 * Menampilkan hasil rekomendasi
 */
function displayResults(recommendations, userInput) {
    const resultsSection = document.getElementById('resultsSection');
    const userInputSummary = document.getElementById('userInputSummary');
    const recommendationResults = document.getElementById('recommendationResults');
    
    // Tampilkan summary input user
    userInputSummary.innerHTML = `
        <h5><i class="bi bi-info-circle"></i> Preferensi Anda:</h5>
        <ul class="mb-0">
            <li><strong>Budget:</strong> ${userInput.budget}</li>
            <li><strong>Genre:</strong> ${userInput.genre}</li>
            <li><strong>Karakter Suara:</strong> ${userInput.sound_character}</li>
        </ul>
    `;
    
    // Tampilkan rekomendasi IEM
    recommendationResults.innerHTML = '';
    
    recommendations.forEach((iem, index) => {
        const iemCard = createIEMCard(iem, index + 1);
        recommendationResults.innerHTML += iemCard;
    });
    
    // Tampilkan results section
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Membuat card untuk setiap IEM
 */
function createIEMCard(iem, rank) {
    // Fix path untuk gambar - tambahkan /static/ prefix
    const iemImagePath = iem.iem_image ? `/static/${iem.iem_image}` : null;
    const tuningImagePath = iem.tuning_image ? `/static/${iem.tuning_image}` : null;

    // Placeholder jika gambar tidak ada
    const placeholderIEM = 'https://via.placeholder.com/300x200/667eea/ffffff?text=' + encodeURIComponent(iem.name);
    const placeholderTuning = 'https://via.placeholder.com/400x200/764ba2/ffffff?text=' + encodeURIComponent(iem.tuning);

    // Hitung match score
    const matchScore = (100 - iem.distance * 10).toFixed(1);

    return `
        <div class="col-md-4 mb-4">
            <div class="card iem-card h-100 shadow-sm">
                <div class="card-header bg-gradient text-white text-center py-2" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                    <h6 class="mb-0">Rekomendasi #${rank}</h6>
                </div>

                <!-- Gambar IEM -->
                <img src="${iemImagePath || placeholderIEM}" class="card-img-top" alt="${iem.name}"
                     style="height: 200px; object-fit: cover;"
                     onerror="this.src='${placeholderIEM}'">

                <div class="card-body">
                    <!-- Nama IEM -->
                    <h5 class="card-title text-primary mb-1">${iem.name}</h5>
                    <p class="text-muted mb-2"><small><i class="bi bi-building"></i> ${iem.brand}</small></p>

                    <!-- Harga -->
                    <h4 class="text-success mb-3"><i class="bi bi-tag-fill"></i> ${iem.price_formatted}</h4>

                    <!-- Tuning Badge -->
                    <div class="mb-3">
                        <span class="badge rounded-pill" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); font-size: 0.9rem; padding: 8px 15px;">
                            <i class="bi bi-music-note-beamed"></i> ${iem.tuning}
                        </span>
                    </div>

                    <!-- Gambar Tuning -->
                    <div class="mb-3 text-center">
                        <p class="mb-2"><small class="text-muted"><strong>Grafik Tuning:</strong></small></p>
                        <img src="${tuningImagePath || placeholderTuning}" class="img-fluid rounded border" alt="${iem.tuning}"
                             style="max-height: 180px; width: 100%; object-fit: contain; background: #f8f9fa;"
                             onerror="this.src='${placeholderTuning}'">
                    </div>

                    <!-- Genre -->
                    <div class="mb-3 p-2 bg-light rounded">
                        <small class="text-muted">
                            <i class="bi bi-disc"></i> <strong>Genre:</strong> ${iem.genre}
                        </small>
                    </div>

                    <!-- Karakteristik Suara dengan Border Box -->
                    <div class="mb-3">
                        <p class="mb-2"><small><strong>Karakteristik Suara:</strong></small></p>

                        <!-- Bass -->
                        <div class="mb-2 p-2 border rounded" style="border-color: #dc3545 !important; border-width: 2px !important;">
                            <div class="d-flex justify-content-between align-items-center">
                                <span class="text-danger"><i class="bi bi-volume-up-fill"></i> <strong>Bass</strong></span>
                                <span class="badge bg-danger">${iem.bass}/5</span>
                            </div>
                            <div class="mt-1">
                                ${'<i class="bi bi-star-fill text-danger"></i>'.repeat(iem.bass)}${'<i class="bi bi-star text-muted"></i>'.repeat(5-iem.bass)}
                            </div>
                        </div>

                        <!-- Mid -->
                        <div class="mb-2 p-2 border rounded" style="border-color: #ffc107 !important; border-width: 2px !important;">
                            <div class="d-flex justify-content-between align-items-center">
                                <span class="text-warning"><i class="bi bi-volume-up-fill"></i> <strong>Mid</strong></span>
                                <span class="badge bg-warning text-dark">${iem.mid}/5</span>
                            </div>
                            <div class="mt-1">
                                ${'<i class="bi bi-star-fill text-warning"></i>'.repeat(iem.mid)}${'<i class="bi bi-star text-muted"></i>'.repeat(5-iem.mid)}
                            </div>
                        </div>

                        <!-- Treble -->
                        <div class="mb-2 p-2 border rounded" style="border-color: #0dcaf0 !important; border-width: 2px !important;">
                            <div class="d-flex justify-content-between align-items-center">
                                <span class="text-info"><i class="bi bi-volume-up-fill"></i> <strong>Treble</strong></span>
                                <span class="badge bg-info text-dark">${iem.treble}/5</span>
                            </div>
                            <div class="mt-1">
                                ${'<i class="bi bi-star-fill text-info"></i>'.repeat(iem.treble)}${'<i class="bi bi-star text-muted"></i>'.repeat(5-iem.treble)}
                            </div>
                        </div>
                    </div>

                    <!-- Info Tambahan -->
                    <div class="border-top pt-3">
                        <small class="text-muted">
                            <i class="bi bi-speaker"></i> <strong>Driver:</strong> ${iem.driver_type}<br>
                            <i class="bi bi-soundwave"></i> <strong>Soundstage:</strong> ${iem.soundstage}/5<br>
                            <i class="bi bi-graph-up"></i> <strong>Match Score:</strong>
                            <span class="badge ${matchScore >= 85 ? 'bg-success' : matchScore >= 75 ? 'bg-warning text-dark' : 'bg-secondary'}">${matchScore}%</span>
                        </small>
                    </div>
                </div>
            </div>
        </div>
    `;
}

