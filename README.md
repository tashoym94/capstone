# 🌤 Weather Dashboard
# A Python + CustomTkinter desktop application that delivers real-time weather updates, 5-day forecasts, historical tracking, and group CSV-based weather analysis — all wrapped in a custom pink-themed UI.

# 📌 Purpose
# The Weather Dashboard was created to give users an interactive and visually appealing way to:
# Monitor real-time weather conditions
# Plan outfits based on the forecast
# Track historical temperature trends
# Compare cities
# Collaborate with teams by combining weather CSV datasets into one chart

# 🚀 Core Features
# Weather Tab
# Current temperature, feels-like, humidity, and wind speed
# Weather condition description + icon
# Outfit recommendation based on weather
# 5-Day Forecast Tab
# Daily temperature & weather conditions for the next 5 days
# Icons and weather descriptions for each day
# History Tab
# Displays up to 10 recent weather records stored in JSON & CSV
# City Comparison Tab
# Compare two cities side-by-side with a mini temperature chart
# Group Feature Tab
# Load multiple CSV files containing Date, Time, City, Temperature_F
# Plot multiple distinct-colored lines on one graph
# Supports different date/time formats (e.g., 15:00 or 11:45pm)

# 🎨 Design & Enhancements
# Custom Pink JSON Theme for a soft, cohesive look
# Embedded Matplotlib charts for data visualization
# Error handling for invalid API keys, missing data, or bad CSVs
# Modular code structure for scalability and maintenance

# 🛠️ Installation
# 1. Clone the Repository
# bash
# Copy
# git clone https://github.com/your-username/weather-dashboard.git
# cd weather-dashboard
# 2. Create a Virtual Environment
# bash
# Copy
# python3 -m venv venv
# source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate     # Windows
# 3. Install Dependencies
# bash
# Copy
# pip install -r requirements.txt
# 4. Set Up .env File
# Create a .env file in the project root:
# env
# Copy
# open_weather_api_key=YOUR_OPENWEATHERMAP_API_KEY
# open_weather_url=https://api.openweathermap.org/data/2.5/weather
# open_weather_forecast_url=https://api.openweathermap.org/data/2.5/forecast
# 📂 Project Structure
# bash
# Copy
# weather-dashboard/
# │── data/
# │   ├── pinktheme.json           # Custom UI theme
# │── features/
# │   ├── icons.py                 # Weather icon handler
# │   ├── city_comparison.py       # City comparison logic
# │── Group_feature/Team_csv/      # CSV files for group feature
# │── livedemo.py                  # Main application file
# │── requirements.txt
# │── README.md
# │── .env
# ▶️ Usage
# bash
# Copy
# python livedemo.py
# Navigate tabs for Weather, 5-Day Forecast, History, City Comparison, and Group Feature.

# In Group Feature, select CSVs and click Add CSV to Graph to visualize multiple datasets together.

# 📊 Example CSV Format
# csv
# Copy
# Date,Time,City,Temperature_F
# 2025-08-06,15:00,Miami,85.0
# 2025-08-07,11:45pm,Los Angeles,71.92
# 💡 Future Enhancements
# Automatic location detection

# Weather alerts for severe conditions

E# xport group charts to PNG/PDF

# 👩‍💻 Author
# Tashoy — Creator, Developer, and Designer of the Weather Dashboard