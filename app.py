"""
app.py
Flask web interface for the TOTP-based 2FA system.

Routes:
    /            -> Home page
    /register    -> Register a new user, shows QR code to scan
    /verify       -> Verify OTP entered by user
"""

from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from totp_core import register_user, verify_otp
import os

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-this-in-production"


@app.route("/qrcodes/<filename>")
def serve_qrcode(filename):
    """Serve generated QR code images so they can be displayed in the browser."""
    return send_from_directory("qrcodes", filename)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        if not username:
            flash("Please enter a username.")
            return redirect(url_for("register"))

        secret, qr_path = register_user(username)

        if secret is None:
            flash(qr_path)  # error message: "User already exists."
            return redirect(url_for("register"))

        return render_template(
            "register_success.html",
            username=username,
            secret=secret,
            qr_image=qr_path,
        )

    return render_template("register.html")


@app.route("/verify", methods=["GET", "POST"])
def verify():
    result = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        otp_code = request.form.get("otp", "").strip()

        is_valid, message = verify_otp(username, otp_code)
        result = {"valid": is_valid, "message": message}

    return render_template("verify.html", result=result)


if __name__ == "__main__":
    os.makedirs("qrcodes", exist_ok=True)
    app.run(debug=True, port=5000)
