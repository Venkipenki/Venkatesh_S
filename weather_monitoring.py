import requests
import time
from datetime import datetime, timedelta
import sqlite3
from flask import Flask, render_template, jsonify

API_KEY = '44a371cac3cc68919ca29fb301d102c0'
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
UPDATE_INTERVAL = 300  # 5 minutes

app = Flask(__name__)

def kelvin_to_celsius(temp):
    return temp - 273.15

def get_weather_data(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
    response = requests.get(url)
    data = response.json()
    return {
        'city': city,
        'main': data['weather'][0]['main'],
        'temp': kelvin_to_celsius(data['main']['temp']),
        'feels_like': kelvin_to_celsius(data['main']['feels_like']),
        'dt': data['dt']
    }

def store_weather_data(data):
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS weather_data
                 (city TEXT, main TEXT, temp REAL, feels_like REAL, dt INTEGER)''')
    c.execute('INSERT INTO weather_data VALUES (?,?,?,?,?)',
              (data['city'], data['main'], data['temp'], data['feels_like'], data['dt']))
    conn.commit()
    conn.close()

def get_daily_summary(city):
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()
    yesterday = datetime.now() - timedelta(days=1)
    yesterday_unix = int(yesterday.timestamp())
    c.execute('''SELECT AVG(temp), MAX(temp), MIN(temp), main
                 FROM weather_data
                 WHERE city = ? AND dt > ?
                 GROUP BY main
                 ORDER BY COUNT(*) DESC
                 LIMIT 1''', (city, yesterday_unix))
    result = c.fetchone()
    conn.close()
    if result:
        return {
            'avg_temp': result[0],
            'max_temp': result[1],
            'min_temp': result[2],
            'dominant_condition': result[3]
        }
    return None

def check_alert_threshold(data, threshold):
    if data['temp'] > threshold:
        print(f"ALERT: Temperature in {data['city']} exceeded {threshold}°C!")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/current_weather')
def current_weather():
    weather_data = [get_weather_data(city) for city in CITIES]
    return jsonify(weather_data)

@app.route('/api/daily_summary')
def daily_summary():
    summaries = {city: get_daily_summary(city) for city in CITIES}
    return jsonify(summaries)

def main():
    while True:
        for city in CITIES:
            data = get_weather_data(city)
            store_weather_data(data)
            check_alert_threshold(data, 35)  # Alert threshold set to 35°C
        time.sleep(UPDATE_INTERVAL)

if __name__ == '__main__':
    app.run(debug=True)
