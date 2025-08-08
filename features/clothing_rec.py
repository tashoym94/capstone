
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
