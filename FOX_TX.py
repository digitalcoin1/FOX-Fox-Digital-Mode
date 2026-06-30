import numpy as np
import scipy.io.wavfile as wav

def string_to_bits(text):
    return [int(b) for char in text for b in f"{ord(char):08b}"]

def generate_fox_symbol(bit_pair, sample_rate, symbol_duration):
    t = np.linspace(0, symbol_duration, int(sample_rate * symbol_duration), endpoint=False)
    sync_duration = symbol_duration * 0.7
    t_sync = t[t < sync_duration]
    t_data = t[t >= sync_duration] - sync_duration
    
    # FOX Sync Signature
    sync_wave = np.sin(2 * np.pi * 1000 * t_sync) * (t_sync / sync_duration) 
    sync_wave += np.sin(2 * np.pi * 1500 * t_sync)
    
    # FOX 2-Bit Data Tones
    bit_string = f"{bit_pair[0]}{bit_pair[1]}"
    tone_mapping = {"00": 800, "01": 1200, "10": 1600, "11": 2000}
    
    data_wave = np.sin(2 * np.pi * tone_mapping[bit_string] * t_data)
    full_symbol = np.concatenate([sync_wave, data_wave])
    return full_symbol / np.max(np.abs(full_symbol)) if len(full_symbol) > 0 else full_symbol

def encode_fox(text, sample_rate, mode_duration):
    audio_signal = []
    bits = string_to_bits(text)
    for i in range(0, len(bits), 2):
        symbol_wave = generate_fox_symbol(bits[i:i+2], sample_rate, mode_duration)
        audio_signal.extend(symbol_wave)
    return np.array(audio_signal, dtype=np.float32)

# --- FOX PROFILE CONFIGURATION ---
SELECTED_PROFILE = "Balanced"  # Options: "Stability", "Balanced", "Speed"
profile_durations = {"Stability": 0.2, "Balanced": 0.1, "Speed": 0.04}
duration = profile_durations[SELECTED_PROFILE]
message = "CQ YD1KLX GRID OI33IR"
sample_rate = 44100

print(f"Encoding payload using FOX profile [{SELECTED_PROFILE}]...")
audio_data = encode_fox(message, sample_rate, duration)

output_filename = f"fox_{SELECTED_PROFILE.lower()}.wav"
wav.write(output_filename, sample_rate, audio_data)

total_time = len(message) * 4 * duration
print(f"[SUCCESS] Saved as '{output_filename}'! Duration: {total_time:.2f} seconds.")