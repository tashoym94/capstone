from features.icons import set_icon


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
        self.display_chart([data1['name'], data2['name']], [temp1, temp2])
