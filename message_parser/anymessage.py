import ctypes
import faulthandler
faulthandler.enable()

# load dll
parser_dll = ctypes.cdll.LoadLibrary(r"./message_parser/lib/anyparse/anyparse.dll")

# define "macro" vars
BIG_ENDIAN = False
LITTLE_ENDIAN = True

# converters
READ_TWOS_COMP = 0
READ_OB = 1
READ_COB = 2
READ_UNS = 3
READ_IEEE_FP = 4
READ_CHAR = 5

# dtypes
DTYPE_OUT_INT =  0
DTYPE_OUT_FLOAT = 1
DTYPE_OUT_CHAR = 2
DTYPE_OUT_UINT = 3

# other defines
MAX_NUM_FIELDS = 10
MAX_FIELDNAME_LEN = 30
MAX_BITMASK_LEN_BYTES = 20
NUM_CONVERTER_OPTIONS = 6
NUM_DTYPE_OPTIONS = 4

# define basetypes using ctypes primitives.
FIELDNAME_ARRAY = ctypes.c_char * MAX_FIELDNAME_LEN
BITMASK_ARRAY = ctypes.c_ubyte * MAX_BITMASK_LEN_BYTES
bitmask_pointer = ctypes.POINTER(BITMASK_ARRAY)
MESSAGENAME_ARRAY = FIELDNAME_ARRAY

# parsed result class
class parsed_result(ctypes.Union):
    _fields_ = [("int_result", ctypes.c_int64),
                ("uint_result", ctypes.c_uint64),
                ("float_result", ctypes.c_double),
                ("char_result", 4*ctypes.c_char)]

# field config class prototype
class field_cfg(ctypes.Structure):
    # note prototype is required for linked lists.
    pass

# define pointer to class prototype
field_cfg_ptr = ctypes.POINTER(field_cfg)

# define fields
field_cfg._fields_ = [("fieldname", FIELDNAME_ARRAY),
            ("bitmask", BITMASK_ARRAY),
            ("num_bits", ctypes.c_ubyte),
            ("converter", ctypes.c_ubyte),
            ("dtype", ctypes.c_ubyte),
            ("sf", ctypes.c_double),
            ("parsed_val", parsed_result),
            ("next_field", field_cfg_ptr)]

# message config class
class message_cfg(ctypes.Structure):
    _fields_ = [("message_name", MESSAGENAME_ARRAY),
                ("num_bytes", ctypes.c_ubyte),
                ("num_fields", ctypes.c_ubyte),
                ("whend", ctypes.c_bool),
                ("first_field", field_cfg)]

message_cfg_ptr = ctypes.POINTER(message_cfg)

# specify return types for dll functions
parser_dll.init_msgcfg.restype = ctypes.c_int32
parser_dll.init_msgcfg.argtypes = [message_cfg_ptr]

parser_dll.update_msgcfg.restype = ctypes.c_int32
parser_dll.update_msgcfg.argtypes = [message_cfg_ptr, 
                                   ctypes.c_char_p, 
                                   ctypes.c_ubyte, 
                                   ctypes.c_bool]

parser_dll.append_field.restype = ctypes.c_int32
parser_dll.append_field.argtypes = [message_cfg_ptr,
                                    bitmask_pointer,
                                    ctypes.c_char_p,
                                    ctypes.c_ubyte,
                                    ctypes.c_ubyte,
                                    ctypes.c_double]

parser_dll.add_field_at_idx.restype = ctypes.c_int32
parser_dll.add_field_at_idx.argtypes = [message_cfg_ptr,
                                        ctypes.c_uint32,
                                        bitmask_pointer,
                                        ctypes.c_char_p,
                                        ctypes.c_ubyte,
                                        ctypes.c_ubyte,
                                        ctypes.c_double]

parser_dll.rm_field_by_idx.restype = ctypes.c_int32
parser_dll.rm_field_by_idx.argtypes = [message_cfg_ptr,
                                       ctypes.c_uint32]

parser_dll.rm_all_msg_fields.restype = ctypes.c_int32
parser_dll.rm_all_msg_fields.argtypes = [message_cfg_ptr]

parser_dll.open_and_parse_file.restype = ctypes.c_int32
parser_dll.open_and_parse_file.argtypes = [ctypes.c_char_p,
                                           ctypes.c_char_p,
                                           message_cfg_ptr,
                                           ctypes.c_bool]

parser_dll.update_fieldcfg_by_idx.restype = ctypes.c_int32
parser_dll.update_fieldcfg_by_idx.argtypes = [message_cfg_ptr,
                                              ctypes.c_uint32,
                                              bitmask_pointer,
                                              ctypes.c_char_p,
                                              ctypes.c_ubyte,
                                              ctypes.c_ubyte,
                                              ctypes.c_double]

parser_dll.field_cfg_by_idx.restype = field_cfg_ptr
parser_dll.field_cfg_by_idx.argtypes = [message_cfg_ptr,
                                        ctypes.c_uint32]



# define message class.
class message:
    def __init__(self):
        self.msg_cfg = message_cfg()
        self.msg_cfg_ptr = ctypes.pointer(self.msg_cfg)
        self.init_msgcfg(self.msg_cfg)
        self.num_fields = 0

    def init_msgcfg(self, msgcfg: dict):
        # initialize message config
        parser_dll.init_msgcfg(self.msg_cfg_ptr);

    def append_field_cfg(self, fieldcfg):
        # validate inputs
        assert len(fieldcfg["fieldname"]) < MAX_FIELDNAME_LEN
        assert ((fieldcfg["dtype"] >= 0) and (fieldcfg["dtype"] < NUM_DTYPE_OPTIONS))
        assert ((fieldcfg["converter"] >= 0) and (fieldcfg["converter"] < NUM_CONVERTER_OPTIONS))

        # create c compatible types.
        fieldname = ctypes.c_char_p(fieldcfg["fieldname"].encode("utf-8"))
        dtype = ctypes.c_ubyte(fieldcfg["dtype"])
        converter = ctypes.c_ubyte(fieldcfg["converter"])
        bitmask = ctypes.pointer(self.bitmask_from_tuple(fieldcfg["bitmask"]))
        sf = ctypes.c_double(fieldcfg["sf"])
        
        # call append_field function from dll.
        parser_dll.append_field(self.msg_cfg_ptr, bitmask, fieldname, converter, dtype, sf)
        # get number of fields and update python fields
        self.num_fields = self.get_num_fields()
    
    def get_msg_contents(self):
        
        fieldname = message.get_array_elements(self.msg_cfg.message_name,)
        return (fieldname,
                self.msg_cfg.num_bytes,
                self.msg_cfg.num_fields,
                self.msg_cfg.whend)

    def get_field_contents(self, idx):
        # get field by index position
        assert idx < self.num_fields
        ct_idx = ctypes.c_uint32(idx)
        field_ptr = parser_dll.field_cfg_by_idx(self.msg_cfg_ptr, ct_idx)

        # get dtype output
        if (field_ptr.contents.dtype == DTYPE_OUT_INT):
            result = field_ptr.contents.parsed_val.int_result
        elif (field_ptr.contents.dtype == DTYPE_OUT_FLOAT):
            result = field_ptr.contents.parsed_val.float_result
        elif (field_ptr.contents.dtype == DTYPE_OUT_CHAR):
            result = field_ptr.contents.parsed_val.char_result
        else:
            result = field_ptr.contents.parsed_val.uint_result
        
        # get bitmask elements
        bitmask = message.get_array_elements(field_ptr.contents.bitmask, MAX_BITMASK_LEN_BYTES)
        
        return (field_ptr.contents.fieldname,
                field_ptr.contents.converter,
                bitmask,
                field_ptr.contents.num_bits,
                field_ptr.contents.dtype,
                field_ptr.contents.sf,
                result)

    def update_msgcfg(self, msgname, num_bytes, whend):
        # note this function is different than init
        # since it does not 0 out pointer fields and num fields.
        assert len(msgname) < MAX_FIELDNAME_LEN
        assert num_bytes < MAX_BITMASK_LEN_BYTES
        assert type(whend) == bool

        # create c compatible types.
        msgname = ctypes.c_char_p(msgname.encode("utf-8"))
        num_bytes = ctypes.c_ubyte(num_bytes)
        whend = ctypes.c_bool(whend)

        parser_dll.update_msgcfg(self.msg_cfg_ptr, msgname, num_bytes, whend)

    def parse_file(self, ftoparse:str, fparsed: str, readmethod: bool):
        # opens and parsed file ftoparse and outputs parsed data
        # to file fparsed. Note parsed readmethod 0=binary, 1=hexascii.
        ftoparse_ptr = ctypes.c_char_p(ftoparse.encode("utf-8"))
        fparsed_ptr = ctypes.c_char_p(fparsed.encode("utf-8"))
        parser_dll.open_and_parse_file(ftoparse_ptr, fparsed_ptr, self.msg_cfg_ptr, readmethod)
    
    def update_cfg_by_idx(self, idx, fieldname, dtype, converter, bitmask, sf):
        # get field by index position
        assert idx < self.num_fields
        # validate inputs
        assert len(fieldcfg["fieldname"]) < MAX_FIELDNAME_LEN
        assert ((fieldcfg["dtype"] >= 0) and (fieldcfg["dtype"] < NUM_DTYPE_OPTIONS))
        assert ((fieldcfg["converter"] >= 0) and (fieldcfg["converter"] < NUM_CONVERTER_OPTIONS))

        # create c compatible types.
        fieldname = ctypes.c_char_p(fieldname)
        dtype = ctypes.c_ubyte(dtype)
        converter = ctypes.c_ubyte(converter)
        bitmask = ctypes.pointer(self.bitmask_from_tuple(bitmask))
        sf = ctypes.c_double(sf)

        parser_dll.update_cfg_by_idx(self.msg_cfg_ptr, idx, fieldname, dtype, converter, bitmask, sf)

    def get_num_fields(self):
        return self.msg_cfg.num_fields

    def __del__(self):
        # define function to free fields when class deleted
        parser_dll.rm_all_msg_fields(self.msg_cfg)

    @staticmethod
    def get_array_elements(c_array, array_size):

        return [c_array[idx] for idx in range(array_size)]

    @staticmethod
    def bitmask_from_tuple(bmask_array:tuple[int]):
        mask_eight = 0xff # ensures all numbers are max 8 bits.
        byte_idx = 0
        array = BITMASK_ARRAY()

        for byte in bmask_array:
            if (byte_idx >= MAX_BITMASK_LEN_BYTES):
                break
            array[byte_idx] = bmask_array[byte_idx] & mask_eight
            byte_idx += 1

        return array

    @staticmethod
    def bitmask_from_cfgstr(cfgstr:str):
        # format: [byte0 byte1 byten] [startbit0 startbit1 startbitn] [stopbit0 stopbit1 stopbitn]
        cfgstr = cfgstr.replace("[", "")
        cfgstr = cfgstr.replace("]", "")
        cfglist_str = cfgstr.split(" ")

        if (((len(cfglist_str) % 3) != 0) or (len(cfglist_str) == 0)):
            raise SyntaxError("Incorrectly formated config string")

        cfglist = [int(val) for val in cfglist_str]
        num_cfgs = int(len(cfglist)/3)
        bitmask = [0 for field in range(0, MAX_BITMASK_LEN_BYTES)]
        
        for idx in range(0, num_cfgs):
            byte = cfglist[idx]
            startbit = cfglist[num_cfgs+idx]
            stopbit = cfglist[2*num_cfgs+idx]
            bitmask[byte] = message.create_bitmask(startbit, stopbit)

        return tuple(bitmask)

    @staticmethod
    def create_bitmask(startbit: int, stopbit: int)->int:
        assert (startbit <= 7) and (stopbit <= 7)

        if (startbit == 0):
            return ((0x01 << (stopbit + 1)) - 1)
        else:
            return ((0x01 << (stopbit + 1)) - 1) - ((0x01 << startbit) - 1)

if __name__ == "__main__":

    field3 = {"fieldname": "testfield3", # need to fix char parser.
            "dtype": DTYPE_OUT_FLOAT,
            "converter": READ_IEEE_FP,
            "bitmask": (255,255,255,255),
            "sf": 1}

    msgcfg = {"message_name": "message1",
              "num_bytes": 4,
              "whend": BIG_ENDIAN}

    msg = message()
    msg.init_msgcfg(msgcfg)
    msg.append_field_cfg(field3)
    print(msg.get_num_fields())
    print(msg.get_field_contents(0))
    #msg.parse_file("testfile.txt", "outfile.txt", 1)
    del(msg)

    #parser.bitmask_from_tuple(field1["bitmask"])