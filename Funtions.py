import wikipedia
import os
import requests, json  # For weather
import webbrowser as wb
from datetime import date, datetime
# from googletrans import Translator

websites = {'google': 'https://www.google.com/',
        'youtube':'https://www.youtube.com/', 
        'facebook':'https://www.facebook.com/'}

links = {'mail': 'https://mail.google.com/mail/u/2/#inbox'}

def greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return 'Good morning Sir!'
    elif 12 <= hour < 17:
        return 'Good afternoon Sir!'
    elif 17 <= hour < 24:
        return 'Good evening Sir!'
    else:
        return 'Good night Sir!'

def get_weather(city_name):
    api_key = 'be51e8ea300628c1f99c7e2d479cde4d'
    base_url = 'http://api.openweathermap.org/data/2.5/weather?'
    complete_url = base_url + 'appid=' + api_key + '&q=' + city_name
    response = requests.get(complete_url)
    x = response.json()
    try:
        if x['cod'] != '404':
            y = x['main']
            current_temperature = int(y['temp'] - 273.15) # K = C + 273.15
            current_pressure = y['pressure']
            current_humidity = y['humidity']
            z = x['weather']
            weather_description = z[0]['description']
            return f"It's {weather_description} right now, " \
            + f"current temperature is {current_temperature} Celsius, current humidity is {current_humidity}%"
        else:
            return "Sorry! I can't find this city! Please make sure the city's name you provided is correct!"
    except:
        return "Sorry! An error occurred while searching for this city's weather information!"

def get_today():
    today = date.today().strftime('%A, %B %d, %Y')
    return f'Today is {today}.'

def get_current_time():
    now = datetime.now()
    return f"Now is {now.hour} hours {now.minute} minutes {now.second} seconds."

# def translate(key, lang_src='en', lang_dest='vi'):
#     return Translator().translate(key, src=lang_src, dest=lang_dest).text

def search_wikipedia(keyword, lang='en'):
    wikipedia.set_lang(lang)
    try:
        return wikipedia.summary(title=keyword, sentences=1)
    except:
        return "Can't not find any pages with this keyword you provided! Please try again!"

def open_website(link):
    wb.open(links[link])

def open_and_search_website(link, query=''):
    url = f'{websites[link]}search?q={query}'
    wb.get().open(url)

def play_music():
    music_dir = r'D:\Music'
    songs = os.listdir(music_dir)
    os.startfile(os.path.join(music_dir,songs[0]))