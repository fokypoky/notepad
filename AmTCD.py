from tkinter import *
from tkinter.messagebox import showinfo, showerror, showwarning
from tkinter import ttk

class Application:
    def __init__(self) -> None:
        self.window = Tk()
        self.window.minsize(800, 450)
        self.window.title("NoName.txtx")
        self.menubar = Menu(self.window)
        
        self.fileMenu = Menu(self.menubar, tearoff=False)
        self.fileMenu.add_command(label="Новый")
        self.fileMenu.add_command(label="Открыть")
        self.fileMenu.add_command(label="Сохранить")
        self.fileMenu.add_command(label="Сохранить как")
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Выход")

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
        
        closeButton = ttk.Button(contentWindow,text="close", command= contentWindow.destroy)
        closeButton.pack(anchor=SE)

    def showWindow(self) -> None:
        self.window.mainloop()


app = Application()
app.showWindow()