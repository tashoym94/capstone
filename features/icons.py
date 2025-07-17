import requests
import os
from PIL import Image
import customtkinter as ctk
from customtkinter import CTkImage


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
