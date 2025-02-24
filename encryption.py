"""
Enhanced Encryption & Decryption Tool with GUI & Clipboard Copy Feature
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext
from cryptography.fernet import Fernet, InvalidToken
import pyperclip  # Clipboard copy support

# Global Password for encryption/decryption
ENCRYPTION_PASSWORD = "mypassword123"  # Change this as needed

# Function to generate and store encryption key
def generate_key():
    """Generates and saves an encryption key."""
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    messagebox.showinfo("Success", "Key generated successfully!")

# Function to load encryption key
def load_key():
    """Loads the encryption key from file."""
    try:
        with open("secret.key", "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        messagebox.showerror("Error", "Key file not found! Generate a key first.")
        return None

# Function to verify password
def verify_password():
    """Checks if entered password matches the set password."""
    entered_password = password_entry.get()
    if entered_password == ENCRYPTION_PASSWORD:
        return True
    messagebox.showerror("Error", "Incorrect Password!")
    return False

# Function to encrypt the message
def encrypt_message():
    """Encrypts the message entered by the user."""
    if not verify_password():
        return  # Wrong password, exit function

    key = load_key()
    if key is None:
        return

    try:
        f = Fernet(key)
        message = entry_text.get("1.0", tk.END).strip()
        if not message:
            messagebox.showerror("Error", "Enter text to encrypt!")
            return

        encrypted_message = f.encrypt(message.encode())
        entry_text.delete("1.0", tk.END)
        entry_text.insert("1.0", encrypted_message.decode())

        # Save the encrypted message to a file
        with open("encrypted_message.txt", "w", encoding="utf-8") as file:
            file.write(encrypted_message.decode())

        messagebox.showinfo("Success", "Message encrypted and saved!")

    except ValueError:
        messagebox.showerror("Error", "Encryption failed: Invalid input.")
    except InvalidToken:
        messagebox.showerror("Error", "Encryption failed: Invalid key or corrupted data.")

# Function to decrypt the message
def decrypt_message():
    """Decrypts the encrypted message."""
    if not verify_password():
        return  # Wrong password, exit function

    key = load_key()
    if key is None:
        return

    try:
        f = Fernet(key)
        encrypted_message = entry_text.get("1.0", tk.END).strip()
        if not encrypted_message:
            messagebox.showerror("Error", "Enter text to decrypt!")
            return

        decrypted_message = f.decrypt(encrypted_message.encode())
        entry_text.delete("1.0", tk.END)
        entry_text.insert("1.0", decrypted_message.decode())

    except ValueError:
        messagebox.showerror("Error", "Decryption failed: Invalid encrypted text.")
    except InvalidToken:
        messagebox.showerror("Error", "Invalid key or corrupted data.")

# Function to load encrypted message from file
def load_encrypted_message():
    """Loads the encrypted message from a file."""
    try:
        with open("encrypted_message.txt", "r", encoding="utf-8") as file:
            encrypted_message = file.read()
            entry_text.delete("1.0", tk.END)
            entry_text.insert("1.0", encrypted_message)
            messagebox.showinfo("Success", "Encrypted message loaded!")
    except FileNotFoundError:
        messagebox.showerror("Error", "No saved encrypted message found!")

# Function to copy message to clipboard
def copy_to_clipboard():
    """Copies the message from the text box to clipboard."""
    text = entry_text.get("1.0", tk.END).strip()
    if text:
        pyperclip.copy(text)
        messagebox.showinfo("Success", "Message copied to clipboard!")
    else:
        messagebox.showerror("Error", "No text to copy!")

# GUI Setup
root = tk.Tk()
root.title("Secure Message Encryptor")
root.geometry("500x400")
root.configure(bg="#f0f0f0")  # Light background

# Styling
FONT = ("Arial", 12)

# Password Input
tk.Label(root, text="Enter Password:", font=FONT, bg="#f0f0f0").pack(pady=5)
password_entry = tk.Entry(
    root,
    show="*",
    width=30,
    font=FONT,
    justify="center"
)
# Center Align Password
password_entry.pack(pady=5)

# Message Input
tk.Label(root, text="Enter Message:", font=FONT, bg="#f0f0f0").pack(pady=5)
entry_text = scrolledtext.ScrolledText(root, height=5, width=60, font=("Arial", 10))
entry_text.pack(padx=10, pady=5)

# Button Frame
frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(pady=10)

# Buttons (Fixed Long Line Errors)
tk.Button(frame, text="Generate Key", command=generate_key, width=15, font=FONT,
          bg="#4CAF50", fg="white").grid(row=0, column=0, padx=5, pady=5)

tk.Button(frame, text="Encrypt", command=encrypt_message, width=15, font=FONT,
          bg="#008CBA", fg="white").grid(row=0, column=1, padx=5, pady=5)

tk.Button(frame, text="Decrypt", command=decrypt_message, width=15, font=FONT,
          bg="#f44336", fg="white").grid(row=0, column=2, padx=5, pady=5)

tk.Button(frame, text="Load Encrypted", command=load_encrypted_message, width=15, font=FONT,
          bg="#ff9800", fg="white").grid(row=1, column=1, padx=5, pady=5)

tk.Button(frame, text="Copy to Clipboard", command=copy_to_clipboard, width=15, font=FONT,
          bg="#673ab7", fg="white").grid(row=1, column=2, padx=5, pady=5)

(root.mainloop())
