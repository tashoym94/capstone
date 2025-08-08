import requests
import os
import customtkinter as ctk
import json
import matplotlib.dates as mdates
import matplotlib
import csv
import re
from datetime import datetime
import pandas as pd
import glob
import matplotlib.pyplot as plt
import matplotlib.figure as Figure
from datetime import datetime
from tkinter import messagebox
from dotenv import load_dotenv
from PIL import Image
from features.icons import set_icon  # Importing set_icon from icons.py
from features.city_comparison import compare_cities
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from customtkinter import CTkImage
import gc  # Optional: for clean memory collection on exit
import numpy as np  # Add this import at the top of your file if not already present

load_dotenv()


class WeatherApp:
    def on_close(self):
        try:
            # Clean up chart widget
            if self.chart_widget:
                try:
                    self.chart_widget.get_tk_widget().destroy()
                except:
                    pass

            # Remove temp icon image
            if os.path.exists("temp_icon.png"):
                try:
                    os.remove("temp_icon.png")
                except:
                    pass

            # Cancel all scheduled after callbacks (important on macOS)
            try:
                pending = self.root.tk.call('after', 'info')
                for cb in pending:
                    try:
                        self.root.after_cancel(cb)
                    except:
                        pass
            except:
                pass

        except Exception as e:
            print("Shutdown error:", e)

        gc.collect()  # Optional: force garbage collection
        self.root.quit()
        self.root.destroy()

    def __init__(self):
        # Set theme and appearance
        ctk.set_appearance_mode("light")
        theme_path = os.path.join(os.path.dirname(
            __file__), "data", "pinktheme.json")
        ctk.set_default_color_theme(theme_path)
        # create window
        self.root = ctk.CTk()
        self.units = "imperial"
        self.theme = ctk.get_appearance_mode()  # current theme
        self.favorite_city = None  # no favorite city initially

        self.root.title("Weather Dashboard")
        self.root.geometry("900x600")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)  # Clean shutdown

        self.api_key = os.getenv("open_weather_api_key")
        self.base_url = os.getenv("open_weather_url")
        self.forecast_url = os.getenv("open_weather_forecast_url")

        self.chart_widget = None  # To track the matplotlib chart widget
        self.compare_cities = compare_cities.__get__(self, WeatherApp)

        self.graph_csv_list = []  # Stores selected filenames for group graph

        self.setup_gui()

    def get_clothing_recommendation(self, temp, condition):
        if temp < 40:
            outfit = "🧥 Heavy jacket, gloves, and scarf"
        elif temp < 60:
            outfit = "🧣 Light jacket or sweater"
        elif temp < 75:
            outfit = "👕 Long sleeves or hoodie"
        elif temp < 85:
            outfit = "👖 T-shirt and jeans or shorts"
        else:
            outfit = "🩳 Tank top, shorts, and stay hydrated"

        if "rain" in condition.lower():
            outfit += " ☔ Bring an umbrella or raincoat"
        elif "snow" in condition.lower():
            outfit += " ❄️ Wear waterproof boots"

        return outfit

    def display_group_feature_graph(self):
        for widget in self.group_tab.winfo_children():
            widget.destroy()

        try:
            folder_path = "./Group_feature/Team_csv"
            csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

            if not csv_files:
                ctk.CTkLabel(self.group_tab, text="No CSV files found.").pack()
                return

            fig, ax = plt.subplots(figsize=(6, 4))

            for file in csv_files:
                df = pd.read_csv(file)

                # Combine Date and Time into a single datetime column
                df['datetime'] = pd.to_datetime(
                    df['Date'] + ' ' + df['Time'], errors='coerce')
                df = df.dropna(subset=['datetime', 'Temperature_F'])
                df = df.sort_values('datetime')

                label = os.path.basename(file).replace(".csv", "")
                ax.plot(df['datetime'], df['Temperature_F'], label=label)

                ax.set_title("Group Temperature Trends")
                ax.set_xlabel("Date")
                ax.set_ylabel("Temperature (°F)")
                ax.legend()
                ax.grid(True)

                canvas = FigureCanvasTkAgg(fig, master=self.group_tab)
                canvas.draw()
                canvas.get_tk_widget().pack(fill="both", expand=True)

        except Exception as e:
            self.handle_errors(f"Failed to load group data: {e}")

    def fetch_forecast(self, city):
        try:
            if not self.forecast_url:
                raise ValueError("Forecast URL is missing.")

            params = {'q': city, 'appid': self.api_key, 'units': self.units}
            response = requests.get(
                self.forecast_url, params=params, timeout=10)

            if response.status_code == 200:
                return response.json()
            else:
                self.handle_errors(
                    f"Failed to fetch forecast data. Status: {response.status_code}")
                return None
        except Exception as e:
            self.handle_errors(f"Forecast error: {e}")
            return None

    def setup_gui(self):

        self.tabview = ctk.CTkTabview(self.root, width=400, height=470)
        self.tabview.pack(pady=10)

        self.weather_tab = self.tabview.add("Weather")
        self.history_tab = self.tabview.add("History")
        self.compare_tab = self.tabview.add("City Comparison")
        self.forecast_tab = self.tabview.add("5-Day Forecast")
        self.group_tab = self.tabview.add("Group Feature")
        self.setup_group_tab()

        # Weather Tab Widgets
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

        self.update_label = ctk.CTkLabel(
            self.weather_tab, text="", font=ctk.CTkFont(size=10))
        self.update_label.pack()

        self.feelslike_label = ctk.CTkLabel(
            self.weather_tab, text="", font=ctk.CTkFont(size=12))
        self.feelslike_label.pack()

        self.humidity_label = ctk.CTkLabel(
            self.weather_tab, text="", font=ctk.CTkFont(size=12))
        self.humidity_label.pack()

        self.wind_label = ctk.CTkLabel(
            self.weather_tab, text="", font=ctk.CTkFont(size=12))
        self.wind_label.pack()

        self.outfit_label = ctk.CTkLabel(
            self.weather_tab, text="", font=ctk.CTkFont(size=12))
        self.outfit_label.pack(pady=5)

        self.weather_icon_label = ctk.CTkLabel(self.weather_tab, text="")
        self.weather_icon_label.pack(pady=5)

        # History Tab
        self.history_table = ctk.CTkFrame(self.history_tab)
        self.history_table.pack(pady=10, padx=10, fill="both", expand=True)
        self.display_history_table()

        # City Comparison Tab
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

        # Forecast Tab
        forecast_input = ctk.CTkFrame(self.forecast_tab)
        forecast_input.pack(pady=5)

        self.forecast_city_entry = ctk.CTkEntry(
            forecast_input, width=200, placeholder_text="Enter City")
        self.forecast_city_entry.pack(side="left", padx=5)

        forecast_btn = ctk.CTkButton(
            forecast_input, text="Show Forecast", command=self.get_forecast_click)
        forecast_btn.pack(side="left", padx=5)

        self.forecast_display = ctk.CTkFrame(self.forecast_tab)
        self.forecast_display.pack(pady=10, fill="both", expand=True)

    def setup_group_tab(self):
        # Dropdown for CSV selection
        self.csv_options = self.get_csv_file_list()
        self.selected_csv = ctk.StringVar(value="")

        ctk.CTkLabel(self.group_tab, text="Select User CSV(s):").pack(
            pady=(10, 0))

        self.csv_selector = ctk.CTkComboBox(
            self.group_tab,
            values=self.csv_options,
            variable=self.selected_csv,
            width=300,
            state="normal"
        )
        self.csv_selector.pack(pady=5)

        add_button = ctk.CTkButton(
            self.group_tab,
            text="Add CSV to Graph",
            command=self.add_csv_to_graph
        )
        add_button.pack(pady=5)

        self.graph_canvas_frame = ctk.CTkFrame(self.group_tab)
        self.graph_canvas_frame.pack(fill="both", expand=True)

        self.graph_csv_list = []  # Stores selected filenames

    def get_csv_file_list(self):
        folder_path = "./Group_feature/Team_csv"
        csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
        return [os.path.basename(f) for f in csv_files]

    def add_csv_to_graph(self):
        selected_file = self.csv_selector.get()
        if selected_file and selected_file not in self.graph_csv_list:
            self.graph_csv_list.append(selected_file)
            self.update_group_graph()

    def get_weather_click(self):
        city = self.city_entry.get().strip()
        if not city:
            self.handle_errors("Please enter a city name.")
            return

        weather_data = self.fetch_weather(city)
        if weather_data:
            self.display_weather(weather_data)
            self.save_weather(weather_data)
            self.display_history_table()

    def get_forecast_click(self):
        city = self.forecast_city_entry.get().strip()
        if not city:
            self.handle_errors("Please enter a city name.")
            return

        forecast_data = self.fetch_forecast(city)
        if forecast_data:
            self.display_forecast(forecast_data)

    def display_forecast(self, data):
        for widget in self.forecast_display.winfo_children():
            widget.destroy()

        # Filter 5 daily forecasts (1 per day, approx every 8th)
        daily_forecasts = [item for idx, item in enumerate(
            data['list']) if idx % 8 == 0][:5]

        row_frame = ctk.CTkFrame(self.forecast_display)
        row_frame.pack(pady=10, padx=10, fill="x")

        for forecast in daily_forecasts:
            date = forecast['dt_txt'].split(" ")[0]
            temp = round(forecast['main']['temp'])
            desc = forecast['weather'][0]['description'].title()
            humidity = forecast['main']['humidity']
            wind = forecast['wind']['speed']
            icon_code = forecast['weather'][0]['icon']

            # Create each forecast block
            block = ctk.CTkFrame(row_frame, width=150,
                                 height=200, corner_radius=12)
            block.pack(side="left", padx=10, pady=5)
            block.pack_propagate(False)

            # Load and show icon
            try:
                url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
                img_data = requests.get(url).content
                with open(f"forecast_icon_{date}.png", "wb") as f:
                    f.write(img_data)

                img = Image.open(f"forecast_icon_{date}.png")
                ctk_img = CTkImage(light_image=img, size=(50, 50))
                icon_label = ctk.CTkLabel(block, image=ctk_img, text="")
                icon_label.image = ctk_img  # prevent garbage collection
                icon_label.pack()
            except:
                ctk.CTkLabel(block, text="(No Icon)").pack()

            # Display forecast info
            ctk.CTkLabel(block, text=f"{date}", font=ctk.CTkFont(
                size=12, weight="bold")).pack()
            ctk.CTkLabel(
                block, text=f"{temp}°F | {desc}", wraplength=120).pack()
            ctk.CTkLabel(block, text=f"💧 {humidity}%").pack()
            ctk.CTkLabel(block, text=f"🌬 {wind} mph").pack()

    def _parse_datetime_safe(self, date_str, time_str):  # Add 'self' here
        s = f"{str(date_str).strip()} {str(time_str).strip()}"
        # Normalize "11:45pm" -> "11:45 PM"
        # Ensure space before am/pm
        s = re.sub(r'(?i)(\d)\s*(am|pm)$', r'\1 \2', s)
        s = re.sub(r'(?i)(am|pm)$', lambda m: f"{m.group(1).upper()}", s)

        for fmt in ("%Y-%m-%d %I:%M %p", "%Y-%m-%d %H:%M"):
            try:
                return datetime.strptime(s, fmt)  # Naive local time
            except ValueError:
                continue
        return pd.NaT

    def update_group_graph(self):
        # Clear the old graph
        for widget in self.graph_canvas_frame.winfo_children():
            widget.destroy()

        folder_path = "./Group_feature/Team_csv"
        fig, ax = plt.subplots(figsize=(6, 4))

        csv_count = len(self.graph_csv_list)
        if csv_count == 0:
            ctk.CTkLabel(self.graph_canvas_frame,
                         text="No CSV files selected").pack()
            return

        # Use the updated colormap function
        colormap = matplotlib.colormaps['tab10']
        colors = [colormap(i / max(1, csv_count - 1))
                  for i in range(csv_count)]

        for i, filename in enumerate(self.graph_csv_list):
            file_path = os.path.join(folder_path, filename)
            print(f"Loading file: {file_path}")

            try:
                df = pd.read_csv(file_path)
                print("First rows:")
                print(df.head())

                # Build deterministic datetimes
                df["datetime"] = [self._parse_datetime_safe(
                    d, t) for d, t in zip(df["Date"], df["Time"])]

                # Clean and sort
                before = len(df)
                df = df.dropna(
                    subset=["datetime", "Temperature_F"]).sort_values("datetime")
                print(f"[{filename}] Parsed {before} -> {len(df)} rows. "
                      f"min={df['datetime'].min() if not df.empty else None}, "
                      f"max={df['datetime'].max() if not df.empty else None}")

                if df.empty:
                    continue

                label = df["City"].iloc[0] if "City" in df.columns else filename.replace(
                    ".csv", "")
                ax.plot(df["datetime"], df["Temperature_F"],
                        label=label, marker="o", color=colors[i])

            except Exception as e:
                print(f"❌ Error loading {filename}: {e}")

        # Axis formatting
        ax.set_title("Group Temperature Trends")
        ax.set_xlabel("Date/Time")
        ax.set_ylabel("Temperature (°F)")
        ax.legend()
        ax.grid(True)
        fig.autofmt_xdate(rotation=45)

        canvas = FigureCanvasTkAgg(fig, master=self.graph_canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def get_weather_click(self):
        city = self.city_entry.get().strip()
        if not city:
            self.handle_errors("Please enter a city name.")
            return

        weather_data = self.fetch_weather(city)
        if weather_data:
            self.display_weather(weather_data)
            self.save_weather(weather_data)
            self.display_history_table()

    def get_forecast_click(self):
        city = self.forecast_city_entry.get().strip()
        if not city:
            self.handle_errors("Please enter a city name.")
            return

        forecast_data = self.fetch_forecast(city)
        if forecast_data:
            self.display_forecast(forecast_data)

    def display_forecast(self, data):
        for widget in self.forecast_display.winfo_children():
            widget.destroy()

        # Filter 5 daily forecasts (1 per day, approx every 8th)
        daily_forecasts = [item for idx, item in enumerate(
            data['list']) if idx % 8 == 0][:5]

        row_frame = ctk.CTkFrame(self.forecast_display)
        row_frame.pack(pady=10, padx=10, fill="x")

        for forecast in daily_forecasts:
            date = forecast['dt_txt'].split(" ")[0]
            temp = round(forecast['main']['temp'])
            desc = forecast['weather'][0]['description'].title()
            humidity = forecast['main']['humidity']
            wind = forecast['wind']['speed']
            icon_code = forecast['weather'][0]['icon']

            # Create each forecast block
            block = ctk.CTkFrame(row_frame, width=150,
                                 height=200, corner_radius=12)
            block.pack(side="left", padx=10, pady=5)
            block.pack_propagate(False)

            # Load and show icon
            try:
                url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
                img_data = requests.get(url).content
                with open(f"forecast_icon_{date}.png", "wb") as f:
                    f.write(img_data)

                img = Image.open(f"forecast_icon_{date}.png")
                ctk_img = CTkImage(light_image=img, size=(50, 50))
                icon_label = ctk.CTkLabel(block, image=ctk_img, text="")
                icon_label.image = ctk_img  # prevent garbage collection
                icon_label.pack()
            except:
                ctk.CTkLabel(block, text="(No Icon)").pack()

            # Display forecast info
            ctk.CTkLabel(block, text=f"{date}", font=ctk.CTkFont(
                size=12, weight="bold")).pack()
            ctk.CTkLabel(
                block, text=f"{temp}°F | {desc}", wraplength=120).pack()
            ctk.CTkLabel(block, text=f"💧 {humidity}%").pack()
            ctk.CTkLabel(block, text=f"🌬 {wind} mph").pack()

    def fetch_weather(self, city):
        try:
            if not self.api_key or not self.base_url:
                raise ValueError("Missing API key or base URL")

            params = {'q': city, 'appid': self.api_key, 'units': self.units}
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
        self.update_label.configure(
            text=f"Updated: {datetime.now().strftime('%I:%M %p')}")
        self.feelslike_label.configure(
            text=f"Feels like: {round(data['main']['feels_like'])}°F")
        self.humidity_label.configure(
            text=f"Humidity: {data['main']['humidity']}%")
        self.wind_label.configure(
            text=f"Wind Speed: {data['wind']['speed']} mph")

        set_icon(self.weather_icon_label, data['weather'][0]['icon'])

        temp = data['main']['temp']
        condition = data['weather'][0]['description']
        recommendation = self.get_clothing_recommendation(temp, condition)
        self.outfit_label.configure(
            text=f"Outfit Suggestion: {recommendation}")

    def save_weather(self, data):
        record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "city": data['name'],
            "temperature": data['main']['temp'],
            "feels_like": data['main']['feels_like'],
            "humidity": data['main']['humidity'],
            "wind_speed": data['wind']['speed'],
            "description": data['weather'][0]['description']
        }

        try:
            history = []
            if os.path.exists("weather_history.json"):
                with open("weather_history.json", "r") as f:
                    history = json.load(f)

            history.append(record)

            with open("weather_history.json", "w") as f:
                json.dump(history[-25:], f, indent=4)  # Keep last 25 records

            try:
                csv_file = "weather_history2.csv"
                file_exists = os.path.exists(csv_file)
                with open(csv_file, "a", newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=record.keys())
                    if not file_exists:
                        writer.writeheader()
                    writer.writerow(record)

            except Exception as csv_err:
                self.handle_errors(f"Failed to write CSV: {csv_err}")

        except Exception as e:
            self.handle_errors(f"Failed to save weather history: {e}")

    def display_history_table(self):
        for widget in self.history_table.winfo_children():
            widget.destroy()

        headers = ["Date", "City",
                   "Temp (°F)", "Feels Like", "Humidity", "Wind", "Description"]
        for i, text in enumerate(headers):
            label = ctk.CTkLabel(self.history_table, text=text,
                                 font=ctk.CTkFont(weight="bold"))
            label.grid(row=0, column=i, padx=4, pady=4)

        try:
            if not os.path.exists("weather_history.json"):
                return

            with open("weather_history.json", "r") as f:
                history = json.load(f)

            for idx, record in enumerate(reversed(history[-10:]), start=1):
                ctk.CTkLabel(self.history_table, text=record['timestamp']).grid(
                    row=idx, column=0, padx=4, pady=2)
                ctk.CTkLabel(self.history_table, text=record['city']).grid(
                    row=idx, column=1, padx=4, pady=2)
                ctk.CTkLabel(self.history_table, text=round(record['temperature'])).grid(
                    row=idx, column=2, padx=4, pady=2)
                ctk.CTkLabel(self.history_table, text=round(record.get('feels_like', 0))).grid(
                    row=idx, column=3, padx=4, pady=2)
                ctk.CTkLabel(self.history_table, text=f"{record.get('humidity', 'N/A')}%").grid(
                    row=idx, column=4, padx=4, pady=2)
                ctk.CTkLabel(self.history_table, text=f"{record.get('wind_speed', 'N/A')} mph").grid(
                    row=idx, column=5, padx=4, pady=2)

                ctk.CTkLabel(self.history_table, text=record['description'].title()).grid(
                    row=idx, column=6, padx=4, pady=2)

        except Exception as e:
            self.handle_errors(f"Failed to load history: {e}")

    def display_chart(self, cities, temps):
        if self.chart_widget:
            self.chart_widget.get_tk_widget().destroy()

        fig = Figure.Figure(figsize=(3.5, 1.6), dpi=100)
        ax = fig.add_subplot(111)

        ax.plot(cities, temps, marker='o', color="#ec407a", linewidth=2)
        ax.set_ylabel("Temp (°F)")
        ax.set_title("City Comparison (Line Chart)")
        ax.set_ylim(0, max(temps) + 10)
        ax.grid(True, linestyle='--', alpha=0.6)

        fig.tight_layout()

        self.chart_widget = FigureCanvasTkAgg(fig, master=self.compare_tab)
        self.chart_widget.draw()
        self.chart_widget.get_tk_widget().pack(pady=5)

    def handle_errors(self, error):
        messagebox.showerror("Error", error)

    def on_close(self):
        try:
            # Clean up chart widget
            if self.chart_widget:
                try:
                    self.chart_widget.get_tk_widget().destroy()
                except:
                    pass

            # Remove temp icon image
            if os.path.exists("temp_icon.png"):
                try:
                    os.remove("temp_icon.png")
                except:
                    pass

            # Cancel all scheduled after callbacks (important on macOS)
            try:
                pending = self.root.tk.call('after', 'info')
                for cb in pending:
                    try:
                        self.root.after_cancel(cb)
                    except:
                        pass
            except:
                pass

        except Exception as e:
            print("Shutdown error:", e)

        gc.collect()  # Optional: force garbage collection
        self.root.quit()
        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = WeatherApp()
    app.run()
