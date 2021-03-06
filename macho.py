from struct import Struct

# little-endian 0xfeedface
MH_MAGIC = b'\xce\xfa\xed\xfe'
# little-endian 0xfeedfacf
MH_MAGIC_64 = b'\xcf\xfa\xed\xfe'
LC_CODE_SIGNATURE = 0x1d

# def struct_factory(target, little_endian=True):
#     if little_endian:
#         base = LittleEndianStructure
#     else:
#         base = BigEndianStructure
#     return type(target.__name__, (target, base), {})()

class DynStruct(Struct):
    """
    struct.Struct with configurable endian
    """
    _fields_ = []
    def __init__(self, little_endian=True):
        if not self._fields_:
            raise NotImplementedError("Need to be subclassed")
        self._keys, fmts = zip(*self._fields_)
        self._fmt = ''.join(fmts)
        pad = '<' if little_endian else '>'
        self._fmt = ''.join(
            (pad, self._fmt))
        super().__init__(self._fmt)
        return

    def unpack_to_dict(self, buffer):
        """Unpack data into dict() corresponding to subclass definition"""
        data = zip(self._keys, self.unpack(buffer))
        self.__dict__.update(data)
        return data

    def pack_from_dict(self, data=None):
        """Pack data into binary form using internal data mapping"""
        binary = (getattr(self, key) for key in self._keys)
        return self.pack(*binary)


class MachHeader(DynStruct):
    """
    struct mach_header {
        uint32_t	magic;		/* mach magic number identifier */
        cpu_type_t	cputype;	/* cpu specifier */
        cpu_subtype_t	cpusubtype;	/* machine specifier */
        uint32_t	filetype;	/* type of file */
        uint32_t	ncmds;		/* number of load commands */
        uint32_t	sizeofcmds;	/* the size of all the load commands */
        uint32_t	flags;		/* flags */
    };
    """
    _fields_ = [
        ("magic", "I"),
        ("cputype", "I"),
        ("cpusubtype", "I"),
        ("filetype", "I"),
        ("ncmds", "I"),
        ("sizeofcmds", "I"),
        ("flags", "I"),
    ]




class MachHeader64(DynStruct):
    """
    struct mach_header_64 {
        uint32_t	magic;		/* mach magic number identifier */
        cpu_type_t	cputype;	/* cpu specifier */
        cpu_subtype_t	cpusubtype;	/* machine specifier */
        uint32_t	filetype;	/* type of file */
        uint32_t	ncmds;		/* number of load commands */
        uint32_t	sizeofcmds;	/* the size of all the load commands */
        uint32_t	flags;		/* flags */
        uint32_t	reserved;	/* reserved */
    };
    """
    _fields_ = [
        ("magic", "I"),
        ("cputype", "I"),
        ("cpusubtype", "I"),
        ("filetype", "I"),
        ("ncmds", "I"),
        ("sizeofcmds", "I"),
        ("flags", "I"),
        ("reserved", "I"),
    ]

class LoadCommand(DynStruct):
    """
    struct load_command {
        uint32_t cmd;		/* type of load command */
        uint32_t cmdsize;	/* total size of command in bytes */
    };
    """
    _fields_ = [
        ("cmd", "I"),
        ("cmdsize", "I"),
    ]


class LinkeditDataCommand(DynStruct):
    """
    struct linkedit_data_command {
        uint32_t	cmd;		/* LC_CODE_SIGNATURE, LC_SEGMENT_SPLIT_INFO,
                                    LC_FUNCTION_STARTS, LC_DATA_IN_CODE,
                    LC_DYLIB_CODE_SIGN_DRS or
                    LC_LINKER_OPTIMIZATION_HINT. */
        uint32_t	cmdsize;	/* sizeof(struct linkedit_data_command) */
        uint32_t	dataoff;	/* file offset of data in __LINKEDIT segment */
        uint32_t	datasize;	/* file size of data in __LINKEDIT segment  */
    };
    """
    _fields_ = [
        ("cmd", "I"),
        ("cmdsize", "I"),
        ("dataoff", "I"),
        ("datasize", "I"),
    ]
