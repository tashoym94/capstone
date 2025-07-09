import customtkinter as ctk
import requests
import os
import json
import matplotlib.pyplot as plt
import tkinter.messagebox as messagebox
from datetime import datetime
from dotenv import load_dotenv
from PIL import Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from customtkinter import CTkImage

load_dotenv()


class WeatherApp:
    def __init__(self):
        # Initialize main window and default appearance
        ctk.set_appearance_mode("light")  # Options: "light", "dark"
        ctk.set_default_color_theme("pinktheme.json")

        self.root = ctk.CTk()
        self.root.title("Weather Dashboard")
        self.root.geometry("420x600")

        self.api_key = os.getenv("open_weather_api_key")
        self.base_url = os.getenv("open_weather_url")

        self.setup_gui()

    def setup_gui(self):
        # Theme toggle
        theme_frame = ctk.CTkFrame(self.root)
        theme_frame.pack(pady=5)
        self.theme_toggle = ctk.CTkSwitch(
            theme_frame, text="Dark Mode", command=self.toggle_theme)
        self.theme_toggle.pack()

        # Tab setup
        self.tabview = ctk.CTkTabview(self.root, width=400, height=520)
        self.tabview.pack(pady=10)

        self.weather_tab = self.tabview.add("Weather")
        self.history_tab = self.tabview.add("Weather History")
        self.compare_tab = self.tabview.add("City Comparison")

        # Weather tab widgets
        search_frame = ctk.CTkFrame(self.weather_tab)
        search_frame.pack(pady=10)

        self.city_entry = ctk.CTkEntry(
            search_frame, width=200, placeholder_text="City Name here")
        self.city_entry.pack(side="left", padx=5)

        get_btn = ctk.CTkButton(
            search_frame, text="Get Weather", command=self.get_weather_click)
        get_btn.pack(side="left", padx=5)

        self.city_label = ctk.CTkLabel(
            self.weather_tab, text="", font=ctk.CTkFont(size=16))
        self.city_label.pack()

        self.temp_label = ctk.CTkLabel(
            self.weather_tab, text="", font=ctk.CTkFont(size=24))
        self.temp_label.pack()

        self.desc_label = ctk.CTkLabel(
            self.weather_tab, text="", font=ctk.CTkFont(size=12))
        self.desc_label.pack()

        self.feels_like_label = ctk.CTkLabel(self.weather_tab, text="")
        self.feels_like_label.pack()

        self.humidity_label = ctk.CTkLabel(self.weather_tab, text="")
        self.humidity_label.pack()

        self.wind_label = ctk.CTkLabel(self.weather_tab, text="")
        self.wind_label.pack()

        self.update_label = ctk.CTkLabel(
            self.weather_tab, text="", font=ctk.CTkFont(size=10))
        self.update_label.pack()

        # History tab
        self.history_frame = ctk.CTkFrame(self.history_tab)
        self.history_frame.pack(fill="both", expand=True, pady=10)

        self.history_text = ctk.CTkTextbox(
            self.history_frame, wrap="none", width=380, height=400)
        self.history_text.pack(pady=10)

        # Comparison tab
        compare_frame = ctk.CTkFrame(self.compare_tab)
        compare_frame.pack(pady=10)

        self.city1_entry = ctk.CTkEntry(
            compare_frame, width=160, placeholder_text="First City")
        self.city1_entry.pack(side="left", padx=5)

        self.city2_entry = ctk.CTkEntry(
            compare_frame, width=160, placeholder_text="Second City")
        self.city2_entry.pack(side="left", padx=5)

        compare_btn = ctk.CTkButton(
            self.compare_tab, text="Compare", command=self.compare_cities)
        compare_btn.pack(pady=5)

        self.icon1_label = ctk.CTkLabel(self.compare_tab, text="")
        self.icon1_label.pack()

        self.icon2_label = ctk.CTkLabel(self.compare_tab, text="")
        self.icon2_label.pack()

        self.result_label = ctk.CTkLabel(
            self.compare_tab, text="", font=ctk.CTkFont(size=14))
        self.result_label.pack(pady=10)

    def toggle_theme(self):
        # Toggle dark/light mode
        mode = "dark" if self.theme_toggle.get() else "light"
        ctk.set_appearance_mode(mode)

    def run(self):
        self.root.mainloop()

    def get_weather_click(self):
        city = self.city_entry.get().strip()
        if not city:
            self.handle_errors("Please enter a city name.")
            return
        weather_data = self.fetch_weather(city)
        if weather_data:
            self.display_weather(weather_data)
            self.save_weather(weather_data)
            self.load_weather_history()

    def fetch_weather(self, city):
        try:
            if not self.api_key or not self.base_url:
                raise ValueError("Missing API key")
            params = {'q': city, 'appid': self.api_key, 'units': 'imperial'}
            response = requests.get(self.base_url, params=params, timeout=10)

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
            self.handle_errors("Request timed out.")
        except requests.exceptions.ConnectionError:
            self.handle_errors("Network error.")
        except Exception as e:
            self.handle_errors(f"Error: {e}")
            return None

    def display_weather(self, data):
        self.city_label.configure(text=data['name'])
        self.temp_label.configure(text=f"{round(data['main']['temp'])}°F")
        self.desc_label.configure(
            text=data['weather'][0]['description'].title())
        self.feels_like_label.configure(
            text=f"Feels Like: {round(data['main']['feels_like'])}°F")
        self.humidity_label.configure(
            text=f"Humidity: {data['main']['humidity']}%")
        self.wind_label.configure(text=f"Wind: {data['wind']['speed']} mph")
        self.update_label.configure(
            text=f"Updated: {datetime.now().strftime('%I:%M %p')}")

    def save_weather(self, data):
        record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "city": data['name'],
            "temperature": data['main']['temp'],
            "description": data['weather'][0]['description']
        }
        try:
            if os.path.exists("weather_history.json"):
                with open("weather_history.json", "r") as f:
                    history = json.load(f)
            else:
                history = []

            history.append(record)
            history = history[-7:]  # Keep last 7 entries only
            with open("weather_history.json", "w") as f:
                json.dump(history, f, indent=4)
        except Exception as e:
            self.handle_errors(f"Failed to save weather history: {e}")

    def load_weather_history(self):
        try:
            with open("weather_history.json", "r") as f:
                history = json.load(f)[-7:]
            self.history_text.delete("1.0", "end")
            for entry in reversed(history):
                self.history_text.insert(
                    "end", f"{entry['timestamp']} - {entry['city']} - {round(entry['temperature'])}°F - {entry['description'].title()}\n")
        except:
            self.history_text.insert("end", "No weather history available.\n")

    def compare_cities(self):
        city1 = self.city1_entry.get().strip()
        city2 = self.city2_entry.get().strip()

        if not city1 or not city2:
            self.handle_errors("Please enter both city names.")
            return

        data1 = self.fetch_weather(city1)
        data2 = self.fetch_weather(city2)

        if data1 and data2:
            temp1 = data1['main']['temp']
            temp2 = data2['main']['temp']
            diff = abs(round(temp1 - temp2, 1))

            self.result_label.configure(
                text=f"{data1['name']}: {round(temp1)}°F\n{data2['name']}: {round(temp2)}°F\nDifference: {diff}°F"
            )

            self.set_icon(self.icon1_label, data1['weather'][0]['icon'])
            self.set_icon(self.icon2_label, data2['weather'][0]['icon'])

            self.display_chart([data1['name'], data2['name']], [temp1, temp2])

    def set_icon(self, label, icon_code):
        try:
            url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            img_data = requests.get(url).content
            with open("temp_icon.png", "wb") as f:
                f.write(img_data)
            img = Image.open("temp_icon.png").resize((50, 50))
            icon = CTkImage(light_image=img, dark_image=img, size=(50, 50))
            label.configure(image=icon, text="")
            label.image = icon
        except Exception as e:
            self.handle_errors(f"Icon load failed: {e}")

    def display_chart(self, cities, temps):
        if hasattr(self, "chart_widget"):
            self.chart_widget.get_tk_widget().destroy()

        fig, ax = plt.subplots(figsize=(3.5, 1.6), dpi=100)
        ax.bar(cities, temps, color=["#f06292", "#ec407a"])
        ax.set_ylabel("Temp °F")
        ax.set_title("City Comparison")
        ax.set_ylim(0, max(temps) + 10)
        fig.tight_layout()

        self.chart_widget = FigureCanvasTkAgg(fig, master=self.compare_tab)
        self.chart_widget.draw()
        self.chart_widget.get_tk_widget().pack(pady=5)

    def handle_errors(self, error): messagebox.showerror("Error", error)


if __name__ == "__main__":
    app = WeatherApp()
    app.run()
