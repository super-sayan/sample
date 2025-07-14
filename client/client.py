import requests
import os
from dotenv import load_dotenv

BASE_URL = "http://127.0.0.1:5000"
ENV_FILE = ".env"

def save_token(token):
    with open(ENV_FILE, 'w') as f:
        f.write(f"TOKEN={token}")

def load_token():
    load_dotenv()
    return os.getenv("TOKEN")

def login():
    username = input("Username: ")
    password = input("Password: ")
    response = requests.post(
        f"{BASE_URL}/login",
        json={"username": username, "password": password}
    )
    if response.status_code == 200:
        token = response.json().get("token")
        print("✅ Login successful!")
        save_token(token)
    else:
        print("Login failed:", response.json().get("error"))

def download():
    token = load_token()
    if not token:
        print("No token found. Please login first.")
        return
    headers = {"Authorization": token}
    response = requests.get(f"{BASE_URL}/download", headers=headers)
    if response.status_code == 200:
        with open("downloaded_song.txt", 'w') as f:
            f.write(response.text)
        print("Song downloaded successfully!")
    else:
        print("Download failed:", response.json().get("error"))

def main():
    print("1. Login\n2. Download Song")
    choice = input("Choose an option: ")
    if choice == "1":
        login()
    elif choice == "2":
        download()
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
