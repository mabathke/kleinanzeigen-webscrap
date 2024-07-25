from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('app/listings.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS listings
                 (ID TEXT PRIMARY KEY, Title TEXT, Price TEXT, Location TEXT, Date TEXT, Description TEXT)''')
    conn.commit()
    conn.close()

@app.route('/store', methods=['POST'])
def store():
    data = request.json.get('data')
    conn = sqlite3.connect('app/listings.db')
    c = conn.cursor()
    for item in data:
        c.execute('''INSERT OR REPLACE INTO listings (ID, Title, Price, Location, Date, Description) 
                     VALUES (?, ?, ?, ?, ?, ?)''', 
                  (item['ID'], item['Title'], item['Price'], item['Location'], item['Date'], item['Description']))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'}), 200

@app.route('/listings', methods=['GET'])
def listings():
    conn = sqlite3.connect('app/listings.db')
    c = conn.cursor()
    c.execute('SELECT * FROM listings')
    rows = c.fetchall()
    conn.close()
    return jsonify(rows), 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5001)
