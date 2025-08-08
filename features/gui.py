import customtkinter as ctk
import os
from features.weather import WeatherHandler
from features.weather_display import ForecastHandler
from features.city_comparison import HistoryHandler
from features.clothing_rec import handle_errors, on_close
from features.icons import set_icon


class WeatherApp:
    def __init__(self):
        # Set theme and appearance
        ctk.set_appearance_mode("light")
        theme_path = os.path.join(os.path.dirname(
            __file__), "data", "pinktheme.json")
        ctk.set_default_color_theme(theme_path)
        # create window
        self.root = ctk.CTk()
        self.root.title("Weather Dashboard")
        self.root.geometry("900x600")

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)  # Clean shutdown

        self.api_key = os.getenv("open_weather_api_key")
        self.base_url = os.getenv("open_weather_url")
        self.forecast_url = os.getenv("open_weather_forecast_url")

        self.chart_widget = None  # To track the matplotlib chart widget

        self.setup_gui()

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

            set_icon(self.icon1_label, data1['weather'][0]['icon'])
            set_icon(self.icon2_label, data2['weather'][0]['icon'])

    def run(self):
        self.root.mainloop()
