import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()


class WeatherApp:
    # Initialize the app window and settings
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Weather Dashboard")
        self.root.geometry("400x300")
        self.api_key = os.getenv("open_weather_api_key")
        self.base_url = os.getenv("open_weather_url")
        self.setup_gui()
    # Create GUI components

    def setup_gui(self):
        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=20)
        self.city_entry = tk.Entry(search_frame, width=20)
        self.city_entry.pack(side=tk.LEFT, padx=5)
        search_btn = tk.Button(
            search_frame, text="Get Weather", command=self.get_weather_click)
        search_btn.pack(side=tk.LEFT)
        self.city_label = tk.Label(self.root, text="", font=('Arial', 16))
        self.city_label.pack(pady=10)
        self.temp_label = tk.Label(self.root, text="", font=('Arial', 24))
        self.temp_label.pack()
        self.desc_label = tk.Label(self.root, text="", font=('Arial', 12))
        self.desc_label.pack(pady=5)
        self.update_label = tk.Label(self.root, text="", font=('Arial', 10))
        self.update_label.pack()
    # Handle search button click

    def get_weather_click(self):
        city = self.city_entry.get()
        if city:
            weather_data = self.fetch_weather(city)
            if weather_data:
                self.display_weather(weather_data)
                self.save_weather(weather_data)
    # Fetch weather data from API

    def fetch_weather(self, city):
        try:
            params = {'q': city, 'appid': self.api_key, 'units': 'imperial'}
            response = requests.get(self.base_url, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                self.handle_errors(f"City '{city}' not found.")
        except Exception as e:
            self.handle_errors(f"Error: {e}")
            return None
    # Display weather data in the GUI

    def display_weather(self, data):
        self.city_label.config(text=data['name'])
        self.temp_label.config(text=f"{round(data['main']['temp'])}°F")
        self.desc_label.config(text=data['weather'][0]['description'].title())
        self.update_label.config(
            text=f"Updated: {datetime.now().strftime('%I:%M %p')}")
    # Save weather data to a file

    def save_weather(self, data):
        with open("weather_history.txt", "a") as f:
            f.write(
                f"{datetime.now()},{data['name']},{data['main']['temp']},{data['weather'][0]['description']}\n")
    # Handle errors and show messages

    def handle_errors(self, error):
        messagebox.showerror("Error", error)
    # Run the application

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = WeatherApp()
    app.run()
