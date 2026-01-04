import ctypes
import faulthandler
faulthandler.enable()

# load dll
parser_dll = ctypes.cdll.LoadLibrary(r"./bin/bitstripper.dll")

# define "macro" vars
BIG_ENDIAN = False
LITTLE_ENDIAN = True

READ_TWOS_COMP = 0
READ_OB = 1
READ_COB = 2
READ_UNS = 3
READ_IEEE_FP = 4
READ_CHAR = 5

DTYPE_OUT_INT =  0
DTYPE_OUT_FLOAT = 1
DTYPE_OUT_CHAR = 2
DTYPE_OUT_UINT = 3

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

# parsed field class prototype
class parsed_field(ctypes.Structure):
    # note prototype is required for linked lists
    pass

parsed_field_ptr = ctypes.POINTER(parsed_field)

parsed_field._fields_ = [("fieldname", FIELDNAME_ARRAY),
            ("dtype", ctypes.c_ubyte),
            ("parsed_val", parsed_result),
            ("next_field", parsed_field_ptr)]

# pointer to parsed_field class prototype
pfield_pntr = ctypes.POINTER(parsed_field)

# field config class prototype
class field_cfg(ctypes.Structure):
    # note prototype is required for linked lists.
    pass

# define pointer to class prototype
field_cfg_ptr = ctypes.POINTER(field_cfg)

# defien fields
field_cfg._fields_ = [("fieldname", FIELDNAME_ARRAY),
            ("bitmask", BITMASK_ARRAY),
            ("num_bits", ctypes.c_ubyte),
            ("converter", ctypes.c_ubyte),
            ("dtype", ctypes.c_ubyte),
            ("sf", ctypes.c_double),
            ("next_field", field_cfg_ptr)]

# message config class
class message_cfg(ctypes.Structure):
    _fields_ = [("message_name", MESSAGENAME_ARRAY),
                ("num_bytes", ctypes.c_ubyte),
                ("num_fields", ctypes.c_ubyte),
                ("whend", ctypes.c_bool),
                ("first_field", field_cfg),
                ("first_pfield", pfield_pntr)]

message_cfg_ptr = ctypes.POINTER(message_cfg)

# specify return types for dll functions
parser_dll.init_msgcfg.restype = ctypes.c_int32
parser_dll.init_msgcfg.argtypes = [message_cfg_ptr, ctypes.c_char_p, ctypes.c_ubyte, ctypes.c_bool]

parser_dll.append_field.restype = ctypes.c_int32
parser_dll.append_field.argtypes = [message_cfg_ptr, bitmask_pointer,
                                 ctypes.c_char_p, ctypes.c_ubyte,
                                 ctypes.c_ubyte, ctypes.c_double]

parser_dll.add_field_at_idx.restype = ctypes.c_int32
parser_dll.add_field_at_idx.argtypes = [message_cfg_ptr, ctypes.c_uint32,
                                 bitmask_pointer, ctypes.c_char_p,
                                 ctypes.c_ubyte, ctypes.c_ubyte, 
                                 ctypes.c_double]

parser_dll.rm_all_msg_fields.restype = ctypes.c_int32
parser_dll.rm_all_msg_fields.argtypes = [message_cfg_ptr]

parser_dll.open_and_parse_file.restype = ctypes.c_int32
parser_dll.open_and_parse_file.argtypes = [ctypes.c_char_p, ctypes.c_char_p, message_cfg_ptr,
                                           ctypes.c_bool]

# define message class.
class message:
    def __init__(self):
        self.msg_cfg = message_cfg()

    def init_msgcfg(self, msgcfg: dict):
        # initializes messageconfig from dict
        # check name length
        assert len(msgcfg["message_name"]) < MAX_FIELDNAME_LEN
        assert type(msgcfg["whend"]) == bool
        msgname = ctypes.c_char_p(msgcfg["message_name"].encode("utf-8"))
        num_bytes = ctypes.c_ubyte(msgcfg["num_bytes"])
        whend = ctypes.c_bool(msgcfg["whend"])
        # initialize message config
        parser_dll.init_msgcfg(self.msg_cfg, msgname, num_bytes, whend);

    def append_field_cfg(self, fieldcfg):
        # appends field to end.
        assert len(fieldcfg["fieldname"]) < MAX_FIELDNAME_LEN
        assert ((fieldcfg["dtype"] >= 0) and (fieldcfg["dtype"] < NUM_DTYPE_OPTIONS))
        assert ((fieldcfg["converter"] >= 0) and (fieldcfg["converter"] < NUM_CONVERTER_OPTIONS))

        fieldname = ctypes.c_char_p(fieldcfg["fieldname"].encode("utf-8"))
        dtype = ctypes.c_ubyte(fieldcfg["dtype"])
        converter = ctypes.c_ubyte(fieldcfg["converter"])
        bitmask = ctypes.pointer(self.bitmask_from_tuple(fieldcfg["bitmask"]))
        sf = ctypes.c_double(fieldcfg["sf"])
        
        # call append_field function from dll.
        parser_dll.append_field(self.msg_cfg, bitmask, fieldname, converter,
                                dtype, sf)

    def parse_file(self, ftoparse:str, fparsed: str, readmethod: bool):
        # opens and parsed file ftoparse and outputs parsed data
        # to file fparsed. Note parsed readmethod 0=binary, 1=hexascii.
        ftoparse_ptr = ctypes.c_char_p(ftoparse.encode("utf-8"))
        fparsed_ptr = ctypes.c_char_p(fparsed.encode("utf-8"))
        parser_dll.open_and_parse_file(ftoparse_ptr, fparsed_ptr, self.msg_cfg, readmethod)

      
    def __del__(self):
        # define function to free fields when class deleted
        parser_dll.rm_all_msg_fields(self.msg_cfg)

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
    field1 = {"fieldname": "testfield",
              "dtype": DTYPE_OUT_INT,
              "converter": READ_COB,
              "bitmask": (255,255,255,255),
              "sf": 1}

    field2 = {"fieldname": "testfield2",
            "dtype": DTYPE_OUT_UINT,
            "converter": READ_UNS,
            "bitmask": (255,255,255,255),
            "sf": 1}

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
    msg.append_field_cfg(field1)
    msg.append_field_cfg(field2)
    msg.append_field_cfg(field3)
    msg.parse_file("testfile.txt", "outfile.txt", 1)
    del(msg)

    #parser.bitmask_from_tuple(field1["bitmask"])