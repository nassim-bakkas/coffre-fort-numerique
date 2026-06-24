# 🔐 Coffre-fort Numérique

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
</p>

> A web application for **hiding and encrypting secret messages inside images** using steganography and cryptography techniques.

---

## ✨ Features

- **Encode** — Hide a text message inside an image using LSB steganography
- **Decode** — Extract hidden messages from steganographic images
- **Encrypt/Decrypt** — Protect messages with cryptographic algorithms
- **Analyze** — Detect steganographic modifications in images and compute metrics (PSNR, MSE)

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| UI | Streamlit |
| Steganography | LSB (Least Significant Bit) |
| Cryptography | Python `cryptography` library |
| Image processing | Pillow, NumPy |
| Metrics | PSNR, MSE analysis |

---

## 🚀 Getting Started

```bash
# Clone the repo
git clone https://github.com/nassim-bakkas/coffre-fort-numerique.git
cd coffre-fort-numerique

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

---

## 📁 Project Structure

```
coffre-fort-numerique/
├── app.py                      # Main Streamlit entry point
├── requirements.txt
├── DOCUMENTATION_TECHNIQUE.md  # Full technical documentation
├── services/
│   ├── crypto_service.py       # Encryption/decryption logic
│   ├── stegano_service.py      # LSB steganography engine
│   ├── file_service.py         # File handling utilities
│   └── metrics_service.py      # Image quality metrics (PSNR, MSE)
└── views/
    ├── home.py                 # Home page
    ├── encode.py               # Encode view
    ├── decode.py               # Decode view
    └── analyze.py              # Analysis view
```

---

## 👤 Author

**Nassim BAKKAS** — Engineering student at ENSET Mohammedia (IICCN — Cybersécurité et Confiance Numérique)

- GitHub: [@nassim-bakkas](https://github.com/nassim-bakkas)
- LinkedIn: [nassim-bakkas](https://linkedin.com/in/nassim-bakkas)
