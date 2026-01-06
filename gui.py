import tkinter as tk
from tkinter import ttk
import message_parser.anymessage as anymsg

# defines options for combobox in message builder.
fieldnum_options = tuple([str(num) for num in range(0,anymsg.MAX_NUM_FIELDS)])

class msg_builder(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        
        msgframe = tk.Frame(self)
        msgframe.grid(row=0, column=0, sticky="nw")

        msglabel = tk.Label(msgframe, text="Messaage Name")
        msglabel.pack(side=tk.TOP)

        msgname_str = tk.StringVar(msgframe, value = "test")
        msgname = tk.Entry(msgframe, textvariable=msgname_str)
        msgname.pack(side=tk.TOP)

        accept = tk.Button(self, text="Update")
        accept.grid(row=1, column=1)

        byteslabel = tk.Label(self, text="Number of Bytes")
        byteslabel.grid(row=2, column=0, sticky="nw")
        num_bytes_str = tk.StringVar(self, value = "test")
        num_bytes = tk.Entry(self, textvariable=num_bytes_str)
        num_bytes.grid(row= 2, column=0)

        field_select = ttk.Combobox(self, values=fieldnum_options)
        field_select.grid(row=2, column=0)
        

class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Python Message Parser")
        self.geometry("500x500")
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        # configure rows and columns
        msg = msg_builder(self)
        msg.grid(row=0,column=0)


if __name__ == "__main__":
    main = MainWindow()
    main.mainloop()

