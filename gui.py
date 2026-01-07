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
        msgframe.grid(row=0, column=0, sticky="n")
        msglabel = tk.Label(msgframe, text="Messaage Name", justify="left")
        msglabel.pack(side=tk.TOP)

        # message name entry
        msgname_str = tk.StringVar(msgframe, value = "test")
        msgname = tk.Entry(msgframe, textvariable=msgname_str)
        msgname.pack(side=tk.TOP, fill="x")

        # accept button
        accept = tk.Button(self, text="Update")
        accept.grid(row=0, column=1, sticky="ns", padx=(5,5), rowspan=3)

        # number of bytes entry
        num_bytes_str = tk.IntVar(self, value = 0)
        byteslabel = tk.Label(msgframe, text="Number of Bytes", justify="left")
        byteslabel.pack(side=tk.TOP, fill="x")
        num_bytes = tk.Entry(msgframe, textvariable=num_bytes_str)
        num_bytes.pack(side=tk.TOP, fill="x")

        # field selector
        field_select_lbl = tk.Label(msgframe, text="Select Field", justify="left")
        field_select_lbl.pack(side=tk.TOP)
        field_select = ttk.Combobox(msgframe, values=fieldnum_options)
        field_select.pack(side=tk.TOP)

        #number of fields display
        num_fields = tk.IntVar(self, 0)
        num_fields_lbl = tk.Label(msgframe, text="Number of Fields", justify="left")
        num_fields_lbl.pack(side=tk.TOP)
        num_fields_disp = tk.Label(msgframe, textvariable=num_fields)
        num_fields_disp.pack(side=tk.TOP)
        

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
        msg.grid(row=0,column=0, sticky="nw")


if __name__ == "__main__":
    main = MainWindow()
    main.mainloop()

