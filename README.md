# 🌦️ Weather Dashboard App

A modern, multi-tab weather application built with **Python** using **CustomTkinter** for the interface and **Matplotlib** for visualizations. This app allows users to:

- 🔍 Check current weather for any city
- 🕘 View weather search history
- 🌇 Compare weather between two cities
- 🌗 Toggle between dark and light mode
- 💖 Enjoy a custom pink theme

---

## ✨ Features

- **Current Weather**: Fetch real-time weather data from the [OpenWeatherMap API](https://openweathermap.org/api)
- **Weather History**: Automatically saves up to 7 previous weather searches in a local JSON file
- **City Comparison**: Compare two cities’ temperatures using icons and a mini bar chart
- **Custom Theme**: Styled with a custom `pinktheme.json` for a unique look
- **Dark/Light Mode**: Easily toggle appearance with a switch

---

## 🔧 Technologies Used

- [Python 3.13+](https://www.python.org/)
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- [Matplotlib](https://matplotlib.org/)
- [Pillow (PIL)](https://python-pillow.org/)
- [Requests](https://docs.python-requests.org/)
- [dotenv](https://pypi.org/project/python-dotenv/)

---
## 2. Create a Virtual Environment (Optional but recommended)

python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate

## 3. Install Dependencies
pip install -r requirements.txt

## 4. Set Up API Key
open_weather_api_key=your_api_key_here
open_weather_url=https://api.openweathermap.org/data/2.5/weather

## 5. Run the App
python livedemo.py

## 📁 File Structure
.
├── livedemo.py               # Main app
├── pinktheme.json            # Custom color theme
├── weather_history.json      # Auto-created search history
├── .env                      # API credentials
├── requirements.txt
└── README.md

## 🛠 Common Issues
❌ Invalid API Key: Double-check .env file

🎨 Theme Errors: Ensure pinktheme.json is complete and formatted

🖼️ Icons Not Showing: Requires internet connection to fetch weather icons

🧱 Missing Widget Styles: CustomTkinter may error if your theme is incomplete

Tashoy Miller
Repo - 
