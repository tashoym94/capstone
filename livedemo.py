import tkinter as tk
from tkinter import messagebox
import requests
import json
from datetime import datetime


class WeatherApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Weather Dashboard")
        self.root.geometry("400x300")

        # API configuration
        self.api_key = "14c4f7b3d3355c7c67893bbd0e6c4b02"
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

        self.setup_gui()

    def setup_gui(self):
        # Search frame
        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=20)

        self.city_entry = tk.Entry(search_frame, width=20)
        self.city_entry.pack(side=tk.LEFT, padx=5)

        search_btn = tk.Button(search_frame, text="Get Weather",
                               command=self.get_weather_click)
        search_btn.pack(side=tk.LEFT)

        # Display frame
        self.display_frame = tk.Frame(self.root, bg='lightgray')
        self.display_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        # Labels for weather info
        self.city_label = tk.Label(
            self.display_frame, text="", font=('Arial', 16))
        self.city_label.pack(pady=10)

        self.temp_label = tk.Label(
            self.display_frame, text="", font=('Arial', 24))
        self.temp_label.pack()

        self.desc_label = tk.Label(
            self.display_frame, text="", font=('Arial', 12))
        self.desc_label.pack(pady=5)

        self.update_label = tk.Label(
            self.display_frame, text="", font=('Arial', 10))
        self.update_label.pack()

    def get_weather_click(self):
        city = self.city_entry.get()
        if city:
            weather_data = self.fetch_weather(city)
            if weather_data:
                self.display_weather(weather_data)
                self.save_weather(weather_data)

    def fetch_weather(self, city):
        try:
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'imperial'
            }
            response = requests.get(self.base_url, params=params, timeout=10)

            if response.status_code == 200:
                return response.json()
            else:
                self.handle_errors(f"City '{city}' not found")
                return None

        except requests.exceptions.Timeout:
            self.handle_errors("Request timed out. Check your connection.")
            return None
        except Exception as e:
            self.handle_errors(f"An error occurred: {str(e)}")
            return None

    def display_weather(self, data):
        self.city_label.config(text=data['name'])
        self.temp_label.config(text=f"{round(data['main']['temp'])}°F")
        self.desc_label.config(text=data['weather'][0]['description'].title())
        self.update_label.config(
            text=f"Updated: {datetime.now().strftime('%I:%M %p')}")

    def save_weather(self, data):
        with open("weather_history.txt", "a") as f:
            f.write(
                f"{datetime.now()},{data['name']},{data['main']['temp']},{data['weather'][0]['description']}\n")

    def handle_errors(self, error_message):
        messagebox.showerror("Error", error_message)

    def run(self):
        self.root.mainloop()


# Run the app
if __name__ == "__main__":
    app = WeatherApp()
    app.run()
