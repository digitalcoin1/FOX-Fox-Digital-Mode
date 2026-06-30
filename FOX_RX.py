import numpy as np
import scipy.io.wavfile as wav

def decode_fox(filename, mode_duration):
    sample_rate, audio_data = wav.read(filename)
    
    if len(audio_data.shape) > 1:
        audio_data = audio_data[:, 0]
    audio_data = audio_data.astype(np.float32)
    if np.max(np.abs(audio_data)) > 1.0:
        audio_data = audio_data / np.max(np.abs(audio_data))

    samples_per_symbol = int(sample_rate * mode_duration)
    total_symbols = len(audio_data) // samples_per_symbol
    
    tone_mapping = {800: "00", 1200: "01", 1600: "10", 2000: "11"}
    target_freqs = [800, 1200, 1600, 2000]
    
    bit_stream = ""
    
    for s in range(total_symbols):
        start_idx = s * samples_per_symbol
        end_idx = start_idx + samples_per_symbol
        symbol_chunk = audio_data[start_idx:end_idx]
        
        data_start = int(samples_per_symbol * 0.7)
        data_chunk = symbol_chunk[data_start:]
        
        fft_data = np.abs(np.fft.rfft(data_chunk))
        fft_freqs = np.fft.rfftfreq(len(data_chunk), d=1/sample_rate)
        
        peak_freq = fft_freqs[np.argmax(fft_data)]
        closest_freq = min(target_freqs, key=lambda x: abs(x - peak_freq))
        bit_stream += tone_mapping[closest_freq]
        
    decoded_text = ""
    for i in range(0, len(bit_stream), 8):
        byte_chunk = bit_stream[i:i+8]
        if len(byte_chunk) == 8:
            decoded_text += chr(int(byte_chunk, 2))
            
    return decoded_text

# --- RUN FOX DECODER ---
# Change this to match what you used in FOX_TX.py!
SELECTED_PROFILE = "Balanced"  # Options: "Stability", "Balanced", "Speed"

profile_durations = {"Stability": 0.2, "Balanced": 0.1, "Speed": 0.04}
duration = profile_durations[SELECTED_PROFILE]
target_file = f"fox_{SELECTED_PROFILE.lower()}.wav"

print(f"Opening '{target_file}' and listening for FOX digital mode signals...")
try:
    decoded_output = decode_fox(target_file, duration)
    print("\n--- FOX DECODED MESSAGE RECEIVED ---")
    print(f"\"{decoded_output}\"")
    print("------------------------------------")
except FileNotFoundError:
    print(f"Error: Run 'FOX_TX.py' first to generate '{target_file}'!")