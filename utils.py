# Externe Datei für nützliche Funktionen
import torch

# Begrüßung und bissel Werbung
def print_welcome():
    print("\033[91mWelcome to the Python Image-Captioning Program for Mac / Windows / Linux  with MPS, CUDA OR CPU\033[0m")

def print_stats():
    print("\033[94mSalesforce/blip2-opt-67b ≈ 7.753.329.664 billion parameters\033[0m")

def print_credits():
    print("\033[91mProgramming: Markus Rößler\n\033[0m")
    print("\033[93mMR-XOTOX-NASSE-WÄNDE-SDXL\033[0m")
    print("\033[93mnow in version 2.0 at CivitAI\033[0m")
    print("\033[93mhttps://civitai.com/models/448483/mr-xotox-nasse-waende-sdxl\n\033[0m")

def print_footer():
    print("June / 2024 Version 1.1 MPS")
    print("\033[91mwww.der-zerfleischer.de\033[0m")

def get_device():
    device = torch.device("mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu")
    return device
