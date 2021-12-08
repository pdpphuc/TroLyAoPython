import speech_recognition
import pyttsx3
import pyttsx3.drivers.sapi5

from Person import *
from Mode import *
from Funtions import *

class MyAssistant:

    def __init__(self, boss, name='Your assistant', age=0, gender='Female'):
        # Thông tin cá nhân
        self.boss = boss
        self.name = name
        self.age = age
        self.gender = gender

        # Các bộ phận
        self.ear = speech_recognition.Recognizer()

        self.mouth = pyttsx3.init()
        self.mouth.setProperty('rate', 250)
        self.voices = self.mouth.getProperty('voices')
        self.voice_id = 1

        self.mode = Mode.SPEAKING_MODE

    @property
    def voice_id(self):
        return self.__voice_id

    @voice_id.setter
    def voice_id(self, value):
        self.__voice_id = value
        self.mouth.setProperty('voice', self.voices[value].id)

    # Đổi giọng
    def change_voice(self):
        self.voice_id = 0 if self.voice_id == 1 else 1
        self.say(f'Hello {self.boss.name}! This is my new voice!')

    # Nghe
    def hear(self):
        with speech_recognition.Microphone() as mic:
            # self.ear.pause_threshold = 2
            self.ear.adjust_for_ambient_noise(mic, duration=0.5)
            audio = self.ear.listen(mic)
        try:
            print(f'{self.name}: ...')
            you = self.ear.recognize_google(audio, language='en')
        except:
            you = ''
        # you = input('{0:>{1}}: '.format(self.boss.name, len(self.name)))
        print('{0:>{1}}: {2}'.format(self.boss.name, len(self.name), you))
        return you

    # Nói
    def say(self, sentence):
        print(self.name + ": " + sentence)
        self.mouth.say(sentence)
        self.mouth.runAndWait()

    # Hỏi
    def ask(self, sentence=None):
        if sentence:
            self.say(sentence)
        if self.mode == Mode.SPEAKING_MODE:
            you = self.hear()
        elif self.mode == Mode.TYPING_MODE:
            you = input('Type your answer here >>> ')
        return you.strip()

    # Sống
    def live(self):
        self.say(greeting())
        while True:
            self.say('How can I help you?')
            if self.mode == Mode.SPEAKING_MODE:
                you = self.hear()
            elif self.mode == Mode.TYPING_MODE:
                you = input('Type your command here >>> ')
            you = you.strip().lower()

            # Không có
            if you == '':
                if self.mode == Mode.SPEAKING_MODE:
                    self.say("Sorry! I can't hear what you're saying! Please try again!")
                elif self.mode == Mode.TYPING_MODE:
                    self.say("Sorry! Your answer can't be empty!")
            # Đổi chế độ nói
            elif 'speaking' in you:
                self.mode = Mode.SPEAKING_MODE
                self.say(f'OK Sir! The mode now will be change to {self.mode}!')
            # Đổi chế độ gõ
            elif 'typing' in you:
                self.mode = Mode.TYPING_MODE
                self.say(f'OK Sir! The mode now will be change to {self.mode}!')
            # Đổi giọng
            elif 'change voice' in you:
                self.change_voice()
            # Chào hỏi
            elif any(greeting in you.split() for greeting in ['hello', 'hi']):
                self.say(f'Hello {self.boss.name}! Nice to meet you!')
            # Đổi tên bot
            elif 'name' in you:
                newName = self.ask('What do you want my new name to be?')
                while newName == '':
                    newName = self.ask("I still haven't received your answer! Please try again!")
                self.name = newName
                self.say(f'OK Sir! My name will be {self.name}.')
            # Đổi tuổi bot
            elif 'age' in you:
                self.say('What do you want my new age to be?')
                while True:
                    answer = input('Type my new age here >>> ')
                    if not answer.isdigit():
                        self.say('My new age must be a positive integer! Please type again!')
                    else:
                        break
                self.age = int(answer)
                self.say(f'OK Sir! My age will be {self.age}.')
            # Hỏi ngày
            elif 'today' in you:
                self.say(get_today())
            # Hỏi giờ
            elif 'time' in you:
                self.say(get_current_time())
            # Xem thời tiết
            elif 'weather' in you:
                city = self.ask('Which city do you want to see the weather of?')
                while city == '':
                    city = self.ask("I still haven't received your answer! Please try again!")
                self.say(get_weather(city))
            elif 'wiki' in you:
                key = self.ask('What information do you want to find?')
                while key == '':
                    key = self.ask("I still haven't received your answer! Please try again!")
                else:
                    self.say(search_wikipedia(key))
            elif 'music' in you:
                play_music()
                self.say('I turned on the music for you!')
            elif any(website in you for website in websites.keys()):
                web = next(web for web in websites.keys() if web in you)
                query = self.ask('What should I search for you?')
                while query == '':
                    query = self.ask("I still haven't received your answer! Please try again!")
                open_and_search_website(web, query)
                self.say(f'Here is your "{query}" on {web}!')
            elif any(link in you for link in links.keys()):
                link = next(link for link in links.keys() if link in you)
                open_website(link)
                self.say(f'I opened {link} for you!')
            elif any(s in you.split() for s in ['quit', 'q', 'bye', 'goodbye']):
                self.say(f'{self.name} is quitting... Goodbye boss!')
                quit()
            elif 'shut down' in you:
                options = 'Yes/No' if self.mode == Mode.SPEAKING_MODE else 'y/n'
                while True:
                    self.say(f'Are you sure you want to shutdown the computer? [{options}]')
                    ans = self.ask().lower()
                    if ans == 'yes' or ans == 'y':
                        self.say('OK Sir! I will shutdown the computer! Goodbye boss!')
                        os.system('shutdown -s')
                    elif ans == 'no' or ans == 'n':
                        break
                    else:
                        self.say(f'You must choose one in two options [{options}]!')
            elif 'restart' in you:
                options = 'Yes/No' if self.mode == Mode.SPEAKING_MODE else 'y/n'
                while True:
                    self.say(f'Are you sure you want to restart the computer? [{options}]')
                    ans = self.ask().lower()
                    if ans == 'yes' or ans == 'y':
                        self.say('OK Sir! I will restart the computer! Goodbye boss!')
                        quit(os.system('shutdown -r'))
                    elif ans == 'no' or ans == 'n':
                        break
                    else:
                        self.say(f'You must choose one in two options [{options}]!')
            else:
                self.say("Sorry! I haven't learned your command yet!")