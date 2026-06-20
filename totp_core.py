"""
totp_core.py
Core logic for TOTP-based Two-Factor Authentication.
Handles secret key generation, QR code creation, and OTP verification.
"""

import pyotp
import qrcode
import json
import os

DB_FILE = "users_db.json"


def load_db():
    """Load user database from JSON file."""
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)


def save_db(db):
    """Save user database to JSON file."""
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=4)


def register_user(username, issuer_name="MySecureApp"):
    """
    Register a new user:
    - Generates a unique base32 secret key
    - Saves it to the database
    - Creates a QR code image for the user to scan in Google Authenticator / Authy
    """
    db = load_db()

    if username in db:
        return None, "User already exists."

    secret = pyotp.random_base32()
    db[username] = {"secret": secret}
    save_db(db)

    # Generate the provisioning URI (used by authenticator apps)
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(name=username, issuer_name=issuer_name)

    # Generate QR code image
    qr_filename = f"qrcodes/{username}_qrcode.png"
    os.makedirs("qrcodes", exist_ok=True)
    qrcode.make(uri).save(qr_filename)

    return secret, qr_filename


def verify_otp(username, otp_code):
    """
    Verify the OTP entered by the user against their stored secret.
    Returns True if valid, False otherwise.
    """
    db = load_db()

    if username not in db:
        return False, "User not found."

    secret = db[username]["secret"]
    totp = pyotp.TOTP(secret)

    is_valid = totp.verify(otp_code, valid_window=1)  # allows 30s clock drift
    return is_valid, "OTP verified successfully!" if is_valid else "Invalid OTP."


def get_current_otp(username):
    """Utility function: get the current valid OTP for a user (for testing/demo only)."""
    db = load_db()
    if username not in db:
        return None
    secret = db[username]["secret"]
    return pyotp.TOTP(secret).now()
