from tkinter import *
from tkinter.messagebox import showinfo, showerror, showwarning
from tkinter import ttk
from tkinter import filedialog

class Application:
    def __init__(self) -> None:
        self.currentFileDirectory = ""

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
        self.editingMenu.add_command(label="Копировать")
        self.editingMenu.add_command(label="Вставить")
        self.editingMenu.add_separator()
        self.editingMenu.add_command(label="Параметры...")

        self.menubar.add_cascade(label="Правка", menu=self.editingMenu)
        
        self.infoMenu = Menu(self.menubar, tearoff=False)
        self.infoMenu.add_command(label="Содержание", command=self.onShowApplicationContentClick)
        self.infoMenu.add_separator()
        self.infoMenu.add_command(label="О программе...", command= self.onAboutButtonClick)

        self.menubar.add_cascade(label="Справка", menu=self.infoMenu)

        self.window.config(menu=self.menubar) 
        
        self.editText = Text(wrap=WORD)
        self.editText.grid(row=0, column=0)

    def onNewFileButtonClick(self) -> None:
        self.currentFileDirectory=""
        self.window.title("NoName.txtx")
        self.editText.delete("1.0", END)

    def onOpenFileButtonClick(self) -> None:
        directory = filedialog.askopenfilename(defaultextension="txtx")
        if (not self.isDirectoryEmpty(directory)):
            with open(directory, "r") as file:
                text = file.read()
                # здесь будет расшифровка
                self.editText.delete("1.0", END)
                self.editText.insert("1.0", END)
            self.window.title(directory)
            self.currentFileDirectory = directory
        else:
            showerror(title="Ошибка", message="Ошибка чтения файла")

    def isDirectoryEmpty(self, directory: str) -> bool:
        return len(directory.replace(' ', '')) == 0

    def onSaveFileAsButtonClick(self):
        directory = filedialog.asksaveasfilename(defaultextension="txtx")
        if(not self.isDirectoryEmpty(directory= directory)):
            with open(directory, "w") as file:
                file.write(self.editText.get(1.0, END))
            self.currentFileDirectory = directory
            self.window.title(self.currentFileDirectory)
            showinfo(title="Сохранение", message="Файл сохранен успешно")
        else:
            showerror(title="Ошибка записи", message= "Не получилось создать/перезаписать файл")
    
    def onSaveFileButtonClick(self):
        if(not self.isDirectoryEmpty(self.currentFileDirectory)):
            with open(self.currentFileDirectory, "w") as file:
                file.write(self.editText.get(1.0, END))
                showinfo(title="Сохранение", message="Файл сохранен успешно")
        else:
            self.onSaveFileAsButtonClick()

    def onAboutButtonClick(self):
        showinfo(title="О программе", message="Программа для 'прозрачного шифрования'\n(c) Petukhov A.O., Russia, 2023")
    def onShowApplicationContentClick(self):
        contentWindow = Toplevel()
        contentWindow.minsize(400, 250)
        contentWindow.title("Справка")

        info = "Приложение с графическим интерфейсом\n'Блокнот TCD'(файл приложения: TCD).\n"
        info += "Позволяет: создавать/открывать/сохранять\nзашифрованный текстовый файл, предусмотрены\nввод и сохранение личного ключа,\nвывод не модальной форма 'Справка',\nвывод модальной формы 'О программе'"
        infoLabel = ttk.Label(contentWindow, text= info)
        infoLabel.pack(anchor=CENTER, expand=1)
        
        closeButton = ttk.Button(contentWindow,text="Закрыть", command= contentWindow.destroy)
        closeButton.pack(anchor=SE)
    def showWindow(self) -> None:
        self.window.mainloop()


app = Application()
app.showWindow()