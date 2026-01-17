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
        
        # message name entry/display
        self.msgframe = tk.Frame(self)
        self.msgframe.pack(side=tk.TOP, expand=True, fill="x")
        self.msgframe_label = tk.Label(self.msgframe, text="Messaage Name")
        self.msgframe_label.pack(side=tk.TOP, fill="x")
        self.msgname_var = tk.StringVar(self.msgframe, value="messagename")
        self.msgname_entry = tk.Entry(self.msgframe)
        self.msgname_entry.pack(side=tk.LEFT)
        self.msgname_disp = tk.Label(self.msgframe, text="-")
        self.msgname_disp.pack(side=tk.RIGHT, expand=True, fill="x")

        # number of bytes entry/display
        self.byteframe = tk.Frame(self)
        self.byteframe.pack(side=tk.TOP, expand=True, fill="x")
        self.byteframe_label = tk.Label(self.byteframe, text="Number of Bytes")
        self.byteframe_label.pack(side=tk.TOP, fill="x")
        self.num_bytes_entry = tk.Entry(self.byteframe)
        self.num_bytes_entry.pack(side=tk.LEFT, expand=True, fill="x")
        self.num_bytes_disp = tk.Label(self.byteframe, text="-")
        self.num_bytes_disp.pack_propagate(False)
        self.num_bytes_disp.pack(side=tk.RIGHT, expand=True, fill="x")

        ## endianness selector
        self.whendframe = tk.Frame(self)
        self.whendframe.pack(side=tk.TOP, expand=True, fill="x")
        self.whend_lbl = tk.Label(self.whendframe, text="Endianness", justify="left")
        self.whend_lbl.pack(side=tk.TOP, fill="x")
        self.whend_select = ttk.Combobox(self.whendframe, values=endian_options)
        self.whend_select.pack(side=tk.LEFT, fill="x")
        self.whend_disp = tk.Label(self.whendframe, text="-")
        self.whend_disp.pack(side=tk.RIGHT, expand=True, fill="x")

        # number of fields display
        self.num_fields_frame = tk.Frame(self)
        self.num_fields_frame.pack(side=tk.TOP, expand=True, fill="x")
        self.num_fields_lbl = tk.Label(self.num_fields_frame, text="Number of Fields")
        self.num_fields_lbl.pack(side=tk.TOP, fill="x")
        self.num_fields_disp = tk.Label(self.num_fields_frame, text="-")
        self.num_fields_disp.pack(side=tk.TOP, expand=True, fill="x")

        ## msg update button
        update_msg = tk.Button(self, text="Update Message", command=self.update_msg)
        update_msg.pack(side=tk.TOP, pady=5, fill="x")

        # fieldframe for selecting field
        self.fieldframe = tk.Frame(self)
        self.fieldframe.pack(side=tk.TOP, expand=True, fill="x")

        ## field selector
        self.field_select_lbl = tk.Label(self.fieldframe, text="Select Field", justify="left")
        self.field_select_lbl.pack(side=tk.TOP, expand=True, fill="x")
        self.field_select = ttk.Combobox(self.fieldframe, values=fieldnum_options)
        self.field_select.pack(side=tk.TOP, expand=True, fill="x")

        ## fieldname selection
        self.fieldname = tk.Label(self.fieldframe, text="Fieldname")
        self.fieldname.pack(side=tk.TOP, expand=True, fill="x")
        self.fieldname_entry = tk.Entry(self.fieldframe)
        self.fieldname_entry.pack(side=tk.LEFT, expand=True, fill="x")
        self.fieldname_disp = tk.Label(self.fieldframe, text="-")
        self.fieldname_disp.pack(side=tk.RIGHT, expand=True, fill="x")

        ## bitmask entry
        self.bitmaskframe = tk.Frame(self)
        self.bitmaskframe.pack(side=tk.TOP, expand=True, fill="x")
        self.bitmask_lbl = tk.Label(self.bitmaskframe, text="Bitmask")
        self.bitmask_lbl.pack(side=tk.TOP)
        self.bitmask_entry = tk.Entry(self.bitmaskframe)
        self.bitmask_entry.pack(side=tk.LEFT, expand=True, fill="x")
        self.bitmask_disp = tk.Label(self.bitmaskframe, text="-")
        self.bitmask_disp.pack(side=tk.RIGHT, expand=True, fill="x")

        ## Converter select
        self.converter_frame = tk.Frame(self)
        self.converter_frame.pack(side=tk.TOP)
        self.converter_lbl = tk.Label(self.converter_frame, text="Converter Select")
        self.converter_lbl.pack(side=tk.TOP, expand=True, fill="x")
        self.converter = ttk.Combobox(self.converter_frame, values=converter_options)
        self.converter.pack(side=tk.LEFT, expand=True, fill="x")
        self.converter_disp = tk.Label(self.converter_frame, text="-")
        self.converter_disp.pack(side=tk.RIGHT, expand=True, fill="x")

        ## Output dtype select
        self.dtype_frame = tk.Frame(self)
        self.dtype_frame.pack(side=tk.TOP, expand=True, fill="x")
        self.dtype_lbl = tk.Label(self.dtype_frame, text="Dtype Out Select", justify="left")
        self.dtype_lbl.pack(side=tk.TOP, expand=True, fill="x")
        self.dtype = ttk.Combobox(self.dtype_frame, values=dtype_options)
        self.dtype.pack(side=tk.TOP, expand=True, fill="x")

        # buttons
        self.update_field = tk.Button(self, text="Update Field")
        self.append_field = tk.Button(self, text="Append Field")
        self.remove_field = tk.Button(self, text="Remove Field")
        self.update_field.pack(side=tk.TOP, expand=True, fill="x")
        self.append_field.pack(side=tk.TOP, expand=True, fill="x")
        self.remove_field.pack(side=tk.TOP, expand=True, fill="x")

        ## field update button
        #field_accept = tk.Button(fieldframe, text="Update Fieldname")
        #field_accept.pack(side=tk.TOP, pady=5)
    def update_msg(self):
        # validate inputs
        msgname_in = self.msgname_entry.get()
        num_bytes_in = self.num_bytes_entry.get()
        whend_in = msg_builder.enumerate_combox(self.whend_select.get(), endian_options)

        try:
            # validate inputs
            assert len(msgname_in) <= anymsg.MAX_FIELDNAME_LEN
            assert num_bytes_in.isdigit() == True
            num_bytes_in = int(num_bytes_in)
            assert num_bytes_in <= anymsg.MAX_BITMASK_LEN_BYTES
            whend_in = bool(whend_in)

            # change bytes in to int and call update msg
            self.msg.update_msgcfg(msgname_in, num_bytes_in, whend_in)

            # get message contents
            contents = self.msg.get_msg_contents()
            msgname_ret = str(contents[0])
            num_bytes_ret = str(contents[1])
            num_fields_ret = str(contents[2])
            whend_ret = contents[3]

            if (whend_ret == 0):
                whend_ret = "Big Endian"
            else:
                whend_ret = "Little Endian"
            
            self.msgname_disp.config(text=msgname_ret)
            self.num_bytes_disp.config(text=num_bytes_ret)
            self.whend_disp.config(text=whend_ret)

        except AssertionError:
            print("Invalid Message input")

    @staticmethod
    def enumerate_combox(option, options):
        # returns enumerated option value for combobox
        for idx in range(0, len(options)):
            if (option == options[idx]):
                return idx

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

