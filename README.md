# 🧩 Helwan ISO Signer

**Helwan ISO Signer** is a professional GUI tool developed as part of the **Helwan Linux Toolset**, designed to simplify the process of signing ISO files and generating release data using **GPG** and **SHA256** verification.

It’s built for developers, maintainers, and security-conscious users who want to handle release signing without diving into command-line tools.

---

## 🚀 Features

* ✅ Generate **SHA256 checksums** for ISO images
* ✅ Create **GPG signatures** automatically
* ✅ Verify existing signatures for authenticity
* ✅ Export readable **verification reports**
* ✅ Automatic or manual key handling
* ✅ Simple, modern **PyQt5 GUI**
* ✅ Fully themed with **Helwan Linux identity**
* ✅ Integrated **desktop entry** and icon for system menus
* ✅ **Splash screen** and polished user experience

---

## 🎨 Visual Identity

Helwan ISO Signer follows the **Helwan Linux Design Language**,
featuring a distinctive sea-green palette (`#0e2626` / `#2ec4b6`)
and a smooth startup splash screen inspired by the Helwan branding.

This design represents **clarity, simplicity, and technical confidence** —
the same values behind Helwan Linux itself.

---

## 🔐 Security

* Uses **GnuPG (gpg)** for signature generation and verification.
* Automatically generates keys for CI/CD workflows (optional).
* Provides **real-time logs** of each operation for full transparency.
* Never hides cryptographic steps — everything is visible and traceable.

---

## ⚙️ Installation

### 1️⃣ Requirements

* Python 3.10+
* PyQt5
* GnuPG (`gpg`)

### 2️⃣ Clone and Run

```bash
git clone https://github.com/helwan-linux/helwan-iso-signer.git
cd helwan-iso-signer
python3 signer_gui.py
```

### 3️⃣ (Optional) Desktop Integration

Install the `.desktop` file and icon:

```bash
sudo cp helwan-iso-signer.desktop /usr/share/applications/
sudo cp helwan-iso-signer.png /usr/share/icons/hicolor/256x256/apps/
```

Then launch **Helwan ISO Signer** from your applications menu.

---

## 🧠 Tech Stack

| Component         | Description                          |
| ----------------- | ------------------------------------ |
| **Language**      | Python 3                             |
| **GUI Framework** | PyQt5                                |
| **Theme**         | Custom Helwan QSS                    |
| **Modules**       | signer_gui.py / signer_logic.py      |
| **Platform**      | Arch-based / Helwan Linux compatible |

---

## 🧩 File Structure

```
helwan-iso-signer/
├── signer_gui.py          # Main GUI application
├── signer_logic.py        # Core logic and cryptographic functions
├── helwan_style.qss       # Helwan Linux theme
├── splash_screen.py       # Splash screen design
├── signer_icon.png        # Application icon
├── helwan-iso-signer.desktop
└── README.md
```

---

## 💚 About Helwan Linux

Helwan Linux is an **Arch-based distribution** focused on simplicity, intelligence,
and accessibility for both developers and everyday users.
Helwan ISO Signer is part of its growing **Helwan Tools Suite**,
aimed at providing elegant, smart, and native utilities for the Helwan ecosystem.

> “Security and usability — the Helwan way.”

---

## 📾 License

This project is licensed under the **MIT License**.
Feel free to fork, improve, and contribute back to the Helwan Linux ecosystem.

---

## 🌐 Author

**Helwan Linux Project**
Maintainer: [helwan-linux](https://github.com/helwan-linux)
Contributor: [@Saeed-Badrelden](https://github.com/Saeed-Badrelden)
