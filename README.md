# 🔐 Two-Factor Authentication System (TOTP-Based)

A complete **Two-Factor Authentication (2FA)** system built in Python using the **TOTP (Time-based One-Time Password)** algorithm — the same technology used by Google Authenticator, Microsoft Authenticator, and Authy.

This project demonstrates how real-world 2FA systems generate, distribute, and verify one-time passwords securely, without storing or transmitting them over the network.

---

## 📌 Features

- ✅ Generate a unique cryptographic secret key per user
- ✅ Create a scannable **QR code** for easy setup in any TOTP authenticator app
- ✅ Verify 6-digit OTP codes with clock-drift tolerance (±30s)
- ✅ Two interfaces:
  - **CLI version** — quick terminal-based demo
  - **Web app (Flask)** — full browser-based registration & verification flow
- ✅ JSON-based lightweight user store (easily swappable with a real database)

---

## 🛠️ Tech Stack

| Component        | Technology         |
|-------------------|--------------------|
| Core 2FA logic    | Python, `pyotp`    |
| QR Code generation| `qrcode`           |
| Web framework     | Flask              |
| Storage           | JSON (demo) |

---

## 📂 Project Structure

```
two-factor-auth-system/
│
├── totp_core.py          # Core TOTP logic (register, verify, QR generation)
├── cli_demo.py            # Command-line interface demo
├── app.py                 # Flask web application
├── templates/             # HTML templates for the web UI
│   ├── base.html
│   ├── home.html
│   ├── register.html
│   ├── register_success.html
│   └── verify.html
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 How It Works

1. **Registration**
   - A random Base32 secret key is generated for the user (`pyotp.random_base32()`)
   - A provisioning URI is created and encoded into a **QR code**
   - User scans the QR code with Google Authenticator / Authy

2. **OTP Generation**
   - The authenticator app independently generates a new 6-digit OTP every 30 seconds using the shared secret + current time

3. **Verification**
   - When the user enters the OTP, the server recomputes the expected OTP using the same secret + current time window
   - If they match (within an allowed drift window), access is granted

This is exactly how production-grade 2FA systems work — **no OTP is ever sent over SMS/network**, making it resistant to interception attacks (unlike SMS-based OTP).

---

## ▶️ Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/two-factor-auth-system.git
cd two-factor-auth-system
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the CLI demo
```bash
python cli_demo.py
```

### 4. OR run the Web app
```bash
python app.py
```
Then open your browser at: **http://127.0.0.1:5000**

---

## 📱 Testing with a Real Authenticator App

1. Register a new user (CLI or web)
2. Open **Google Authenticator** / **Authy** on your phone
3. Scan the generated QR code (or manually enter the secret key)
4. Use the 6-digit code shown in the app to verify on the website/CLI

---

## 🔒 Security Notes

- This project is for **educational/demo purposes**. The JSON-based storage is **not** suitable for production.
- In a real-world system:
  - Store secrets encrypted in a proper database
  - Use HTTPS for all communication
  - Rate-limit OTP verification attempts to prevent brute-forcing
  - Combine with password-based primary authentication (this project assumes 2FA is the *second* factor)

---

## 📈 Possible Future Improvements

- [ ] Add password-based primary login (full 2-step auth flow)
- [ ] Database integration (SQLite/PostgreSQL) instead of JSON
- [ ] Backup codes for account recovery
- [ ] Rate limiting on OTP attempts
- [ ] Dockerize the application

---

## 📄 License

This project is open-source and available under the MIT License.

---

## 👤 Author
  Prajapati Amisha a.
  Built as part of a personal cybersecurity portfolio project.
