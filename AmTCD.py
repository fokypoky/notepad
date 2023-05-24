from tkinter import *
from tkinter.messagebox import showinfo, showerror, showwarning
from tkinter import ttk
from tkinter import filedialog
from tkinter.simpledialog import askinteger 

class Encryptor:
    def encrypt(self, message: str, key:int) -> str:
        encrypted = ""
        if(key > 32):
            key = key % 32
        for c in message:
            unicode_number = ord(c)
            encrypted += chr(unicode_number + key)
        return encrypted
    def decrypt(self, message: str, key: int) -> str:
        decrypted = ""
        if(key > 32):
            key = key % 32
        for c in message:
            unicode_number = ord(c)
            decrypted += chr(unicode_number - key)
        return decrypted
class Application:
    def __init__(self) -> None:
        self.currentFileDirectory = ""
        self.personalKey = None

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
        self.editingMenu.add_command(label="Копировать", command = self.onCopyTextButtonClick)
        self.editingMenu.add_command(label="Вставить", command=self.onInsertTextButtonClick)
        self.editingMenu.add_separator()
        self.editingMenu.add_command(label="Параметры...", command=self.onParametersButtonClick)

        self.menubar.add_cascade(label="Правка", menu=self.editingMenu)
        
        self.infoMenu = Menu(self.menubar, tearoff=False)
        self.infoMenu.add_command(label="Содержание", command=self.onShowApplicationContentClick)
        self.infoMenu.add_separator()
        self.infoMenu.add_command(label="О программе...", command= self.onAboutButtonClick)

        self.menubar.add_cascade(label="Справка", menu=self.infoMenu)

        self.window.config(menu=self.menubar) 
        
        self.editText = Text(wrap=WORD)

        self.scroll = Scrollbar(command=self.editText.yview())
        self.scroll.pack(side=RIGHT, fill=Y)

        self.editText.pack(fill="both", expand=True)
        self.editText.configure(yscrollcommand=self.scroll.set)

    def onNewFileButtonClick(self) -> None:
        self.currentFileDirectory=""
        self.window.title("NoName.txtx")
        self.editText.delete("1.0", END)

    def onOpenFileButtonClick(self) -> None:
        directory = filedialog.askopenfilename(defaultextension="txtx")
        if(not self.isDirectoryEmpty(directory)):
            text = self.readFile(directory)
            self.editText.delete("1.0", END)
            self.editText.insert("1.0", END)
            self.window.title(directory)
            self.currentFileDirectory = directory
        else:
            showerror(title="Ошибка", message="Неверно указан путь")


    def readFile(self, directory: str) -> str:
        text = ""
        with open(directory, "r") as file:
            text = file.read()
        return text


    def isDirectoryEmpty(self, directory: str) -> bool:
        return len(directory.replace(' ', '')) == 0

    def onSaveFileAsButtonClick(self) -> None:
        self.currentFileDirectory = filedialog.asksaveasfilename(defaultextension="txtx")
        if(not self.isDirectoryEmpty(self.currentFileDirectory)):
            self.saveFile()
            self.window.title(self.currentFileDirectory)
            showinfo(title="Сохранение", message="Файл успешно сохранен")
        else:
            showerror(title="Ошибка", message="Неверно указан путь")
    
    def onSaveFileButtonClick(self) -> None:
        print(self.isDirectoryEmpty(self.currentFileDirectory))
        if(not self.isDirectoryEmpty(self.currentFileDirectory)):
            self.saveFile()
        else:
            self.onSaveFileAsButtonClick()

    def saveFile(self) -> None:
        with open(self.currentFileDirectory, "w") as file:
            file.write(self.editText.get(1.0, END))
        

    def onCopyTextButtonClick(self) -> None:
        self.window.clipboard_clear()
        self.window.clipboard_append(self.editText.selection_get())

    def onInsertTextButtonClick(self) -> None:
        clipboardValue = self.window.clipboard_get()
        if isinstance(clipboardValue, str):
            self.editText.insert(INSERT, clipboardValue)
        else:
            showerror(title="Ошибка", message="Вставить можно только текст")

    def onAboutButtonClick(self) -> None:
        showinfo(title="О программе", message="Программа для 'прозрачного шифрования'\n(c) Petukhov A.O., Russia, 2023")
    
    def onShowApplicationContentClick(self) -> None:
        contentWindow = Toplevel()
        contentWindow.resizable(False, False)
        contentWindow.minsize(350, 250)
        contentWindow.title("Справка")

        info = "Приложение с графическим интерфейсом\n'Блокнот TCD'(файл приложения: TCD).\n"
        info += "Позволяет: создавать/открывать/сохранять\nзашифрованный текстовый файл, предусмотрены\nввод и сохранение личного ключа,\nвывод не модальной форма 'Справка',\nвывод модальной формы 'О программе'"
        infoLabel = ttk.Label(contentWindow, text= info)
        infoLabel.pack(anchor=CENTER, expand=1)
        
        closeButton = ttk.Button(contentWindow,text="Закрыть", command= contentWindow.destroy)
        closeButton.pack(anchor=SE)
    def onParametersButtonClick(self) -> None:
        self.personalKey = askinteger(title="Ключ", prompt="Введите Ваш ключ:", minvalue=1)

    def showWindow(self) -> None:
        self.window.mainloop()


app = Application()
app.showWindow()