from flask import Flask, render_template, request
import base64
import os
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Google Sheets API Setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Get the environment variable for credentials (Base64 encoded)
credentials_base64 = os.getenv("GOOGLE_CREDENTIALS")
credentials_json = base64.b64decode(credentials_base64).decode('utf-8')

# Save the decoded credentials to a temporary file
with open('credentials.json', 'w') as f:
    f.write(credentials_json)

# Authorize the client using the credentials file
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# Open the Google Sheet
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1iFpIAzz_tJ5s44Iuvy8Idcwwk6NfowdbNe4i66YzXdc/edit?usp=sharing").sheet1

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_order():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        address = request.form['address']
        size = request.form['size']
        order_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Save the order to Google Sheet
        sheet.append_row([name, phone, address, size, order_time])

        return f"Order received! Name: {name}, Size: {size}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
