import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
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
        
        self.browser = FileBrowser(self)
        self.browser.pack(side=tk.TOP, fill="x", expand=True)
        # message name entry/display
        self.msgframe = tk.Frame(self)
        self.msgframe.pack(side=tk.TOP, fill="x", expand=True)
        self.msgframe_label = tk.Label(self.msgframe, text="Messaage Name", anchor="w")
        self.msgframe_label.pack(side=tk.TOP, fill="x", expand=True)
        self.msgname_var = tk.StringVar(self.msgframe, value="messagename")
        self.msgname_entry = tk.Entry(self.msgframe, width=40)
        self.msgname_entry.pack(side=tk.LEFT)
        self.msgname_disp = tk.Label(self.msgframe, width=40, text="-", relief=tk.RIDGE)
        self.msgname_disp.pack(side=tk.LEFT)

        # number of bytes entry/display
        self.byteframe = tk.Frame(self)
        self.byteframe.pack(side=tk.TOP, fill="x", expand=True)
        self.byteframe_lbl = tk.Label(self.byteframe, width=20, text="Number of Bytes", anchor="w")
        self.byteframe_lbl.pack(side=tk.TOP, fill="x", expand=True)
        self.num_bytes_entry = tk.Entry(self.byteframe, width=40)
        self.num_bytes_entry.pack(side=tk.LEFT)
        self.num_bytes_disp = tk.Label(self.byteframe, width=40, text="-", relief=tk.RIDGE)
        self.num_bytes_disp.pack(side=tk.LEFT)

        ## endianness selector
        self.whendframe = tk.Frame(self)
        self.whendframe.pack(side=tk.TOP, fill="x", expand=True)
        self.whend_lbl = tk.Label(self.whendframe, width=20, text="Endianness", anchor="w")
        self.whend_lbl.pack(side=tk.TOP, fill="x", expand=True)
        self.whend_select = ttk.Combobox(self.whendframe, width=37, values=endian_options)
        self.whend_select.pack(side=tk.LEFT)
        self.whend_disp = tk.Label(self.whendframe, width=40, text="-", relief=tk.RIDGE)
        self.whend_disp.pack(side=tk.LEFT)

        # number of fields display
        self.num_fields_frame = tk.Frame(self)
        self.num_fields_frame.pack(side=tk.TOP, fill="x", expand=True)
        self.num_fields_var = tk.IntVar(self.num_fields_frame, value=0)
        self.num_fields_lbl = tk.Label(self.num_fields_frame, text="Number of Fields", anchor="w")
        self.num_fields_lbl.pack(side=tk.TOP, fill="x", expand=True)
        self.num_fields_disp = tk.Label(self.num_fields_frame, width=75, relief=tk.RIDGE, textvariable=self.num_fields_var)
        self.num_fields_disp.pack(side=tk.LEFT)

        ## msg update button
        update_msg = tk.Button(self, width=75, text="Update Message", command=self.update_msg)
        update_msg.pack(side=tk.TOP, anchor="w")

        # fieldframe for selecting field
        self.fieldframe = tk.Frame(self)
        self.fieldframe.pack(side=tk.TOP, expand=True, fill="x")

        ## field selector
        self.field_select_lbl = tk.Label(self.fieldframe, width=20, text="Select Field", anchor="w")
        self.field_select_lbl.pack(side=tk.TOP, expand=True, fill="x")
        # combobox options will be updated when fileds added.
        self.fieldnum = tk.StringVar(self.fieldframe)
        self.fieldnum.trace_add("write", self.update_field_disp)
        self.field_select = ttk.Combobox(self.fieldframe, width=37, textvariable=self.fieldnum)
        self.field_select.pack(side=tk.TOP, anchor="w")

        ## fieldname selection
        self.fieldname_lbl = tk.Label(self.fieldframe, width=20, text="Fieldname", anchor="w")
        self.fieldname_lbl.pack(side=tk.TOP, expand=True, fill="x")
        self.fieldname_entry = tk.Entry(self.fieldframe, width=40)
        self.fieldname_entry.pack(side=tk.LEFT)
        self.fieldname_disp = tk.Label(self.fieldframe, width=40, text="-", relief=tk.RIDGE)
        self.fieldname_disp.pack(side=tk.LEFT)

        ## bitmask entry
        self.bitmaskframe = tk.Frame(self)
        self.bitmaskframe.pack(side=tk.TOP, expand=True, fill="x")
        self.bitmask_lbl = tk.Label(self.bitmaskframe, width=20, text="Bitmask", anchor="w")
        self.bitmask_lbl.pack(side=tk.TOP, expand=True, fill="x")
        self.bitmask_entry = tk.Entry(self.bitmaskframe, width=40)
        self.bitmask_entry.pack(side=tk.LEFT)
        self.bitmask_disp = tk.Label(self.bitmaskframe, width=40, text="-", relief=tk.RIDGE)
        self.bitmask_disp.pack(side=tk.LEFT)

        ## Converter select
        self.converter_frame = tk.Frame(self)
        self.converter_frame.pack(side=tk.TOP, expand=True, fill="x")
        self.converter_lbl = tk.Label(self.converter_frame, width=20, text="Converter Select", anchor="w")
        self.converter_lbl.pack(side=tk.TOP, expand=True, fill="x")
        self.converter = ttk.Combobox(self.converter_frame, width=37, values=converter_options)
        self.converter.pack(side=tk.LEFT)
        self.converter_disp = tk.Label(self.converter_frame, width=40, text="-", relief=tk.RIDGE)
        self.converter_disp.pack(side=tk.LEFT)

        ## Output dtype select
        self.dtype_frame = tk.Frame(self)
        self.dtype_frame.pack(side=tk.TOP, expand=True, fill="x")
        self.dtype_lbl = tk.Label(self.dtype_frame, width=20, text="Dtype Out Select", anchor="w")
        self.dtype_lbl.pack(side=tk.TOP, expand=True, fill="x")
        self.dtype = ttk.Combobox(self.dtype_frame, width=37, values=dtype_options)
        self.dtype.pack(side=tk.LEFT)
        self.dtype_disp = tk.Label(self.dtype_frame, width=40, text="-", relief=tk.RIDGE)
        self.dtype_disp.pack(side=tk.LEFT)

        ## sf entry
        self.sf_frame = tk.Frame(self)
        self.sf_frame.pack(side=tk.TOP, expand=True, fill="x")
        self.sf_lbl = tk.Label(self.sf_frame, width=20, text="Scale Factor", anchor="w")
        self.sf_lbl.pack(side=tk.TOP, expand=True, fill="x")
        self.sf_entry = tk.Entry(self.sf_frame, width=40)
        self.sf_entry.pack(side=tk.LEFT)
        self.sf_disp = tk.Label(self.sf_frame, width=40, text="-", relief=tk.RIDGE)
        self.sf_disp.pack(side=tk.LEFT)

        # buttons
        self.update_field = tk.Button(self, width=75, text="Update Field", command=self.update_field)
        self.append_field = tk.Button(self, width=75, text="Append Field", command=self.append_field)
        self.remove_field = tk.Button(self, width=75, text="Remove Field", command=self.remove_field)
        self.parse_file = tk.Button(self, width=75, text="Parse File", command=self.parse_file)
        self.update_field.pack(side=tk.TOP, anchor="w")
        self.append_field.pack(side=tk.TOP, anchor="w")
        self.remove_field.pack(side=tk.TOP, anchor="w")
        self.parse_file.pack(side=tk.TOP, anchor="w")

    def process_field_input(self):
         # get inputs
        fieldname = self.fieldname_entry.get()
        converter = msg_builder.enumerate_combobox(self.converter.get(), converter_options)
        dtype = msg_builder.enumerate_combobox(self.dtype.get(), dtype_options)
        bitmask_str = self.bitmask_entry.get()
        sf_str = self.sf_entry.get()
        bitmask = msg_builder.bitmask_tuple_from_str(bitmask_str) # build bitmask from string

        try:
            # validate inputs
            assert len(fieldname) <= anymsg.MAX_FIELDNAME_LEN
            if (dtype == 1): # 1 is float
                assert sf_str.replace(".", "").isdigit() == 1 # check if all numberic after point removal
                sf = float(sf_str)
            else:
                assert sf_str.isdigit() == 1
                sf = int(sf_str)

            assert len(bitmask) == self.msg.get_msg_contents()[1] # bitmask len must be same len as num bytes

            return (fieldname,
                    dtype,
                    converter,
                    bitmask,
                    sf)

        except AssertionError:
            print("Invalid Field Input")
            return None


    def append_field(self):
        # get inputs
        contents = self.process_field_input()
        if contents is not None:
            fieldname = contents[0]
            dtype = contents[1]
            converter = contents[2]
            bitmask = contents[3]
            sf = contents[4]
            # append field
            self.msg.append_field_cfg(fieldname, dtype, converter, bitmask, sf)
            # update options in option combobox
            self.update_field_options()
            # update number of fields
            self.num_fields_var.set(self.msg.get_msg_contents()[2])

    def remove_field(self):
        idx_str = self.field_select.get()
        idx = int(idx_str)
        self.msg.rm_field_by_idx(idx)
        self.update_field_options()
        self.num_fields_var.set(self.msg.get_msg_contents()[2])

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

    def update_field(self):
        # get inputs
        contents = self.process_field_input()
        idxstr = self.fieldnum.get()
        # check validity of index and contents
        if (len(idxstr) != 0) and (contents is not None):
            idx = int(idxstr)
            # get inputs
            contents = self.process_field_input()
            self.msg.update_fieldcfg_by_idx(idx, contents[0], contents[1], contents[2], contents[3], contents[4])
            self.update_field_disp() # update displayed fields.

    def update_field_options(self):
        # updates options based on number of fields
        # in msgcfg
        num_fields = self.msg.get_num_fields()
        self.field_select["values"] = tuple([idx for idx in range(0, num_fields)])

    def update_field_disp(self, *args):
        # get field contents for selected field.
        idxstr = self.fieldnum.get()
        if (len(idxstr) != 0):
            idx = int(idxstr)
            contents = self.msg.get_field_contents(idx)
            fieldname = contents[0]
            converter = contents[1]
            bitmask = contents[2]
            dtype = contents[4]
            sf = contents[5]

            self.fieldname_disp.config(text=fieldname)
            self.converter_disp.config(text=msg_builder.str_from_enum_idx(converter_options, converter))
            self.bitmask_disp.config(text=bitmask)
            self.dtype_disp.config(text=msg_builder.str_from_enum_idx(dtype_options, dtype))
            self.sf_disp.config(text=str(sf))

    def parse_file(self):
        infile = self.browser.inpath_var
        outfile = self.browser.outpath_var
        parsemethod = self.browser.parsemethod_var
        
        self.msg.parse_file(infile.get(), outfile.get(), parsemethod.get())

    @staticmethod
    def enumerate_combobox(option:str, options:tuple[str]):
        # returns enumerated option value for combobox
        for idx in range(0, len(options)):
            if (option == options[idx]):
                return idx

    @staticmethod
    def str_from_enum_idx(enum:tuple[str], enum_idx:int):
        cntr = 0
        for enum_str in enum:
            if (cntr == enum_idx):
                return enum_str
            cntr+=1

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

class FileBrowser(tk.Frame):
    """used for file entry and setting read method"""
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # configure geometry
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=0)

        # define variables
        self.inpath_var = tk.StringVar(self)
        self.outpath_var = tk.StringVar(self)
        self.parsemethod_var = tk.BooleanVar(self, value=0)

        # create widgets
        self.inpath_entry = tk.Entry(self, textvariable=self.inpath_var, width=62)
        self.inpath_browse = tk.Button(self, text="Browse Input File", width=20, command=self.browse_infile)
        self.outpath_entry = tk.Entry(self, textvariable=self.outpath_var, width=62)
        self.outpath_browse_btn = tk.Button(self, text="Browse Output File", width=20, command=self.browse_outfile)
        self.parsemethod_btn = tk.Checkbutton(self, text="Parse AsciiHex", variable=self.parsemethod_var)
        # create layout
        self.inpath_entry.grid(row=0,column=0, sticky="w")
        self.inpath_browse.grid(row=0, column=1, sticky="w", padx=(5,5), pady=5)
        self.outpath_entry.grid(row=1, column=0, sticky="w")
        self.outpath_browse_btn.grid(row=1, column=1, sticky="w", padx=(5,5), pady=5)
        self.parsemethod_btn.grid(row=2, column=0, sticky="w")

    def browse_infile(self):
        # open file dialog
        filename = filedialog.askopenfilename(initialdir = "/",
                                    title = "Select a File",
                                    filetypes = (("Text files",
                                                "*.txt*"),
                                                ("all files",
                                                "*.*")))

        self.inpath_var.set(filename)

    def browse_outfile(self):
        # open file dialog
        filename = filedialog.asksaveasfilename(initialdir = "/",
                                    title = "Select a File",
                                    filetypes = (("Text files",
                                                "*.txt*"),
                                                ("all files",
                                                "*.*")))
        # set path variable
        self.outpath_var.set(filename)


class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Python Message Parser")
        self.geometry("500x650")
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=0)
        # configure rows and columns
        msg = msg_builder(self)
        msg.grid(row=1, column=0, rowspan = 2, columnspan = 1, sticky="nesw")


if __name__ == "__main__":
    main = MainWindow()
    main.mainloop()

