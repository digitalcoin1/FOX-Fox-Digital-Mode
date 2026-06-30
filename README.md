# DMFAR - Digital Mode For Amateur Radio

Developed by **SkywaveDX**

DMFAR is a homebrewed, software-defined digital radio modulation protocol designed for experimental amateur radio communications. It features a unique multi-tone synchronization framing ramp paired with an efficient 4-state frequency-shift data payload window, allowing operators to transition smoothly between high-speed keyboard chatting and high-stability weak-signal operations.



## Protocol Architecture

DMFAR operates on a sequential frame structure. Each data symbol is split into two distinct time-domain periods:
1. **Sync/Pilot Phase (70% of symbol duration):** A signature multi-tone ramp combining overlapping $1000\text{ Hz}$ and $1500\text{ Hz}$ signals to provide robust timing alignment for the receiver, even under fading (QSB) conditions.
2. **Data Payload Phase (30% of symbol duration):** A single stable tone mapping a 2-bit binary pair to one of four distinct frequency states:
   * `00` $\rightarrow 800\text{ Hz}$
   * `01` $\rightarrow 1200\text{ Hz}$
   * `10` $\rightarrow 1600\text{ Hz}$
   * `11` $\rightarrow 2000\text{ Hz}$

By encoding **2 bits per symbol**, DMFAR achieves high throughput relative to its signaling speed.

---

## Operating Profiles

DMFAR supports three official operating profiles to adapt to varying atmospheric and band conditions:

| Profile Mode | Symbol Duration | Baud Rate | Efficiency / Best For |
| :--- | :--- | :--- | :--- |
| **DMFAR-S** (Stability) | $200\text{ ms}$ | $5\text{ Baud}$ | Extreme weak-signal, high noise-floor, and long-distance HF propagation. |
| **DMFAR-B** (Balanced) | $100\text{ ms}$ | $10\text{ Baud}$ | General calling, stable VHF/UHF paths, and mild fading. |
| **DMFAR-F** (Speed) | $40\text{ ms}$ | $25\text{ Baud}$ | High-speed live keyboard ragchewing, rapid contesting (~70 WPM). |

---

## Project Structure

* `dmfar.py` - The transmitter engine. Synthesizes text data into legal, un-encrypted acoustic/RF wave streams.
* `dmfar_receiver.py` - The software-defined receiver. Uses Fast Fourier Transforms (FFT) to process audio streams and demodulate symbols cleanly.

---

## Quick Start Guide

### 1. Requirements & Setup
Ensure you have Python 3 installed, then create and activate your environment:
```bash
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install numpy scipy
