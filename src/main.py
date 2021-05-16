from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
import random
import keyboard
import datetime


class MainMenu(Screen):
    def entry_check(self):
        global current_book
        current_book = ""
        wm.current = "word test"


class LetterTest(Screen):
    write = ObjectProperty(None)
    past_write = ObjectProperty(None)

    def __init__(self, **kwargs):
        # List of used variables
        super(LetterTest, self).__init__(**kwargs)
        self.overall_loop_run = False
        self.loop_run = False
        self.current_time = ""
        self.count = 0
        self.stats = ""
        self.alphabet = ""
        self.current_alphabet = ""
        self.past_alphabet = [" "] * 5

    def on_pre_enter(self, *args):
        # Preparing the loop / Enabling typing process
        self.overall_loop_run = True
        self.write.focus = True
        self.restart_loop()
        self.typing_process()

    def on_pre_leave(self, *args):
        # Stopping the loop
        self.overall_loop_run = False

    def save_results(self):
        # Saving results / Calling results popup
        f = open("database/records.txt", "r")
        self.stats = f.readlines()
        f.close()

        if int(self.ids.LPM.text) > int(self.stats[0].strip()):
            self.stats[0] = self.ids.LPM.text
            f = open("database/records.txt", "w")
            for i in range(3):
                f.write(self.stats[i].strip() + "\n")
            f.close()

        results(self.ids.accuracy.text, self.ids.LPM.text, self.stats[0], "LPM")

    def restart_loop(self):
        # Setting variables to initial values
        self.loop_run = False
        self.current_time = ""
        self.count = 0
        self.past_alphabet = [" "] * len(self.past_alphabet)
        self.ids.read.text = ""
        self.ids.accuracy.text = str(0) + "%"
        self.ids.LPM.text = str(0)
        self.ids.time.text = str(60)
        self.initiate()

    def initiate(self):
        # Generating initial set of letters
        f = open("database/letters.txt", "r")
        self.alphabet = f.readlines()
        self.write.text = ""
        self.past_write.text = "     "

        for i in range(9):
            self.write.text += self.alphabet[random.randint(0, 25)].strip() + "    "
        for i in range(len(self.past_alphabet)):
            self.past_write.text += self.past_alphabet[i] + "    "

        f.close()

    def typing_process(self):
        # Updates on the main text input while in typing process
        self.current_alphabet = self.write.text.split()

        # Fixing space problem
        if self.write.text[0].strip() == "":
            self.write.text = self.write.text[1:]

        # Checking for new input
        try:
            if len(self.current_alphabet[0].strip()) >= 2:
                self.loop_run = True
                char_split(self.current_alphabet[0].strip())

                # Validity of the new input
                if self.current_alphabet[0][0] == self.current_alphabet[0][1]:
                    self.ids.LPM.text = str(int(self.ids.LPM.text) + 1)
                    self.ids.read.color = 0, 1, 0, 1
                else:
                    self.ids.read.color = 1, 0, 0, 1

                self.write.text = ""
                self.past_write.text = "     "

                # Updates on self.write.text
                for i in range(0, len(self.current_alphabet) - 1):
                    self.write.text += self.current_alphabet[i + 1] + "    "
                self.write.text += self.alphabet[random.randint(0, 25)].strip() + "    "

                # Updates on self.past_write.text
                for i in range(0, len(self.past_alphabet) - 1):
                    self.past_alphabet[i] = self.past_alphabet[i + 1]
                    self.past_write.text += self.past_alphabet[i] + "    "
                self.past_alphabet[len(self.past_alphabet) - 1] = self.current_alphabet[0][0]
                self.past_write.text += self.past_alphabet[len(self.past_alphabet) - 1] + "    "

                # Fixing accuracy
                self.count += 1
                self.ids.read.text = self.current_alphabet[0][1].strip()
                self.ids.accuracy.text = str(int(100 * (int(self.ids.LPM.text) / self.count))) + "%"

        except IndexError:
            pass

        # Fixing time
        if float(self.ids.time.text) != 0:
            if self.loop_run:
                if self.current_time == "":
                    self.current_time = datetime.datetime.now().second

                else:
                    if self.current_time != datetime.datetime.now().second:
                        self.current_time = datetime.datetime.now().second
                        self.ids.time.text = str(int(self.ids.time.text) - 1)
        else:
            self.write.focus = False
            self.save_results()
            self.restart_loop()

        # Recalling the loop
        self.write.cursor = (0, 0)
        if self.overall_loop_run:
            Clock.schedule_once(lambda dt: self.typing_process(), 0.01)

    def focus_on(self):
        self.write.focus = True


class WordTest(Screen):
    write = ObjectProperty(None)
    past_write = ObjectProperty(None)

    def __init__(self, **kwargs):
        # List of used variables
        super(WordTest, self).__init__(**kwargs)
        self.overall_loop_run = False
        self.loop_run = False
        self.space_mode = False
        self.correct = True
        self.backspace_enb = True
        self.current_time = ""
        self.fixed_past_text = ""
        self.count = 0
        self.stats = ""
        self.words = ""
        self.current_words = ""
        self.new_word = ""
        self.new_word_count = 0
        self.current_word_lens = [0] * 3

    def on_pre_enter(self, *args):
        # Preparing for a new loop / Enabling typing process
        self.overall_loop_run = True
        self.write.focus = True
        self.space_mode = False
        self.correct = True
        self.backspace_enb = True
        self.restart_loop()
        self.typing_process()

    def on_pre_leave(self, *args):
        # Stopping the loop
        self.overall_loop_run = False

    def save_results(self):
        global current_book
        # Saving results / Calling results popup
        f = open("database/records.txt", "r")
        self.stats = f.readlines()
        f.close()

        if current_book == "":
            if int(self.ids.WPM.text) > int(self.stats[1].strip()):
                self.stats[1] = self.ids.WPM.text

        else:
            if int(self.ids.WPM.text) > int(self.stats[2].strip()):
                self.stats[2] = self.ids.WPM.text

            f = open("database/records.txt", "w")
            for i in range(3):
                f.write(self.stats[i].strip() + "\n")
            f.close()

        if current_book == "":
            results(self.ids.accuracy.text, self.ids.WPM.text, self.stats[1], "WPM")
        else:
            results(self.ids.accuracy.text, self.ids.WPM.text, self.stats[2], "WPM")

    def restart_loop(self):
        # Setting variables to initial values
        self.loop_run = False
        self.space_mode = False
        self.correct = True
        self.backspace_enb = True
        self.current_time = ""
        self.new_word = ""
        self.new_word_count = 3
        self.count = 0
        self.ids.accuracy.text = str(0) + "%"
        self.ids.pro_WPM.text = str(0)
        self.ids.WPM.text = str(0)
        self.ids.time.text = str(60)
        self.initiate()

    def initiate(self):
        global current_book
        # Generating initial word set
        if current_book == "":
            f = open("database/words.txt", "r")
        else:
            f = open("database/" + current_book[7:] + ".txt", "r")

        self.words = f.readlines()
        self.write.text = ""
        self.past_write.text = "     "
        self.fixed_past_text = ""

        for i in range(3):
            if current_book == "":
                self.write.text += self.words[random.randint(0, len(self.words))].strip() + " "
            else:
                self.write.text += self.words[i].strip() + " "

            self.current_words = self.write.text
            self.current_word_lens[i] = len(self.current_words.split()[i])

        f.close()

    def typing_process(self):
        # Updates on main text input during the typing process
        self.current_words = self.write.text.split()

        # Backspace pressed
        if keyboard.is_pressed("backspace"):
            if self.backspace_enb and self.past_write.text.strip() != "":
                self.write.text = \
                    self.fixed_past_text.split()[0][len(self.fixed_past_text) - 1] + self.write.text
                self.past_write.text = self.past_write.text[:-1]
                self.fixed_past_text = self.fixed_past_text[:-1]

                if self.past_write.text.strip() == self.fixed_past_text.strip():
                    self.correct = True
                    self.past_write.color = 0, .3, 1, .6

                self.current_word_lens[0] += 1
                self.backspace_enb = False

        # Space pressed
        elif self.space_mode:
            if self.write.text[0] == self.write.text[1]:
                self.write.text = self.write.text[2:]
                self.space_mode = False
            else:
                if self.write.text[0].strip() != "":
                    self.write.text = self.write.text[1:]

        # Checking for new input
        else:

            # Fixing space problem
            if self.write.text[0].strip() == "":
                self.write.text = self.write.text[1:]

            try:
                if len(self.current_words[0]) > self.current_word_lens[0]:
                    self.loop_run = True
                    self.backspace_enb = True

                    # Validity of new input
                    if self.current_words[0][0] != self.current_words[0][1]:
                        self.correct = False
                        self.past_write.color = 1, 0, 0, 1

                    # Updates on arrays
                    self.past_write.text += self.current_words[0][0]
                    self.fixed_past_text += self.current_words[0][1]
                    self.current_words[0] = self.current_words[0][2:]
                    self.current_word_lens[0] -= 1
                    self.write.text = ""

                    # Whether input completes the word or is a part of it
                    if self.current_word_lens[0] > 0:
                        for i in range(0, len(self.current_words)):
                            self.write.text += self.current_words[i] + " "

                    else:
                        # Another update on arrays / label / text input
                        self.write.text = " "
                        for i in range(0, len(self.current_words) - 1):
                            self.write.text += self.current_words[i + 1] + " "
                            self.current_word_lens[i] = self.current_word_lens[i + 1]

                        global current_book
                        if current_book == "":
                            self.new_word = self.words[random.randint(0, len(self.words))].strip()
                        else:
                            self.new_word = self.words[self.new_word_count].strip()
                            self.new_word_count += 1

                        self.write.text += self.new_word + " "
                        self.current_word_lens[len(self.current_words) - 1] = len(self.new_word)
                        self.past_write.text = "    "
                        self.past_write.color = 0, .3, 1, .6
                        self.fixed_past_text = ""

                        # If word was entered correctly
                        if self.correct:
                            self.ids.WPM.text = str(int(self.ids.WPM.text) + 1)
                        else:
                            self.correct = True

                        self.space_mode = True

                        # Fixing accuracy
                        self.count += 1
                        self.ids.accuracy.text = str(int(100 * (int(self.ids.WPM.text) / self.count))) + "%"

            except IndexError:
                pass

        # Fixing time
        if float(self.ids.time.text) != 0:
            if self.loop_run:
                if self.current_time == "":
                    self.current_time = datetime.datetime.now().second

                else:
                    if self.current_time != datetime.datetime.now().second:
                        self.current_time = datetime.datetime.now().second
                        self.ids.time.text = str(int(self.ids.time.text) - 1)

        else:
            self.write.focus = False
            self.save_results()
            self.restart_loop()

        # Determining projected WPM
        try:
            self.ids.pro_WPM.text = str(int((int(self.ids.WPM.text) / (60 - int(self.ids.time.text))) * 60))
        except ZeroDivisionError:
            pass

        # Determining backspace mode
        time = datetime.datetime.now()
        if float(str(time.second) + "." + str(time.microsecond)[:-5]) % 0.5 == 0 and float(self.ids.time.text) != 60.0:
            if not self.backspace_enb:
                self.backspace_enb = True

        # Recalling the loop
        self.write.cursor = (0, 0)
        if self.overall_loop_run:
            Clock.schedule_once(lambda dt: self.typing_process(), 0.01)

    def focus_on(self):
        self.write.focus = True


class SentenceSelect(Screen):
    def __init__(self, **kwargs):
        super(SentenceSelect, self).__init__(**kwargs)
        self.books = ["images/wonderland.png", "images/plague.jpg", "images/gatsby.png"]
        self.current_book = ""

    def on_pre_enter(self, *args):
        self.current_book = self.ids.book.background_normal

    def new_book(self):
        self.ids.book.background_normal = self.books[random.randint(0, len(self.books) - 1)]
        if self.ids.book.background_normal != self.current_book:
            self.ids.book.background_down = self.ids.book.background_normal
            self.current_book = self.ids.book.background_normal
        else:
            self.new_book()

    def apply_book(self):
        global current_book
        current_book = self.ids.book.background_normal[:-4]
        wm.current = "word test"


class WindowManager(ScreenManager):
    pass


def char_split(string):
    return[char for char in string]


def results(accuracy,  ind, record, ind_text):
    # Results popup
    box = BoxLayout(orientation='vertical', padding=10)
    popup = Popup(title='RESULTS',
                  content=box,
                  size_hint=(None, None), size=(350, 300),
                  auto_dismiss=False)

    popup_label = Label(text="\n" + "Accuracy: " + str(accuracy) + "\n"
                             + str(ind_text) + ": " + str(ind) + "\n"
                             + "Record " + str(ind_text) + ": " + str(record) + "\n",
                        color=(1, 1, 1, 1), font_size=18, bold=True,
                        size_hint=(1, 0.8))

    popup_button = Button(text="Close",
                          size_hint=(1, 0.2),
                          on_press=popup.dismiss)

    popup_button2 = Button(text="Statistics",
                           size_hint=(1, 0.2))

    box.add_widget(popup_label)
    box.add_widget(popup_button)
    box.add_widget(popup_button2)
    popup.open()


current_book = ""
kv = Builder.load_file('kv')
wm = WindowManager()

# All screens
screens = [MainMenu(name="main menu"), WordTest(name="word test"),
           LetterTest(name="letter test"), SentenceSelect(name="sens")]
for screen in screens:
    wm.add_widget(screen)


class TypingTest(App):
    def build(self):
        return wm


if __name__ == "__main__":
    TypingTest().run()
