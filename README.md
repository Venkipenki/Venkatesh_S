# Project Documentation

## Overview

This repository contains two web application projects:

1. **Rule Engine**: A system for creating and evaluating logical rules based on user data.
2. **Weather Monitoring Dashboard**: A dashboard that tracks real-time weather conditions for multiple cities.

---

## Project 1: Rule Engine

### Description
The Rule Engine allows users to create custom rules using logical conditions and evaluate them against user data provided in JSON format. The application is built with Flask, SQLAlchemy, and JavaScript.

### Key Features
- Create custom rules.
- Evaluate rules against user data.
- Store rules in a SQLite database.

### Technologies Used
- **Flask**: Web framework for building the application.
- **SQLAlchemy**: ORM for managing the SQLite database.
- **JavaScript**: For handling user interactions and AJAX requests.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Venkipenki/Venkatesh_S/tree/532a04e40f5ec08329150da5160d103ede8eae8d
   ```
2. Navigate to the project directory:
   ```bash
   cd rule-engine
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python app.py
   ```

### Usage
- Open your web browser and go to `http://127.0.0.1:5000` to access the Rule Engine interface.

---

## Project 2: Weather Monitoring Dashboard

### Description
The Weather Monitoring Dashboard provides real-time weather data for various cities using the OpenWeatherMap API. It displays current weather conditions and daily summaries, including temperature visualizations.

### Key Features
- Displays current weather conditions for selected cities.
- Provides daily weather summaries (average, maximum, and minimum temperatures).
- Visual representation of temperature data using charts.

### Technologies Used
- **Flask**: Web framework for the application.
- **SQLite**: For storing weather data.
- **Chart.js**: For displaying temperature data graphically.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Venkipenki/Venkatesh_S/tree/532a04e40f5ec08329150da5160d103ede8eae8d
   ```
2. Navigate to the project directory:
   ```bash
   cd weather-dashboard
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Add your OpenWeatherMap API key in the code:
   ```python
   API_KEY = 'your_api_key_here'
   ```
5. Run the application:
   ```bash
   python app.py
   ```

### Usage
- Open your web browser and go to `http://127.0.0.1:5000` to access the Weather Monitoring Dashboard.

---
![image](https://github.com/user-attachments/assets/9a0e014f-f105-459f-beef-15560071021a)

![image](https://github.com/user-attachments/assets/afed6348-e4bf-445a-870d-3c38ee28bd69)


