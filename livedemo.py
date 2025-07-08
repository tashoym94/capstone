import customtkinter as ctk
from tkinter import messagebox
import json
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set appearance and theme
ctk.set_appearance_mode("light")  # default to light
# predefined themes or JSON theme
ctk.set_default_color_theme("pinktheme.json")


class WeatherApp:
    def __init__(self):
        # Create main application window
        self.root = ctk.CTk()
        self.root.title("Weather Dashboard")
        self.root.geometry("400x400")

        # Get API credentials from .env file
        self.api_key = os.getenv("open_weather_api_key")
        self.base_url = os.getenv("open_weather_url")

        # Setup GUI components
        self.setup_gui()

    def run(self):
        self.root.mainloop()

    def setup_gui(self):
        # Create input section (entry + buttons)
        search_frame = ctk.CTkFrame(self.root)
        search_frame.pack(pady=20)

        # Input field with placeholder
        self.city_entry = ctk.CTkEntry(
            search_frame, width=200, placeholder_text="City Name here")
        self.city_entry.grid(row=0, column=0, padx=5)

        # Button to fetch weather
        self.weather_btn = ctk.CTkButton(
            search_frame, text="☁️", width=40, command=self.get_weather_click)
        self.weather_btn.grid(row=0, column=1, padx=5)

        # Button to show weather history
        self.history_btn = ctk.CTkButton(
            search_frame, text="🕰️", width=40, command=self.show_history)
        self.history_btn.grid(row=0, column=2, padx=5)

        # Labels to show weather data
        self.city_label = ctk.CTkLabel(self.root, text="", font=('Arial', 18))
        self.city_label.pack(pady=10)

        self.temp_label = ctk.CTkLabel(self.root, text="", font=('Arial', 26))
        self.temp_label.pack()

        self.desc_label = ctk.CTkLabel(self.root, text="", font=('Arial', 14))
        self.desc_label.pack(pady=5)

        self.update_label = ctk.CTkLabel(
            self.root, text="", font=('Arial', 12))
        self.update_label.pack()

        # Toggle button for dark/light mode
        mode_toggle = ctk.CTkSwitch(
            self.root, text="Dark Mode", command=self.toggle_mode)
        mode_toggle.pack(pady=10)

    def toggle_mode(self):
        current = ctk.get_appearance_mode()
        if current == "Light":
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

    def get_weather_click(self):
        # Get user input from entry field
        city = self.city_entry.get().strip()

        if not city:
            self.handle_errors("Please enter a city name.")
            return
        if len(city) < 2:
            self.handle_errors("City name is too short.")
            return

        # Fetch weather data and update UI
        weather_data = self.fetch_weather(city)
        if weather_data:
            self.display_weather(weather_data)
            self.save_weather(weather_data)

    def fetch_weather(self, city):
        # Call OpenWeather API with city name
        try:
            if not self.api_key or not self.base_url:
                raise ValueError("Missing API key or base URL")

            params = {'q': city, 'appid': self.api_key, 'units': 'imperial'}
            response = requests.get(self.base_url, params=params, timeout=10)

            # Handle different API response statuses
            if response.status_code == 401:
                self.handle_errors("Invalid API key.")
                return None
            elif response.status_code == 404:
                self.handle_errors(f"City '{city}' not found.")
                return None
            elif response.status_code != 200:
                self.handle_errors(f"Unexpected error: {response.status_code}")
                return None

            return response.json()

        except requests.exceptions.Timeout:
            self.handle_errors(
                "Request timed out. Please check your internet connection.")
        except requests.exceptions.ConnectionError:
            self.handle_errors("Network error. Please check your connection.")
        except Exception as e:
            self.handle_errors(f"An unexpected error occurred: {e}")
            return None

    def display_weather(self, data):
        # Update UI with weather information
        self.city_label.configure(text=data['name'])
        self.temp_label.configure(text=f"{round(data['main']['temp'])}°F")
        self.desc_label.configure(
            text=data['weather'][0]['description'].title())
        self.update_label.configure(
            text=f"Updated: {datetime.now().strftime('%I:%M %p')}")

    def save_weather(self, data):
        # Save weather history to a JSON file
        history_file = "weather_history.json"

        record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "city": data['name'],
            "temperature": data['main']['temp'],
            "description": data['weather'][0]['description']
        }

        try:
            if os.path.exists(history_file):
                with open(history_file, "r") as f:
                    history = json.load(f)
            else:
                history = []

            history.append(record)

            with open(history_file, "w") as f:
                json.dump(history, f, indent=4)

        except Exception as e:
            self.handle_errors(f"Failed to save weather history: {e}")

    def load_weather_history(self):
        # Load saved weather history
        history_file = "weather_history.json"
        try:
            if os.path.exists(history_file):
                with open(history_file, "r") as f:
                    history = json.load(f)
                return history
            else:
                return []
        except Exception as e:
            self.handle_errors(f"Error loading weather history: {e}")
            return []

    def show_history(self):
        # Show last 5 weather records in a pop-up
        history = self.load_weather_history()
        if not history:
            messagebox.showinfo("Weather History", "No history available.")
            return

        history_str = "\n".join(
            [f"{h['timestamp']} - {h['city']}: {round(h['temperature'])}°F, {h['description'].title()}"
             for h in history[-5:]]
        )
        messagebox.showinfo("Last 5 Weather Records", history_str)

    def handle_errors(self, error):
        # Show error in pop-up dialog
        messagebox.showerror("Error", error)


if __name__ == "__main__":
    app = WeatherApp()
    app.run()
