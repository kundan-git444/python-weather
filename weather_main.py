import tkinter as tk
import requests
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap
from datetime import datetime

# Function to get weather data
def get_weather(city):
    API_key = "67da89e70576e4055188cecc9f5673ab"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
    res = requests.get(url)

    if res.status_code == 404:
        messagebox.showerror("City not found")
        return None

    weather = res.json()
    icon_id = weather['weather'][0]['icon']
    temperature = weather['main']['temp'] - 273.15
    description = weather['weather'][0]['description']
    city_name = weather['name']
    country = weather['sys']['country']
    icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
    if not icon_url.startswith('http'):
        icon_url = 'https://' + icon_url

    return icon_url, temperature, description, city_name, country



#Function to search weather for a city
def search():
    city = city_entry.get()
    result = get_weather(city)
    if result is None:
        return "error"
    #if the city is found 
    icon_url, temperature, description, city, country = result
    location_label.configure(text=f"{city},{country}")

    image = Image.open(requests.get(icon_url, stream = True).raw)
    icon = ImageTk.PhotoImage(image)
    icon_label.configure(image = icon)
    icon_label.image = icon

    temperature_label.configure(text=f"Temperature: {temperature:.2f}°C") 
    description_label.configure(text=f"Description: {description}")

    now = datetime.now()
    date_time_label.configure(text=now.strftime("Time: %H:%M"))


root = ttkbootstrap.Window(themename="solar")
root.title("Weather")
root.geometry("400x500")

city_entry = ttkbootstrap.Entry(root, font= "Montserrat, 18")
city_entry.pack(pady = 10)

search_button = ttkbootstrap.Button(root, text = "Search city", command = search, bootstyle="warning")
search_button.pack(pady=10)

location_label = tk.Label(root, font = "Montserrat, 25")
location_label.pack(pady=20)

date_time_label = tk.Label(root, font="Monsterrat, 20")
date_time_label.pack()

icon_label = tk.Label(root)
icon_label.pack()

temperature_label = tk.Label(root, font = "Montserrat, 20")
temperature_label.pack()

description_label = tk.Label(root, font="Montserrat, 20")
description_label.pack()
root.mainloop()

