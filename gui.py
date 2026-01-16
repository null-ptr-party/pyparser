import tkinter as tk
from tkinter import ttk
from message_parser import anymessage as anymsg

# defines options for combobox in message builder.
fieldnum_options = tuple([str(num) for num in range(0,anymsg.MAX_NUM_FIELDS)])
# defines options for converters combobox
converter_options = ("Twos Complement", "Offset Binary", "Complementary Offset Binary",
                          "Unsigned", "iee fp", "char")

dtype_options = ("int", "float", "char", "uint")

endian_options = ("Big Endian", "Little Endian")

class msg_builder(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.msg = anymsg.message()
        self.messagename, self.num_bytes, self.num_fields, self.whend = self.msg.get_msg_contents()
        
        # message name entry/display
        msgframe = tk.Frame(self)
        msgframe.pack(side=tk.TOP, fill="x")
        msgframe_label = tk.Label(msgframe, text="Messaage Name")
        msgframe_label.pack(side=tk.TOP, fill="x")
        msgname_var = tk.StringVar(msgframe, value="messagename")
        msgname_entry = tk.Entry(msgframe)
        msgname_entry.pack(side=tk.LEFT)
        msgname_disp = tk.Label(msgframe, textvariable=msgname_var)
        msgname_disp.pack(side=tk.RIGHT)

        # number of bytes entry/display
        byteframe = tk.Frame(self)
        byteframe.pack(side=tk.TOP, fill="x")
        num_bytes_var = tk.IntVar(self, value = 0)
        byteframe_label = tk.Label(byteframe, text="Number of Bytes")
        byteframe_label.pack(side=tk.TOP, fill="x")
        num_bytes = tk.Entry(byteframe)
        num_bytes.pack(side=tk.LEFT)
        num_bytes_disp = tk.Label(byteframe, textvariable=num_bytes_var)
        num_bytes_disp.pack(side=tk.RIGHT)


        ## endianness selector
        whendframe = tk.Frame(self)
        whendframe.pack(side=tk.TOP, fill="x")
        whend_lbl = tk.Label(whendframe, text="Endianness", justify="left")
        whend_lbl.pack(side=tk.TOP)
        whend_select = ttk.Combobox(whendframe, values=endian_options)
        whend_select.pack(side=tk.LEFT)
        whend_var = tk.IntVar(whendframe, value = 0)
        whend_disp = tk.Label(whendframe, textvariable=whend_var)
        whend_disp.pack(side=tk.RIGHT)
        
        ## msg update button
        update_msg = tk.Button(self, text="Update Message")
        update_msg.pack(side=tk.TOP, pady=5, fill="x")

        fieldframe = tk.Frame(self)
        ## field selector
        #field_select_lbl = tk.Label(fieldframe, text="Select Field", justify="left")
        #field_select_lbl.pack(side=tk.TOP)
        #field_select = ttk.Combobox(fieldframe, values=fieldnum_options)
        #field_select.pack(side=tk.TOP)

        ## fieldname entry
        #fieldname = tk.Label(fieldframe, text="Fieldname", justify="left")
        #fieldname.pack(side=tk.TOP)
        #fieldname_entry = tk.Entry(fieldframe)
        #fieldname_entry.pack(side=tk.TOP, fill="x")

        ## bitmask entry
        #bitmask = tk.Label(fieldframe, text="Bitmask", justify="left")
        #bitmask.pack(side=tk.TOP)
        #bitmask_entry = tk.Entry(fieldframe)
        #bitmask_entry.pack(side=tk.TOP, fill="x")

        ## Converter select
        #converter_lbl = tk.Label(fieldframe, text="Converter Select", justify="left")
        #converter_lbl.pack(side=tk.TOP)
        #converter = ttk.Combobox(fieldframe, values=converter_options)
        #converter.pack(side=tk.TOP)

        ## Output dtype select
        #dtype_lbl = tk.Label(fieldframe, text="Dtype Out Select", justify="left")
        #dtype_lbl.pack(side=tk.TOP)
        #dtype = ttk.Combobox(fieldframe, values=dtype_options)
        #dtype.pack(side=tk.TOP)

        ## field update button
        #field_accept = tk.Button(fieldframe, text="Update Fieldname")
        #field_accept.pack(side=tk.TOP, pady=5)
        
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

