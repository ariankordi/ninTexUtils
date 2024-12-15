import struct
from .ktx import KTXHeader, KTXError
from .gx2Texture import GX2TexturePrintInfo
from .gx2Enum import GX2SurfaceFormat, GX2TileMode
from .gx2Texture import GX2Texture, GX2SurfaceDim, Linear2DToGX2Texture, GX2CompSel

# Mapping OpenGL formats to GX2SurfaceFormat
GL_TO_GX2_FORMAT = {
    0x0: GX2SurfaceFormat.Invalid,  # No corresponding GX2 format

    # Uncompressed Formats
    0x8229: GX2SurfaceFormat.Unorm_R8,          # GL_R8
    0x822A: GX2SurfaceFormat.Unorm_R16,         # GL_R16
    0x822B: GX2SurfaceFormat.Unorm_RG8,         # GL_RG8
    0x822C: GX2SurfaceFormat.Unorm_RG16,        # GL_RG16
    0x8058: GX2SurfaceFormat.Unorm_RGBA8,       # GL_RGBA8
    0x805B: GX2SurfaceFormat.Unorm_RGBA16,      # GL_RGBA16
    0x8D62: GX2SurfaceFormat.Unorm_RGB565,      # GL_RGB565
    0x8056: GX2SurfaceFormat.Unorm_RGBA4,       # GL_RGBA4
    0x8057: GX2SurfaceFormat.Unorm_RGB5A1,      # GL_RGB5_A1
    0x8059: GX2SurfaceFormat.Unorm_RGB10A2,     # GL_RGB10_A2
    0x8051: GX2SurfaceFormat.Unorm_RGBA8,       # GL_RGB8 (Assuming RGBA8)
    0x1903: GX2SurfaceFormat.Unorm_R8,          # GL_RED
    0x1907: GX2SurfaceFormat.Unorm_RGBA8,       # GL_RGB (Assuming RGBA8)
    0x1908: GX2SurfaceFormat.Unorm_RGBA8,       # GL_RGBA
    0x8227: GX2SurfaceFormat.Unorm_RG8,         # GL_RG

    # Unsigned Integer Formats
    0x8236: GX2SurfaceFormat.Uint_R32,          # GL_R32UI
    0x8D70: GX2SurfaceFormat.Uint_RGBA32,       # GL_RGBA32UI
    0x8234: GX2SurfaceFormat.Uint_R16,          # GL_R16UI
    0x8238: GX2SurfaceFormat.Uint_RG8,          # GL_RG8UI
    0x823A: GX2SurfaceFormat.Uint_RG16,         # GL_RG16UI
    0x823C: GX2SurfaceFormat.Uint_RG32,         # GL_RG32UI
    0x8D71: GX2SurfaceFormat.Uint_RGB10A2,      # GL_RGB32UI (Assuming RGB10A2)
    0x8D76: GX2SurfaceFormat.Uint_RGBA16,       # GL_RGBA16UI
    0x8D77: GX2SurfaceFormat.Uint_RGBA16,       # GL_RGB16UI (Assuming RGBA16)
    0x8D7C: GX2SurfaceFormat.Uint_RGBA8,        # GL_RGBA8UI
    0x8D7D: GX2SurfaceFormat.Uint_RGBA8,        # GL_RGB8UI (Assuming RGBA8)


    # Signed Integer Formats
    0x8233: GX2SurfaceFormat.Sint_R16,          # GL_R16I
    0x8235: GX2SurfaceFormat.Sint_R32,          # GL_R32I
    0x8237: GX2SurfaceFormat.Sint_RG8,          # GL_RG8I
    0x8239: GX2SurfaceFormat.Sint_RG16,         # GL_RG16I
    0x823B: GX2SurfaceFormat.Sint_RG32,         # GL_RG32I
    0x8D82: GX2SurfaceFormat.Sint_RGBA32,       # GL_RGBA32I
    0x8D83: GX2SurfaceFormat.Sint_RGB10A2,      # GL_RGB32I (Assuming RGB10A2)
    0x8D88: GX2SurfaceFormat.Sint_RGBA16,       # GL_RGBA16I
    0x8D89: GX2SurfaceFormat.Sint_RGBA16,       # GL_RGB16I (Assuming RGBA16)
    0x8D8E: GX2SurfaceFormat.Sint_RGBA8,        # GL_RGBA8I
    0x8D8F: GX2SurfaceFormat.Sint_RGBA8,        # GL_RGB8I


    # Normalized Signed Formats
    0x8F94: GX2SurfaceFormat.Snorm_R8,          # GL_R8_SNORM
    0x8F95: GX2SurfaceFormat.Snorm_RG8,         # GL_RG8_SNORM
    0x8F96: GX2SurfaceFormat.Snorm_RGBA8,       # GL_RGB8_SNORM (Assuming RGBA8)
    0x8F97: GX2SurfaceFormat.Snorm_RGBA8,       # GL_RGBA8_SNORM
    0x8F98: GX2SurfaceFormat.Snorm_R16,         # GL_R16_SNORM
    0x8F99: GX2SurfaceFormat.Snorm_RG16,        # GL_RG16_SNORM
    0x8F9A: GX2SurfaceFormat.Snorm_RGBA16,      # GL_RGB16_SNORM (Assuming RGBA16)
    0x8F9B: GX2SurfaceFormat.Snorm_RGBA16,      # GL_RGBA16_SNORM

    # SRGB Formats
    0x8C41: GX2SurfaceFormat.SRGB_RGBA8,        # GL_SRGB8
    0x8C43: GX2SurfaceFormat.SRGB_RGBA8,        # GL_SRGB8_ALPHA8

    # Floating Point Formats
    0x822E: GX2SurfaceFormat.Float_R32,  # GL_R32F
    0x8230: GX2SurfaceFormat.Float_RG32,  # GL_RG32F
    0x822D: GX2SurfaceFormat.Float_R16,  # GL_R16F
    0x822F: GX2SurfaceFormat.Float_RG16,  # GL_RG16F
    0x881A: GX2SurfaceFormat.Float_RGBA16,  # GL_RGBA16F
    0x8814: GX2SurfaceFormat.Float_RGBA32,  # GL_RGBA32F
    0x8C3A: GX2SurfaceFormat.Float_RG11B10,  # GL_R11F_G11F_B10F
    0x88F0: GX2SurfaceFormat.Float_D24S8,  # GL_DEPTH24_STENCIL8

    # Compressed Formats
    0x83F0: GX2SurfaceFormat.Unorm_BC1,  # GL_COMPRESSED_RGB_S3TC_DXT1_EXT
    0x83F2: GX2SurfaceFormat.Unorm_BC2,  # GL_COMPRESSED_RGBA_S3TC_DXT3_EXT
    0x83F3: GX2SurfaceFormat.Unorm_BC3,  # GL_COMPRESSED_RGBA_S3TC_DXT5_EXT
    0x8DBB: GX2SurfaceFormat.Unorm_BC4,  # GL_COMPRESSED_RED_RGTC1
    0x8DBC: GX2SurfaceFormat.Unorm_BC5,  # GL_COMPRESSED_RG_RGTC2
    0x8E8C: GX2SurfaceFormat.SRGB_BC1,  # GL_COMPRESSED_SRGB_S3TC_DXT1_EXT
    0x8E8E: GX2SurfaceFormat.SRGB_BC2,  # GL_COMPRESSED_SRGB_ALPHA_S3TC_DXT3_EXT
    0x8E8F: GX2SurfaceFormat.SRGB_BC3,  # GL_COMPRESSED_SRGB_ALPHA_S3TC_DXT5_EXT

    # YUV Format
    0x8C70: GX2SurfaceFormat.Unorm_NV12,  # GL_NV12 (Requires GL extension)

    # Add more mappings as necessary...
}
def KTXToGX2Texture(filename, surfMode, perfModulation, tileMode, swizzle, SRGB, compSelIdx, printInfo=True):
    """
    Converts a KTX file to a GX2Texture object, handling extra mip levels and padding.

    :param filename: The input KTX file path.
    :param surfMode: Surface mode parameter for GX2Texture.
    :param perfModulation: Performance modulation parameter for GX2Texture.
    :param tileMode: Tile mode for GX2Texture.
    :param swizzle: Swizzle parameter for GX2Texture.
    :param SRGB: Boolean indicating if SRGB is used.
    :param compSelIdx: Component selector indices.
    :param printInfo: Whether to print debug information.
    :return: GX2Texture object.
    """
    with open(filename, 'rb') as f:
        data = f.read()

    if not KTXHeader.is_valid_ktx(data):
        raise RuntimeError("Not a valid KTX input file!")

    ktx_header = KTXHeader()
    try:
        ktx_header.load(data)
    except KTXError as e:
        raise RuntimeError(f"Failed to load KTX header: {e}") from None

    # Validate KTX properties
    if ktx_header.pixelDepth > 1:
        raise NotImplementedError("3D textures are not supported!")

    if ktx_header.numFaces != 1:
        raise NotImplementedError("Cube maps and array textures are not supported!")

    if ktx_header.numMipLevels < 1:
        raise KTXError("KTX file must include at least one mip level.")

    # Determine GX2SurfaceFormat from OpenGL format
    if ktx_header.glBaseInternalFormat not in GL_TO_GX2_FORMAT:
        raise RuntimeError(f"Unsupported OpenGL format: {ktx_header.glBaseInternalFormat}")

    gx2_format = GL_TO_GX2_FORMAT[ktx_header.glBaseInternalFormat]

    # Collect image and mip data
    imageData = b""
    mipData = b""
    offset = 64 + ktx_header.bytesOfKeyValueData  # Header size + key-value data

    maxExpectedMips = (ktx_header.pixelWidth.bit_length() - 1)  # Max mip levels based on width
    validMipCount = min(min(ktx_header.numMipLevels, maxExpectedMips), 13)

    for mip in range(validMipCount):
        if offset + 4 > len(data):
            raise KTXError(f"Unexpected end of file while reading mipmap size at mip {mip}.")

        # Read the mip size
        mip_size = struct.unpack('<I', data[offset:offset + 4])[0]
        offset += 4  # Advance past the mip size

        if offset + mip_size > len(data):
            raise KTXError(f"Unexpected end of file while reading mipmap data at mip {mip}.")

        # Append to imageData or mipData
        if mip == 0:
            imageData += data[offset:offset + mip_size]
        else:
            mipData += data[offset:offset + mip_size]

        offset += mip_size  # Advance past the mip data

        # Skip padding to align to 4-byte boundaries
        padding = (4 - (mip_size % 4)) % 4
        offset += padding

    if ktx_header.numMipLevels > validMipCount:
        print(f"Truncated {ktx_header.numMipLevels - validMipCount} extra mip levels.")

    # Combine the component selectors read from the input files and the user
    compSel = (compSelIdx[0] << 24 |
               compSelIdx[1] << 16 |
               compSelIdx[2] << 8 |
               compSelIdx[3])

    # Create GX2Texture using Linear2DToGX2Texture
    texture = Linear2DToGX2Texture(
        width=ktx_header.pixelWidth,
        height=ktx_header.pixelHeight,
        numMips=validMipCount,
        format_=gx2_format,
        compSel=compSel,
        imageData=imageData,
        tileMode=tileMode,
        swizzle=swizzle,
        mipData=mipData,
        surfMode=surfMode,
        perfModulation=perfModulation
    )

    if printInfo:
        GX2TexturePrintInfo(texture)

    return texture
