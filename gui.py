import tkinter as tk


class parser_widget(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Python Message Parser")
        self.geometry("1000x1000")


if __name__ == "__main__":
    main = MainWindow()
    main.mainloop()

