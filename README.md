# FOX - Fox Digital Mode Protocol for Amateur Radio

Developed by **SkywaveDX**

FOX (Fox Digital Mode) is an open-source, software-defined digital radio modulation protocol designed for experimental amateur radio communications. It features a unique multi-tone synchronization framing ramp paired with an efficient 4-state frequency-shift data payload window, allowing operators to transition smoothly between high-speed keyboard chatting and high-stability weak-signal operations.

## Protocol Architecture

FOX operates on a sequential frame structure. Each data symbol is split into two distinct time-domain periods:

1. **Sync/Pilot Phase (70% of symbol duration):** A signature multi-tone ramp combining overlapping 1000 Hz and 1500 Hz signals to provide robust timing alignment for the receiver, even under fading (QSB) conditions.
2. **Data Payload Phase (30% of symbol duration):** A single stable tone mapping a 2-bit binary pair to one of four distinct frequency states:
   * `00` -> 800 Hz
   * `01` -> 1200 Hz
   * `10` -> 1600 Hz
   * `11` -> 2000 Hz

By encoding **2 bits per symbol**, FOX achieves high throughput relative to its signaling speed.

---

## Operating Profiles

FOX supports three official operating profiles to adapt to varying atmospheric and band conditions. **CRITICAL:** The transmitter and receiver must be set to the exact same profile mode to avoid data corruption!

| Profile Mode | Symbol Duration | Baud Rate | Efficiency / Best For |
| :--- | :--- | :--- | :--- |
| **FOX-S** (Stability) | 200 ms | 5 Baud | Extreme weak-signal, high noise-floor, and long-distance HF propagation. |
| **FOX-B** (Balanced) | 100 ms | 10 Baud | General calling, stable VHF/UHF paths, and mild fading. |
| **FOX-F** (Speed) | 40 ms | 25 Baud | High-speed live keyboard ragchewing, rapid contesting (~70 WPM). |

---

## Project Structure

* `FOX_TX.py` - The transmitter engine. Synthesizes text data into legal, un-encrypted acoustic/RF wave streams (`.wav`).
* `FOX_RX.py` - The software-defined receiver. Uses Fast Fourier Transforms (FFT) to process audio streams and demodulate symbols cleanly.

---

## Quick Start Guide

### 1. Requirements & Setup
Ensure you have Python 3 installed, then create and activate your environment:

```bash
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install numpy scipy
```
An error occured while executing .venv\Scripts\Activate.ps1? Execute
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

### 2. Transmitting (TX)
Open FOX_TX.py, configure your SELECTED_PROFILE ("Stability", "Balanced", or "Speed") and customize your message payload (e.g., "CQ YD1KLX GRID OI33IR"). Run the script to generate your transmission wave file:

```bash
python FOX_TX.py
```

### 3. Receiving (RX)
Open FOX_RX.py and ensure the SELECTED_PROFILE variable matches exactly what was used to generate the file. Then execute the demodulator:

```bash
python FOX_RX.py
```

## Legal Compliance

FOX is fully open-source and publicly documented here. It complies with international amateur radio regulations prohibiting secret ciphers, making it legal for use on designated experimental amateur frequencies by licensed operators. Always include your callsign within the payload stream!
