import sys
import csv
from PyQt5.QtWidgets import QApplication, QMainWindow
import time
from PyQt5 import QtWidgets, QtCore
from smth import Ui_MainWindow
from PyQt5.Qt import QPalette, QBrush, QSize, QImage
from threading import Thread
import keyboard
import pygame
import shutil
import numpy as np
import os
import pydub
import threading
import os.path
from functools import partial
import pyaudio
import wave

note = ''
song = ''
text = ''
new_dir = 'default'
all_simb = '1234567890qwertyuiopasdfghjklzxcvbnm'

directories = ['default']
custom = {}

file2 = open("music.csv", 'w')
file3 = open("music2.csv", 'w')
file2.close()
file3.close()
file = open("music.csv", 'r+')
reader = csv.reader(file, delimiter=',')
gg = set()
for row in reader:
    if row:
        gg.add(row[0])
directories.extend(gg)


def play_base_setups():
    global text, custom
    th1 = threading.currentThread()
    pygame.init()
    pygame.mixer.set_num_channels(50)
    pydub.AudioSegment.converter = os.getcwd() + "\\ffmpeg.exe"
    pydub.AudioSegment.ffprobe = os.getcwd() + "\\ffprobe.exe"
    # used try so that if user pressed other than the given key error will not be shown
    strr = '1234567890'
    data = [[i] for i in list(strr)]

    def read(f, normalized=False):
        """MP3 to numpy array"""
        try:
            a = pydub.AudioSegment.from_mp3(f)
        except Exception:
            a = pydub.AudioSegment.from_file(f)
        y = np.array(a.get_array_of_samples())
        if a.channels == 2:
            y = y.reshape((-1, 2))
        if normalized:
            return a.frame_rate, np.float32(y) / 2 ** 15
        else:
            return a.frame_rate, y

    def speedx(sound_array, factor):
        """ Multiplies the sound's speed by some `factor` """
        indices = np.round(np.arange(0, len(sound_array), factor))
        indices = indices[indices < len(sound_array)].astype(int)
        return sound_array[indices.astype(int)]
        # export / save pitch changed sound

    def write(f, sr, x, normalized=False):
        """numpy array to MP3"""
        channels = 2 if (x.ndim == 2 and x.shape[1] == 2) else 1
        if normalized:  # normalized array - each item should be a float in [-1, 1)
            y = np.int16(x * 2 ** 15)
        else:
            y = np.int16(x)
        song = pydub.AudioSegment(y.tobytes(), frame_rate=sr, sample_width=2, channels=channels)
        song.export(f, format="mp3", bitrate="320k")

    def do(f_in, f_out, factor):
        w, s = read(f_in)
        hipitch_sound = speedx(s, factor)
        write(f_out, w, hipitch_sound)

    def func():
        folder_from = os.getcwd() + r'\alfabet'
        folder_to = os.getcwd()
        for f in os.listdir(folder_from):
            if os.path.isfile(os.path.join(folder_from, f)):
                shutil.copy(os.path.join(folder_from, f), os.path.join(folder_to, f))
            if os.path.isdir(os.path.join(folder_from, f)):
                os.system(f'rd /S /Q {folder_to}\\{f}')
                shutil.copytree(os.path.join(folder_from, f), os.path.join(folder_to, f))
        folder_from = os.getcwd() + r'\music'
        folder_to = os.getcwd()

        for f in os.listdir(folder_from):
            if os.path.isfile(os.path.join(folder_from, f)):
                shutil.copy(os.path.join(folder_from, f), os.path.join(folder_to, f))
            if os.path.isdir(os.path.join(folder_from, f)):
                os.system(f'rd /S /Q {folder_to}\\{f}')
                shutil.copytree(os.path.join(folder_from, f), os.path.join(folder_to, f))
        if not os.path.isdir("Custom"):
            os.mkdir("Custom")
        folder_from = os.getcwd() + r'\custom'
        folder_to = os.getcwd()

        for f in os.listdir(folder_from):
            if os.path.isfile(os.path.join(folder_from, f)):
                shutil.copy(os.path.join(folder_from, f), os.path.join(folder_to, f))
            if os.path.isdir(os.path.join(folder_from, f)):
                os.system(f'rd /S /Q {folder_to}\\{f}')
                shutil.copytree(os.path.join(folder_from, f), os.path.join(folder_to, f))

    def do_note():
        folder_from = os.getcwd() + r'\notes'
        folder_to = os.getcwd()

        for f in os.listdir(folder_from):
            if os.path.isfile(os.path.join(folder_from, f)):
                shutil.copy(os.path.join(folder_from, f), os.path.join(folder_to, f))
            if os.path.isdir(os.path.join(folder_from, f)):
                os.system(f'rd /S /Q {folder_to}\\{f}')
                shutil.copytree(os.path.join(folder_from, f), os.path.join(folder_to, f))

    let = {
        'num': [1],
        'q': ['Quiet You - QuickSounds.com.mp3', False],
        'w': ['weeeee_original_1193597514938524841.mp3', False],
        'e': ['ea-sports_FKtJ2U8.mp3', False],
        'r': ['welcome-to-the-gulag.mp3', False],
        't': ['Two Hours Later (Spongebob) - QuickSounds.com.mp3', False],
        'y': ['Yodeling Kid - QuickSounds.com.mp3', False],
        'u': [False],
        'i': ["It's Corn Song Meme Sound Effect.mp3", False],
        'o': ['Ohhh My God Meme - QuickSounds.com.mp3', False],
        'p': ['Tik tok - a person who thinks all the time (1).mp3', False],
        'a': ['aaaaugh_YxUGh8a.mp3', False],
        's': ['smash-mouth-all-stars-ost-shrek.mp3', False],
        'd': [False],
        'f': [False],
        'g': ['No God Please No - Sound Effect.mp3', False],
        'h': ['forrest_gump_27 Sweet Home Alabama.mp3', False],
        'j': ['ooo.mp3', False],
        'k': ['nioce.mp3', False],
        'l': ['Look At This Dude - QuickSounds.com.mp3', False],
        'z': ['What Are Those - QuickSounds.com.mp3', False],
        'x': [False],
        'c': ['KDmqo2yv61Y_The-Coconut-Song---Da-Coconut-Nut-.mp3', False],
        'v': [False],
        'b': [False],
        'n': ['Never Gonna Give You Up Original.mp3', False],
        'm': ['mayo-escalator.mp3', False],
    }
    let2 = {
        'num': [2],
        'q': ['q (mp3cut.net).mp3', False],
        'w': ['w (mp3cut.net).mp3', False],
        'e': ['e (mp3cut.net).mp3', False],
        'r': ['r (mp3cut.net).mp3', False],
        't': ['t (mp3cut.net).mp3', False],
        'y': ['y (mp3cut.net).mp3', False],
        'u': ['u (mp3cut.net).mp3', False],
        'i': ['i (mp3cut.net).mp3', False],
        'o': ['o (mp3cut.net).mp3', False],
        'p': ['p (mp3cut.net).mp3', False],
        'a': ['a (mp3cut.net).mp3', False],
        's': ['s (mp3cut.net).mp3', False],
        'd': ['d (mp3cut.net).mp3', False],
        'f': ['f (mp3cut.net).mp3', False],
        'g': ['g (mp3cut.net).mp3', False],
        'h': ['h (mp3cut.net).mp3', False],
        'j': ['j (mp3cut.net).mp3', False],
        'k': ['k (mp3cut.net).mp3', False],
        'l': ['l (mp3cut.net).mp3', False],
        'z': ['z (mp3cut.net).mp3', False],
        'x': ['x (mp3cut.net).mp3', False],
        'c': ['c (mp3cut.net).mp3', False],
        'v': ['v (mp3cut.net).mp3', False],
        'b': ['b (mp3cut.net).mp3', False],
        'n': ['n (mp3cut.net).mp3', False],
        'm': ['m (mp3cut.net).mp3', False],
        'escape': ['esc_KNfNlOfG.mp3', False],
        'control': ['bdush_oB7K8HPU.mp3', False]
    }
    func()
    do_note()
    custom = {}
    if 1 == 1:
        down = True
        cont = False
        s = False
        up = True
        z = False
        dooo = False
        a = False
        f = False
        f1 = False
        dd = False
        aaa = True
        ban = True
        st = False
        for i in data:
            i.append(False)
            if int(i[0]) != 0:
                i.append(f'key0{int(i[0])}.mp3')
            else:
                i.append(f'key{10}.mp3')
        while getattr(th1, "do_run", True):
            if not ban:
                ban = True
            if keyboard.is_pressed('Shift') and f:  # pedal
                f = not f
                a = False
            if (not keyboard.is_pressed('Shift')) and not f:
                f = not f
                a = True
                ban = False
            if keyboard.is_pressed('.') and down:
                down = not down
            if (not keyboard.is_pressed('.')) and not down:  # lower
                down = not down
                for i in let:
                    if i != 'd' and i != 'k' and len(let[i]) > 1:
                        a = let[i][0]
                        do(a, a, 0.7)
                for i in data:
                    a = i[2]
                    do(a, a, 0.7)
                text = 'Completed lowering'
            if keyboard.is_pressed('\\') and up:  # upper
                up = not up
            if (not keyboard.is_pressed('\\')) and not up:
                up = not up
                for i in let:
                    if i != 'd' and i != 'k' and len(let[i]) > 1:
                        a = let[i][0]
                        do(a, a, 1.3)
                for i in data:
                    a = i[2]
                    do(a, a, 1.3)
                text = 'Completed rising'

            if keyboard.is_pressed('Space') and f1:  # swap
                f1 = not f1

            if (not keyboard.is_pressed('Tab')) and not z:  # repeating
                z = not z
            if keyboard.is_pressed('Tab') and z:
                z = not z
                s = not s
            if (not keyboard.is_pressed('Capslock')) and not dooo:  # countinue
                dooo = not dooo
            if keyboard.is_pressed('Capslock') and dooo:
                dooo = not dooo
                a = not a
                ban = False

            if (not keyboard.is_pressed(',')) and not cont:  # reset
                cont = not cont
            if keyboard.is_pressed(',') and z:
                cont = not cont
                func()
                do_note()

            if (not keyboard.is_pressed('Space')) and not f1:
                f1 = not f1
                if custom == {}:
                    let2, let = let, let2
                else:
                    let, let2, custom = let2, custom, let

            for i in data:
                if ban:
                    if keyboard.is_pressed(str(i[0])) and not i[1]:
                        pygame.mixer.Channel(int(i[0])).play(pygame.mixer.Sound(i[2]))
                        i[1] = True
                    if keyboard.is_pressed(str(i[0])) and not pygame.mixer.Channel(int(i[0])).get_busy() and s:
                        pygame.mixer.Channel(int(i[0])).stop()
                        pygame.mixer.Channel(int(i[0])).play(pygame.mixer.Sound(i[2]))
                    if (not keyboard.is_pressed(str(i[0]))) and i[1]:
                        if a:
                            pygame.mixer.Channel(int(i[0])).stop()
                        i[1] = False
                else:
                    if not keyboard.is_pressed(str(i[0])):
                        pygame.mixer.Channel(int(i[0])).stop()
            count = 11
            for i in let:
                if len(let[i]) > 1:
                    if ban:
                        if keyboard.is_pressed(i) and not let[i][1]:
                            pygame.mixer.Channel(count).play(pygame.mixer.Sound(let[i][0]))
                            let[i][1] = True
                        if keyboard.is_pressed(i) and not pygame.mixer.Channel(count).get_busy() and s:
                            pygame.mixer.Channel(count).stop()
                            pygame.mixer.Channel(count).play(pygame.mixer.Sound(let[i][0]))
                        if (not keyboard.is_pressed(i)) and let[i][1]:
                            if a:
                                pygame.mixer.Channel(count).stop()
                            let[i][1] = False
                    else:
                        if not keyboard.is_pressed(i):
                            pygame.mixer.Channel(count).stop()
                count += 1


th1 = Thread(target=play_base_setups)


class Ui_Help(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setObjectName("self")
        self.resize(400, 300)
        self.textEdit = QtWidgets.QTextEdit(self)
        self.textEdit.setGeometry(QtCore.QRect(0, 0, 401, 301))
        self.textEdit.setObjectName("textEdit")

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "Help"))
        self.textEdit.setHtml(_translate("self",
                                         "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                         "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                         "p, li { white-space: pre-wrap; }\n"
                                         "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Speed up: \\</p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Slow down: .</p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Reset: ,</p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Swap sets: space</p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Pedal: shift</p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Constant pedal: Caps lock</p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Continue after end: Tab</p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">You cant change default presets</p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">To change the sound you should press the the letter on the self</p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">You can create new sets, record your own voice and choose custom songs</p>\n"
                                         "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))


class Ui_about(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setObjectName("self")
        self.resize(400, 59)
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(20, 20, 250, 16))
        self.label.setObjectName("label")

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "About"))
        self.label.setText(_translate("self", "Music keyboard made by moti4k"))


class Ui_self(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setObjectName("self")
        self.resize(400, 300)
        self.textEdit = QtWidgets.QTextEdit(self)
        self.textEdit.setGeometry(QtCore.QRect(10, 10, 371, 171))
        self.textEdit.setObjectName("textEdit")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(20, 190, 121, 16))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(290, 190, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(20, 220, 341, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(150, 250, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.pushButton_2.clicked.connect(self.make_new_dir)
        self.pushButton.clicked.connect(self.show_exist)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "Load"))
        self.label.setText(_translate("self", "These setups exist"))
        self.pushButton.setText(_translate("self", "Refresh"))
        self.pushButton_2.setText(_translate("self", "Load"))

    def make_new_dir(self):
        global new_dir, custom, directories, note, song
        new_dir = self.lineEdit.text()
        if new_dir != 'default':
            if new_dir not in directories:
                directories.append(new_dir)
                print(directories)
                file = open("music.csv", mode='a', newline='')
                writer = csv.writer(file, delimiter=',')
                for i in all_simb:
                    writer.writerow([new_dir, i, 'no'])
                custom = {
                    'num': [2],
                    'q': [False],
                    'w': [False],
                    'e': [False],
                    'r': [False],
                    't': [False],
                    'y': [False],
                    'u': [False],
                    'i': [False],
                    'o': [False],
                    'p': [False],
                    'a': [False],
                    's': [False],
                    'd': [False],
                    'f': [False],
                    'g': [False],
                    'h': [False],
                    'j': [False],
                    'k': [False],
                    'l': [False],
                    'z': [False],
                    'x': [False],
                    'c': [False],
                    'v': [False],
                    'b': [False],
                    'n': [False],
                    'm': [False],
                    'escape': [False],
                    'control': [False]
                }
            else:
                file = open("music.csv", mode='r')
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == new_dir:
                        if row[2] == 'no':
                            custom[row[1]] = [False]
                        else:
                            custom[row[1]] = [row[2], False]
                print(custom)
        else:
            custom = {}

    def show_exist(self):
        self.textEdit.setText('')
        for i in directories:
            self.textEdit.append(i)


class Ui_Form(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setObjectName("self")
        self.resize(322, 230)
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(170, 120, 121, 91))
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(20, 20, 281, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(140, 100, 47, 14))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(110, 0, 111, 20))
        self.label_2.setObjectName("label_2")
        self.pushButton_3 = QtWidgets.QPushButton(self)
        self.pushButton_3.setGeometry(QtCore.QRect(110, 50, 75, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(self)
        self.lineEdit_2.setGeometry(QtCore.QRect(10, 150, 141, 20))
        self.lineEdit_2.setText("")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(50, 130, 71, 16))
        self.label_3.setObjectName("label_3")

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.pushButton.clicked.connect(self.start)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "Change_button"))
        self.pushButton.setText(_translate("self", "Record"))
        self.label.setText(_translate("self", "Or"))
        self.label_2.setText(_translate("self", "Ender file path"))
        self.pushButton_3.setText(_translate("self", "Choose"))
        self.label_3.setText(_translate("self", "Audio length"))

    def start(self):
        global new_dir
        global note, custom
        filename = f"{new_dir}{note}.mp3"
        # установить размер блока в 1024 сэмпла
        chunk = 1024
        # образец формата
        FORMAT = pyaudio.paInt16
        # моно, если хотите стере измените на 2
        channels = 1
        # 44100 сэмплов в секунду
        sample_rate = 44100
        record_seconds = int(self.lineEdit_2.text())
        # initialize PyAudio object
        p = pyaudio.PyAudio()
        # открыть объект потока как ввод и вывод
        stream = p.open(format=FORMAT,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        output=True,
                        frames_per_buffer=chunk)
        frames = []
        print("Recording...")
        for i in range(int(44100 / chunk * record_seconds)):
            data = stream.read(chunk)
            # если вы хотите слышать свой голос во время записи
            # stream.write(data)
            frames.append(data)
        print("Finished recording.")
        # остановить и закрыть поток
        stream.stop_stream()
        stream.close()
        # завершить работу объекта pyaudio
        p.terminate()
        # сохранить аудиофайл
        # открываем файл в режиме 'запись байтов'
        wf = wave.open(filename, "wb")
        # установить каналы
        wf.setnchannels(channels)
        # установить формат образца
        wf.setsampwidth(p.get_sample_size(FORMAT))
        # установить частоту дискретизации
        wf.setframerate(sample_rate)
        # записываем кадры как байты
        wf.writeframes(b"".join(frames))
        # закрыть файл
        wf.close()
        tex = filename
        if new_dir != 'default':
            if os.path.isfile(tex):
                if not os.path.isdir("Custom"):
                    os.mkdir("Custom")
                os.replace(tex, f"Custom/{tex}")
                folder_from = os.getcwd() + r'custom'
                folder_to = os.getcwd()

                for f in os.listdir(folder_from):
                    if os.path.isfile(os.path.join(folder_from, f)):
                        shutil.copy(os.path.join(folder_from, f), os.path.join(folder_to, f))
                    if os.path.isdir(os.path.join(folder_from, f)):
                        os.system(f'rd /S /Q {folder_to}\\{f}')
                        shutil.copytree(os.path.join(folder_from, f), os.path.join(folder_to, f))
                f2 = open('music2.csv', mode='w', newline='')
                f = open('music.csv')
                writer = csv.writer(f2)
                reader = csv.reader(f)
                for row in reader:
                    if row[0] == new_dir:
                        if row[1] == note:
                            writer.writerow([row[0], row[1], tex])
                        else:
                            writer.writerow(row)
                    else:
                        writer.writerow(row)
                f.close()
                f2.close()
                f2 = open('music.csv', mode='w', newline='')
                f = open('music2.csv')
                writer = csv.writer(f2)
                reader = csv.reader(f)
                for row in reader:
                    writer.writerow(row)
                f.close()
                f2.close()
                file = open("music.csv", mode='r')
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == new_dir:
                        if row[2] == 'no':
                            custom[row[1]] = [False]
                        else:
                            custom[row[1]] = [row[2], False]
                print(custom)
            else:
                self.lineEdit.setText('No such file')
        else:
            self.lineEdit.setText("You can't change the defaults")

    def end(self):
        Ui_Form.flag = True

    def get_song(self):
        global new_dir, note, custom
        tex = self.lineEdit.text()
        if new_dir != 'default':
            if os.path.isfile(tex):
                if not os.path.isdir("Custom"):
                    os.mkdir("Custom")
                os.replace(tex, f"Custom/{tex}")
                folder_from = os.getcwd() + r'\custom'
                folder_to = os.getcwd()

                for f in os.listdir(folder_from):
                    if os.path.isfile(os.path.join(folder_from, f)):
                        shutil.copy(os.path.join(folder_from, f), os.path.join(folder_to, f))
                    if os.path.isdir(os.path.join(folder_from, f)):
                        os.system(f'rd /S /Q {folder_to}\\{f}')
                        shutil.copytree(os.path.join(folder_from, f), os.path.join(folder_to, f))
                f2 = open('music2.csv', mode='w', newline='')
                f = open('music.csv')
                writer = csv.writer(f2)
                reader = csv.reader(f)
                for row in reader:
                    if row[0] == new_dir:
                        if row[1] == note:
                            writer.writerow([row[0], row[1], tex])
                        else:
                            writer.writerow(row)
                    else:
                        writer.writerow(row)
                f.close()
                f2.close()
                f2 = open('music.csv', mode='w', newline='')
                f = open('music2.csv')
                writer = csv.writer(f2)
                reader = csv.reader(f)
                for row in reader:
                    writer.writerow(row)
                f.close()
                f2.close()
                file = open("music.csv", mode='r')
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == new_dir:
                        if row[2] == 'no':
                            custom[row[1]] = [False]
                        else:
                            custom[row[1]] = [row[2], False]
                print(custom)
            else:
                self.lineEdit.setText('No such file')
        else:
            self.lineEdit.setText("You can't change the defaults")


# Наследуемся от виджета из PyQt5.QtWidgets и от класса с интерфейсом
class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        # Вызываем метод для загрузки интерфейса из класса Ui_MainWindow,
        # остальное без изменений
        self.setupUi(self)
        oImage = QImage("back.jpg")
        sImage = oImage.scaled(QSize(1619, 991))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)
        data = self.b1.parent().children()
        click = ''
        for i in data:
            d = type(i).__name__
            if d == 'QPushButton':
                nam = i.text()
                if nam not in ['Play', 'Swap', 'Load or make new', 'Stop', 'Help', 'About']:
                    i.clicked.connect(partial(self.fff, i.text()))
                if nam == 'Load or make new':
                    i.clicked.connect(self.creat_new)
                if nam == 'Help':
                    i.clicked.connect(self.helpi)
                if nam == 'About':
                    i.clicked.connect(self.abouti)

    #
    def helpi(self):
        self.mak2 = Ui_Help()
        self.mak2.show()

    def abouti(self):
        self.make1 = Ui_about()
        self.make1.show()

    def fff(self, text):
        global note
        note = text
        self.mak = Ui_Form()
        self.mak.show()

    def creat_new(self):
        self.make = Ui_self()
        self.make.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    th1.start()
    if not app.exec_():
        print(new_dir)
        th1.do_run = False
        exit()
