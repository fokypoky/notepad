from tkinter import *
from tkinter.messagebox import showinfo, showerror
from tkinter import ttk
from tkinter import filedialog
from tkinter.simpledialog import askinteger
import configparser
import os.path
class Encryptor():
    def encrypt(self, message: str, key: int) -> str:
        encrypted = ""
        if (key > 32):
            key = key % 32
        for c in message:
            unicode_number = ord(c)
            if (unicode_number + key > 1114111):
                encrypted += chr(unicode_number + key - 1114111)
                continue
            encrypted += chr(unicode_number + key)
        return encrypted

    def decrypt(self, message: str, key: int) -> str:
        decrypted = ""
        if (key > 32):
            key = key % 32
        for c in message:
            unicode_number = ord(c)
            if (unicode_number - key < 0):
                decrypted += chr(1114111 - (key - unicode_number))
                continue
            decrypted += chr(unicode_number - key)
        return decrypted

class Application():
    def __init__(self) -> None:
        self.currentFileDirectory = ""
        self.personalKey = None

        if (os.path.exists("AmTCD.ini")):
            config = configparser.ConfigParser()
            config.read('AmTCD.ini')
            self.personalKey = int(config['main']['key'])

        self.window = Tk()
        self.window.minsize(800, 450)
        self.window.title("NoName.txtx")
        self.window.resizable(False, False)
        self.menubar = Menu(self.window)

        self.fileMenu = Menu(self.menubar, tearoff=False)
        self.fileMenu.add_command(label="Новый", command=self.onNewFileButtonClick)
        self.fileMenu.add_command(label="Открыть", command=self.onOpenFileButtonClick)
        self.fileMenu.add_command(label="Сохранить", command=self.onSaveFileButtonClick)
        self.fileMenu.add_command(label="Сохранить как", command=self.onSaveFileAsButtonClick)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Выход", command=self.window.destroy)

        self.menubar.add_cascade(label="Файл", menu=self.fileMenu)

        self.editingMenu = Menu(self.menubar, tearoff=False)
        self.editingMenu.add_command(label="Копировать", command=self.onCopyTextButtonClick)
        self.editingMenu.add_command(label="Вставить", command=self.onInsertTextButtonClick)
        self.editingMenu.add_separator()
        self.editingMenu.add_command(label="Параметры...", command=self.onParametersButtonClick)

        self.menubar.add_cascade(label="Правка", menu=self.editingMenu)

        self.infoMenu = Menu(self.menubar, tearoff=False)
        self.infoMenu.add_command(label="Содержание", command=self.onShowApplicationContentClick)
        self.infoMenu.add_separator()
        self.infoMenu.add_command(label="О программе...", command=self.onAboutButtonClick)

        self.menubar.add_cascade(label="Справка", menu=self.infoMenu)

        self.window.config(menu=self.menubar)

        self.editText = Text(wrap=WORD)

        self.scroll = Scrollbar(command=self.editText.yview())
        self.scroll.pack(side=RIGHT, fill=Y)

        self.editText.pack(fill="both", expand=True)
        self.editText.configure(yscrollcommand=self.scroll.set)

    def onNewFileButtonClick(self) -> None:
        self.currentFileDirectory = ""
        self.window.title("NoName.txtx")
        self.editText.delete("1.0", END)

    def onOpenFileButtonClick(self) -> None:
        directory = filedialog.askopenfilename(defaultextension="txtx")
        if (not self.isDirectoryEmpty(directory)):
            key = askinteger(title="Ключ", prompt="Введите ключ для расшифровки", minvalue=1, maxvalue=999)
            self.editText.delete("1.0", END)
            self.editText.insert("1.0", Encryptor().decrypt(message=self.readFile(directory), key=key))
            self.window.title(directory)
            self.currentFileDirectory = directory
        else:
            showerror(title="Ошибка", message="Неверно указан путь")

    def readFile(self, directory: str) -> str:
        with open(directory, "r") as file:
            return file.read()

    def isDirectoryEmpty(self, directory: str) -> bool:
        return len(directory.replace(' ', '')) == 0

    def onSaveFileAsButtonClick(self) -> None:
        self.currentFileDirectory = filedialog.asksaveasfilename(defaultextension="txtx")
        if (not self.isDirectoryEmpty(self.currentFileDirectory)):
            self.saveFile()
            self.window.title(self.currentFileDirectory)
            showinfo(title="Сохранение", message="Файл успешно сохранен")
        else:
            showerror(title="Ошибка", message="Неверно указан путь")

    def onSaveFileButtonClick(self) -> None:
        self.saveFile() if not self.isDirectoryEmpty(self.currentFileDirectory) else self.onSaveFileAsButtonClick()

    def saveFile(self) -> None:
        if (self.personalKey is None):
            self.personalKey = askinteger(title="Ключ", prompt="Ваш ключ не установлен. Введите его", minvalue=1, maxvalue=999)
        with open(self.currentFileDirectory, "w") as file:
            file.write(str(Encryptor().encrypt(message=self.editText.get(1.0, END), key=self.personalKey)))

    def onCopyTextButtonClick(self) -> None:
        self.window.clipboard_clear()
        self.window.clipboard_append(self.editText.selection_get())

    def onInsertTextButtonClick(self) -> None:
        self.editText.insert(INSERT, self.window.clipboard_get()) if isinstance(self.window.clipboard_get(), str) else showerror(title='Ошибка', message='Вставить можно только текс')

    def onAboutButtonClick(self) -> None:
        showinfo(title="О программе", message="Программа для 'прозрачного шифрования'\n(c) Petukhov A.O., Russia, 2023")

    def onShowApplicationContentClick(self) -> None:
        contentWindow = Toplevel()
        contentWindow.resizable(False, False)
        contentWindow.minsize(350, 250)
        contentWindow.title("Справка")

        info = "Приложение с графическим интерфейсом\n'Блокнот TCD'(файл приложения: TCD).\n"
        info += "Позволяет: создавать/открывать/сохранять\nзашифрованный текстовый файл, предусмотрены\nввод и сохранение личного ключа,\nвывод не модальной форма 'Справка',\nвывод модальной формы 'О программе'"
        infoLabel = ttk.Label(contentWindow, text=info).pack(anchor=CENTER, expand=1)

        closeButton = ttk.Button(contentWindow, text="Закрыть", command=contentWindow.destroy).pack(anchor=SE, pady=10, padx=10)

    def onParametersButtonClick(self) -> None:
        self.savePreferences(askinteger(title="Ключ", prompt="Введите Ваш ключ", minvalue=1, maxvalue=999))
        showinfo(title='Ключ', message='Ключ сохранен')

    def savePreferences(self, key: int) -> None:
        config = configparser.ConfigParser()
        config['main'] = {'key': str(key)}
        with open("AmTCD.ini", 'w') as file:
            config.write(file)

    def showWindow(self) -> None:
        self.window.mainloop()

app = Application()
app.showWindow()