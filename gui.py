import tkinter as tk
from tkinter import ttk
from message_parser import anymessage as anymsg

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
        # combobox options will be updated when fileds added.
        self.field_select = ttk.Combobox(self.fieldframe)
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
        self.dtype.pack(side=tk.LEFT, expand=True, fill="x")
        self.dtype_disp = tk.Label(self.dtype_frame, text="-")
        self.dtype_disp.pack(side=tk.RIGHT)

        ## sf entry
        self.sf_frame = tk.Frame(self)
        self.sf_frame.pack(side=tk.TOP, expand=True, fill="x")
        self.sf_lbl = tk.Label(self.sf_frame, text="Scale Factor")
        self.sf_lbl.pack(side=tk.TOP)
        self.sf_entry = tk.Entry(self.sf_frame)
        self.sf_entry.pack(side=tk.LEFT, expand=True, fill="x")
        self.sf_disp = tk.Label(self.sf_frame, text="-")
        self.sf_disp.pack(side=tk.RIGHT, expand=True, fill="x")

        # buttons
        self.update_field = tk.Button(self, text="Update Field")
        self.append_field = tk.Button(self, text="Append Field", command=self.append_field)
        self.remove_field = tk.Button(self, text="Remove Field")
        self.update_field.pack(side=tk.TOP, expand=True, fill="x")
        self.append_field.pack(side=tk.TOP, expand=True, fill="x")
        self.remove_field.pack(side=tk.TOP, expand=True, fill="x")

    def append_field(self):
        # get inputs
        fieldname = self.fieldname_entry.get()
        converter = msg_builder.enumerate_combobox(self.converter.get(), converter_options)
        dtype = msg_builder.enumerate_combobox(self.dtype.get(), dtype_options)
        bitmask_str = self.bitmask_entry.get()
        sf_str = self.sf_entry.get()

        try:
            # validate inputs
            assert len(fieldname) <= anymsg.MAX_FIELDNAME_LEN
            if (dtype == 1): # 1 is float
                assert sf_str.replace(".", "").isdigit() == 1 # check if all numberic after point removal
                sf = float(sf_str)
            else:
                assert sf_str.isdigit() == 1
                sf = int(sf_str)

            bitmask = msg_builder.bitmask_tuple_from_str(bitmask_str) # build bitmask from string
            assert len(bitmask) == self.msg.get_msg_contents()[1] # bitmask len must be same len as num bytes

            # append field
            self.msg.append_field_cfg(fieldname, dtype, converter, bitmask, sf)
            self.update_field_options()

        except AssertionError:
            print("Invalid Field Input")

    def remove_field(self):
        idx_str = self.field_select.get()
        idx = int(idx_str)
        self.msg.rm_field_by_idx(idx)
        self.update_field_options()

    def update_msg(self):
        msgname_in = self.msgname_entry.get()
        num_bytes_in = self.num_bytes_entry.get()
        whend_in = msg_builder.enumerate_combobox(self.whend_select.get(), endian_options)

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
    
    def update_field_options(self):
        # updates options based on number of fields
        # in msgcfg
        num_fields = self.msg.get_num_fields()
        self.field_select["values"] = tuple([idx for idx in range(0, num_fields)])

    @staticmethod
    def enumerate_combobox(option:str, options:tuple[str]):
        # returns enumerated option value for combobox
        for idx in range(0, len(options)):
            if (option == options[idx]):
                return idx

    @staticmethod
    def bitmask_tuple_from_str(mask_str: str):
        mask_bytes = mask_str.split(",")
        bytes_out = []

        for byte in mask_bytes:
            if ("0x" in byte):
                byte = int(byte, base=16)
            else:
                byte = int(byte)
            bytes_out.append(byte)

        return tuple(bytes_out)

class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Python Message Parser")
        self.geometry("500x600")
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

