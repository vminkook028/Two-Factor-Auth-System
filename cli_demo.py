"""
cli_demo.py
Command-line demo of the TOTP 2FA system.
Run this file to register a user and verify OTP directly in terminal.
"""

from totp_core import register_user, verify_otp, get_current_otp

def main():
    print("=== TOTP 2FA System (CLI Demo) ===\n")
    print("1. Register new user")
    print("2. Verify OTP")
    print("3. Show current OTP (for testing)")
    choice = input("\nEnter choice (1/2/3): ").strip()

    if choice == "1":
        username = input("Enter username: ").strip()
        secret, qr_path = register_user(username)
        if secret:
            print(f"\n[+] User '{username}' registered successfully!")
            print(f"[+] Secret key: {secret}")
            print(f"[+] QR code saved at: {qr_path}")
            print("[+] Scan this QR code with Google Authenticator / Authy app.")
        else:
            print(f"\n[-] {qr_path}")  # error message

    elif choice == "2":
        username = input("Enter username: ").strip()
        otp = input("Enter 6-digit OTP from your authenticator app: ").strip()
        valid, message = verify_otp(username, otp)
        print(f"\n[{'✓' if valid else '✗'}] {message}")

    elif choice == "3":
        username = input("Enter username: ").strip()
        otp = get_current_otp(username)
        if otp:
            print(f"\n[i] Current valid OTP for '{username}': {otp}")
            print("[i] (In real use, this comes from the authenticator app, not the server.)")
        else:
            print("\n[-] User not found.")

    else:
        print("\nInvalid choice.")


if __name__ == "__main__":
    main()
