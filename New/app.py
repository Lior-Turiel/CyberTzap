from tkinter import *
from client import Client
from login_page import LoginPage

class App:
    def __init__(self):
        self.root = Tk()
        self.client = None

        self.width = 960
        self.height = 540

        self.root.title('CyperTzap')
        self.root.geometry(f'{str(self.width)}x{str(self.height)}')
        self.root.resizable(False, False)

        login = LoginPage(self.root, self.client)

        self.root.mainloop()


if __name__ == '__main__':
    App()
