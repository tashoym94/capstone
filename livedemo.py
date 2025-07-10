import customtkinter as ctk
import requests
import os
import json
import matplotlib.figure as Figure
from datetime import datetime
from dotenv import load_dotenv
from PIL import Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from customtkinter import CTkImage
import gc  # Optional: for clean memory collection on exit

load_dotenv()


class WeatherApp:
    def __init__(self):
        # Set theme and appearance
        ctk.set_appearance_mode("light")
        # Ensure this file exists
        ctk.set_default_color_theme("pinktheme.json")

        self.root = ctk.CTk()
        self.root.title("Weather Dashboard")
        self.root.geometry("420x520")

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)  # Clean shutdown

        self.api_key = os.getenv("open_weather_api_key")
        self.base_url = os.getenv("open_weather_url")

        self.chart_widget = None  # To track the matplotlib chart widget

        self.setup_gui()

    def setup_gui(self):
        self.tabview = ctk.CTkTabview(self.root, width=400, height=470)
        self.tabview.pack(pady=10)

        self.weather_tab = self.tabview.add("Weather")
        self.history_tab = self.tabview.add("History")
        self.compare_tab = self.tabview.add("City Comparison")

        # Weather Tab
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
            self.display_history_table()

    def fetch_weather(self, city):
        try:
            if not self.api_key or not self.base_url:
                raise ValueError("Missing API key or base URL")

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
            history = []
            if os.path.exists("weather_history.json"):
                with open("weather_history.json", "r") as f:
                    history = json.load(f)

            history.append(record)
            with open("weather_history.json", "w") as f:
                json.dump(history[-7:], f, indent=4)

        except Exception as e:
            self.handle_errors(f"Failed to save weather history: {e}")

    def display_history_table(self):
        for widget in self.history_table.winfo_children():
            widget.destroy()

        headers = ["Date", "City", "Temp (°F)", "Description"]
        for i, text in enumerate(headers):
            label = ctk.CTkLabel(self.history_table, text=text,
                                 font=ctk.CTkFont(weight="bold"))
            label.grid(row=0, column=i, padx=5, pady=5)

        try:
            if not os.path.exists("weather_history.json"):
                return

            with open("weather_history.json", "r") as f:
                history = json.load(f)

            for idx, record in enumerate(reversed(history[-7:]), start=1):
                ctk.CTkLabel(self.history_table, text=record['timestamp']).grid(
                    row=idx, column=0, padx=5, pady=2)
                ctk.CTkLabel(self.history_table, text=record['city']).grid(
                    row=idx, column=1, padx=5, pady=2)
                ctk.CTkLabel(self.history_table, text=round(record['temperature'])).grid(
                    row=idx, column=2, padx=5, pady=2)
                ctk.CTkLabel(self.history_table, text=record['description'].title()).grid(
                    row=idx, column=3, padx=5, pady=2)

        except Exception as e:
            self.handle_errors(f"Failed to load history: {e}")

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
                text=f"{data1['name']}: {round(temp1)}°F\n"
                f"{data2['name']}: {round(temp2)}°F\n"
                f"Difference: {diff}°F"
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

            img = Image.open("temp_icon.png")
            ctk_img = CTkImage(light_image=img, size=(50, 50))
            label.configure(image=ctk_img, text="")
            label.image = ctk_img

        except Exception as e:
            self.handle_errors(f"Icon load failed: {e}")

    def display_chart(self, cities, temps):
        if self.chart_widget:
            self.chart_widget.get_tk_widget().destroy()

        fig = Figure.Figure(figsize=(3.5, 1.6), dpi=100)
        ax = fig.add_subplot(111)
        ax.bar(cities, temps, color=["#f06292", "#ec407a"])
        ax.set_ylabel("Temp °F")
        ax.set_title("City Comparison")
        ax.set_ylim(0, max(temps) + 10)
        fig.tight_layout()

        self.chart_widget = FigureCanvasTkAgg(fig, master=self.compare_tab)
        self.chart_widget.draw()
        self.chart_widget.get_tk_widget().pack(pady=5)

    def handle_errors(self, error):
        ctk.CTkMessagebox(title="Error", message=error, icon="cancel")

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


if __name__ == "__main__":
    app = WeatherApp()
    app.run()
