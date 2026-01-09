
import matplotlib.pyplot as plt
import numpy as np
import os

# Buat folder jika belum ada
os.makedirs('static/images/Tuning', exist_ok=True)

def create_tuning_graph(tuning_type, filename):
    """
    Generate grafik frequency response untuk berbagai jenis tuning
    """
    # Frequency range: 10Hz to 20kHz
    freq = np.logspace(1, 4.3, 200)
    
    # Define response berdasarkan tuning type
    if tuning_type == "V-Shaped":
        # Bass boost + treble boost, mid dip
        response = -8 * (np.log10(freq/100))**2 + 5
        response += 3 * np.sin(np.log10(freq/20) * 3)
        
    elif tuning_type == "Neutral":
        # Flat response
        response = np.zeros_like(freq) + np.random.normal(0, 0.3, len(freq))
        
    elif tuning_type == "Balanced":
        # Slight variations, mostly flat
        response = 2 * np.sin(np.log10(freq/50) * 2)
        
    elif tuning_type == "Bright":
        # Treble emphasis
        response = 5 * np.log10(freq/100)
        response = np.clip(response, -5, 8)
        
    elif tuning_type == "Neutral-Bright":
        # Slight treble boost
        response = 3 * np.log10(freq/100)
        response = np.clip(response, -3, 6)
    
    else:
        response = np.zeros_like(freq)
    
    # Create figure
    plt.figure(figsize=(8, 4), facecolor='white')
    
    # Plot
    plt.semilogx(freq, response, linewidth=2.5, color='#667eea', label=tuning_type)
    
    # Grid
    plt.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
    
    # Labels
    plt.xlabel('Frequency (Hz)', fontsize=11, fontweight='bold')
    plt.ylabel('Relative Amplitude (dB)', fontsize=11, fontweight='bold')
    plt.title(f'{tuning_type} Tuning', fontsize=13, fontweight='bold', pad=15)
    
    # Limits
    plt.xlim(10, 20000)
    plt.ylim(-10, 10)
    
    # X-axis ticks
    plt.xticks([20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000],
               ['20', '50', '100', '200', '500', '1K', '2K', '5K', '10K', '20K'])
    
    # Y-axis ticks
    plt.yticks(range(-10, 11, 2))
    
    plt.axhline(y=0, color='gray', linestyle='-', linewidth=1, alpha=0.5)
    
    # Legend
    plt.legend(loc='upper right', framealpha=0.9)
    
    # Tight layout
    plt.tight_layout()
    
    # Save
    filepath = f'static/images/Tuning/{filename}'
    plt.savefig(filepath, dpi=100, bbox_inches='tight', facecolor='white')
    print(f"✅ Generated: {filepath}")
    
    plt.close()

# Generate semua grafik tuning
print("="*60)
print("Generating Tuning Graphs...")
print("="*60)

tuning_configs = [
    ("V-Shaped", "V Shape.png"),
    ("Neutral", "Neutral.png"),
    ("Balanced", "Balanced.png"),
    ("Bright", "Bright.png"),
    ("Neutral-Bright", "Neutral bright.png")
]

for tuning_type, filename in tuning_configs:
    create_tuning_graph(tuning_type, filename)

print("="*60)
print(" All tuning graphs generated successfully!")
print("="*60)
print("\nGrafik tersimpan di: static/images/Tuning/")
print("\nFile yang dibuat:")
for _, filename in tuning_configs:
    print(f"  - {filename}")

