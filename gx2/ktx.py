import struct
import enum

class KTXError(Exception):
    pass

class KTXHeader:
    # KTX file identifier
    identifier = b'\xABKTX 11\xBB\r\n\x1A\n'

    # Struct format for endianness, glType, glTypeSize, glFormat, glInternalFormat, glBaseInternalFormat, etc.
    header_struct = '<12sIiiIIIIII'

    def __init__(self):
        self.endianness = 0x04030201
        self.glType = 0
        self.glTypeSize = 1
        self.glFormat = 0
        self.glInternalFormat = 0
        self.glBaseInternalFormat = 0
        self.pixelWidth = 0
        self.pixelHeight = 0
        self.pixelDepth = 0
        self.numArrayElements = 0
        self.numFaces = 1
        self.numMipLevels = 1
        self.bytesOfKeyValueData = 0
        self.keyValueData = b''

    def load(self, data):
        if len(data) < 64:
            raise KTXError("Data too short to be a valid KTX file.")

        unpacked = struct.unpack('<12s13I', data[:64])
        if unpacked[0] != self.identifier:
            raise KTXError("Invalid KTX file identifier.")

        (self.identifier, self.endianness, self.glType, self.glTypeSize, self.glFormat,
         self.glInternalFormat, self.glBaseInternalFormat, self.pixelWidth, self.pixelHeight,
         self.pixelDepth, self.numArrayElements, self.numFaces, self.numMipLevels,
         self.bytesOfKeyValueData) = unpacked

        self.keyValueData = data[64:64 + self.bytesOfKeyValueData]

    def save(self):
        packed = struct.pack(
            '<12s13I',
            self.identifier,
            self.endianness,
            self.glType,
            self.glTypeSize,
            self.glFormat,
            self.glInternalFormat,
            self.glBaseInternalFormat,
            self.pixelWidth,
            self.pixelHeight,
            self.pixelDepth,
            self.numArrayElements,
            self.numFaces,
            self.numMipLevels,
            self.bytesOfKeyValueData
        )
        return packed + self.keyValueData

    @staticmethod
    def is_valid_ktx(data):
        return data.startswith(KTXHeader.identifier)
