import struct
from .ktx import KTXHeader, KTXError
from .gx2Texture import GX2TexturePrintInfo
from .gx2Enum import GX2SurfaceFormat, GX2TileMode
from .gx2Surface import GX2Surface
from .gx2Texture import GX2Texture

# Mapping GX2SurfaceFormat to OpenGL formats
# GX2SurfaceFormat to OpenGL Internal Format Mapping
GX2_TO_GL_FORMAT = {
    GX2SurfaceFormat.Invalid: (0x0, 0x0),  # No corresponding OpenGL format

    # Uncompressed Formats
    GX2SurfaceFormat.Unorm_R8: (0x8229, 0x1401),  # (GL_R8, GL_UNSIGNED_BYTE)
    GX2SurfaceFormat.Unorm_RG8: (0x822B, 0x1401),  # (GL_RG8, GL_UNSIGNED_BYTE)
    GX2SurfaceFormat.Unorm_R16: (0x822A, 0x1403),  # (GL_R16, GL_UNSIGNED_SHORT)
    GX2SurfaceFormat.Unorm_RG16: (0x822C, 0x1403),  # (GL_RG16, GL_UNSIGNED_SHORT)
    GX2SurfaceFormat.Unorm_RGB5A1: (0x8057, 0x8034),  # (GL_RGB5_A1, GL_UNSIGNED_SHORT_5_5_5_1)
    GX2SurfaceFormat.Unorm_RGBA4: (0x8056, 0x8033),  # (GL_RGBA4, GL_UNSIGNED_SHORT_4_4_4_4)
    GX2SurfaceFormat.Unorm_RGBA8: (0x8058, 0x1401),  # (GL_RGBA8, GL_UNSIGNED_BYTE)
    GX2SurfaceFormat.Unorm_RGB10A2: (0x8059, 0x8036),  # (GL_RGB10_A2, GL_UNSIGNED_INT_2_10_10_10_REV)
    GX2SurfaceFormat.Unorm_R24X8: (0x81A6, 0x84F9),  # (GL_DEPTH24_STENCIL8, GL_UNSIGNED_INT_24_8)
    GX2SurfaceFormat.Unorm_RGBA16: (0x805B, 0x1403),  # (GL_RGBA16, GL_UNSIGNED_SHORT)

    # Unsigned Integer Formats
    GX2SurfaceFormat.Uint_R8: (0x8232, 0x1401),  # (GL_R8UI, GL_UNSIGNED_BYTE)
    GX2SurfaceFormat.Uint_RG8: (0x8233, 0x1401),  # (GL_RG8UI, GL_UNSIGNED_BYTE)
    GX2SurfaceFormat.Uint_R16: (0x8234, 0x1403),  # (GL_R16UI, GL_UNSIGNED_SHORT)
    GX2SurfaceFormat.Uint_RG16: (0x8235, 0x1403),  # (GL_RG16UI, GL_UNSIGNED_SHORT)
    GX2SurfaceFormat.Uint_R32: (0x8236, 0x1405),  # (GL_R32UI, GL_UNSIGNED_INT)
    GX2SurfaceFormat.Uint_RG32: (0x8237, 0x1405),  # (GL_RG32UI, GL_UNSIGNED_INT)
    GX2SurfaceFormat.Uint_RGBA8: (0x8D7C, 0x1401),  # (GL_RGBA8UI, GL_UNSIGNED_BYTE)
    GX2SurfaceFormat.Uint_RGBA16: (0x8D76, 0x1403),  # (GL_RGBA16UI, GL_UNSIGNED_SHORT)
    GX2SurfaceFormat.Uint_RGBA32: (0x8D82, 0x1405),  # (GL_RGBA32UI, GL_UNSIGNED_INT)

    # Signed Integer Formats
    GX2SurfaceFormat.Sint_R8: (0x8231, 0x1400),  # (GL_R8I, GL_BYTE)
    GX2SurfaceFormat.Sint_RG8: (0x8238, 0x1400),  # (GL_RG8I, GL_BYTE)
    GX2SurfaceFormat.Sint_R16: (0x8239, 0x1402),  # (GL_R16I, GL_SHORT)
    GX2SurfaceFormat.Sint_RG16: (0x823A, 0x1402),  # (GL_RG16I, GL_SHORT)
    GX2SurfaceFormat.Sint_R32: (0x823B, 0x1404),  # (GL_R32I, GL_INT)
    GX2SurfaceFormat.Sint_RG32: (0x823C, 0x1404),  # (GL_RG32I, GL_INT)
    GX2SurfaceFormat.Sint_RGBA8: (0x8D8E, 0x1400),  # (GL_RGBA8I, GL_BYTE)
    GX2SurfaceFormat.Sint_RGBA16: (0x8D88, 0x1402),  # (GL_RGBA16I, GL_SHORT)
    GX2SurfaceFormat.Sint_RGBA32: (0x8D82, 0x1404),  # (GL_RGBA32I, GL_INT)

    # Normalized Signed Formats
    GX2SurfaceFormat.Snorm_R8: (0x8F94, 0x1400),  # (GL_R8_SNORM, GL_BYTE)
    GX2SurfaceFormat.Snorm_RG8: (0x8F95, 0x1400),  # (GL_RG8_SNORM, GL_BYTE)
    GX2SurfaceFormat.Snorm_RGBA8: (0x8F97, 0x1400),  # (GL_RGBA8_SNORM, GL_BYTE)
    GX2SurfaceFormat.Snorm_R16: (0x8F98, 0x1402),  # (GL_R16_SNORM, GL_SHORT)
    GX2SurfaceFormat.Snorm_RG16: (0x8F99, 0x1402),  # (GL_RG16_SNORM, GL_SHORT)
    GX2SurfaceFormat.Snorm_RGBA16: (0x8F9A, 0x1402),  # (GL_RGBA16_SNORM, GL_SHORT)

    # SRGB Formats
    GX2SurfaceFormat.SRGB_RGBA8: (0x8C43, 0x1401),  # (GL_SRGB8_ALPHA8, GL_UNSIGNED_BYTE)
    GX2SurfaceFormat.SRGB_BC1: (0x8E8C, 0x0),  # (GL_COMPRESSED_SRGB_S3TC_DXT1_EXT, Compressed - no glType)
    GX2SurfaceFormat.SRGB_BC2: (0x8E8E, 0x0),  # (GL_COMPRESSED_SRGB_ALPHA_S3TC_DXT3_EXT, Compressed)
    GX2SurfaceFormat.SRGB_BC3: (0x8E8F, 0x0),  # (GL_COMPRESSED_SRGB_ALPHA_S3TC_DXT5_EXT, Compressed)

    # Floating Point Formats
    GX2SurfaceFormat.Float_R32: (0x822E, 0x1406),  # (GL_R32F, GL_FLOAT)
    GX2SurfaceFormat.Float_RG32: (0x8230, 0x1406),  # (GL_RG32F, GL_FLOAT)
    GX2SurfaceFormat.Float_R16: (0x822D, 0x140B),  # (GL_R16F, GL_HALF_FLOAT)
    GX2SurfaceFormat.Float_RG16: (0x822F, 0x140B),  # (GL_RG16F, GL_HALF_FLOAT)
    GX2SurfaceFormat.Float_RGBA16: (0x881A, 0x140B),  # (GL_RGBA16F, GL_HALF_FLOAT)
    GX2SurfaceFormat.Float_RGBA32: (0x8814, 0x1406),  # (GL_RGBA32F, GL_FLOAT)
    GX2SurfaceFormat.Float_RG11B10: (0x8C3A, 0x1406),  # (GL_R11F_G11F_B10F, GL_FLOAT)

    # Compressed Formats
    GX2SurfaceFormat.Unorm_BC1: (0x83F0, 0x0),  # (GL_COMPRESSED_RGB_S3TC_DXT1_EXT, Compressed)
    GX2SurfaceFormat.Unorm_BC2: (0x83F2, 0x0),  # (GL_COMPRESSED_RGBA_S3TC_DXT3_EXT, Compressed)
    GX2SurfaceFormat.Unorm_BC3: (0x83F3, 0x0),  # (GL_COMPRESSED_RGBA_S3TC_DXT5_EXT, Compressed)
    GX2SurfaceFormat.Unorm_BC4: (0x8DBB, 0x0),  # (GL_COMPRESSED_RED_RGTC1, Compressed)
    GX2SurfaceFormat.Unorm_BC5: (0x8DBC, 0x0),  # (GL_COMPRESSED_RG_RGTC2, Compressed)
}


def GX2SurfaceGetLevels(surface):
    levels = []
    levels.append(surface.imageData[:surface.imageSize])

    for mipLevel in range(1, surface.numMips):
        if mipLevel == 1:
            offset = 0
        else:
            offset = surface.mipOffset[mipLevel - 1]

        end = surface.mipOffset[mipLevel] if mipLevel < surface.numMips - 1 else surface.mipSize
        levels.append(surface.mipData[offset:end])

    return levels


def GX2TextureToKTX(texture: GX2Texture, filename: str, printInfo=False):
    """
    Converts a GX2Texture to a KTX file.

    :param texture: The GX2Texture object to convert.
    :param filename: The output KTX file path.
    :param printInfo: Whether to print debug information.
    """
    if printInfo:
        GX2TexturePrintInfo(texture)

    # Initialize KTX Header
    ktx_header = KTXHeader()
    ktx_header.endianness = 0x04030201  # Little endian
    ktx_header.pixelWidth = texture.surface.width
    ktx_header.pixelHeight = texture.surface.height
    ktx_header.pixelDepth = texture.surface.depth
    ktx_header.numArrayElements = 0
    ktx_header.numFaces = 1
    ktx_header.numMipLevels = texture.surface.numMips
    ktx_header.bytesOfKeyValueData = 0  # No key-value data

    # Set OpenGL format based on GX2SurfaceFormat
    if texture.surface.format not in GX2_TO_GL_FORMAT:
        raise NotImplementedError(f"GX2SurfaceFormat {texture.surface.format} not supported for KTX export.")

    gl_format, gl_type = GX2_TO_GL_FORMAT[texture.surface.format]
    ktx_header.glFormat = gl_format
    ktx_header.glType = gl_type

    # Handle compressed formats
    if texture.surface.format.isCompressed():
        # KTX requires specifying compressed formats using glInternalFormat
        ktx_header.glInternalFormat = gl_format
        ktx_header.glBaseInternalFormat = gl_format
    else:
        ktx_header.glInternalFormat = gl_format
        ktx_header.glBaseInternalFormat = gl_format

    # Create a new GX2Texture to store the untiled texture
    linear_texture = GX2Texture.initTexture(
        texture.surface.dim, texture.surface.width, texture.surface.height,
        texture.surface.depth, texture.surface.numMips, texture.surface.format,
        texture.compSel, GX2TileMode.Linear_Special,
    )

    # Untile the texture
    GX2Surface.copySurface(texture.surface, linear_texture.surface)

    # Get all mip levels
    levels = GX2SurfaceGetLevels(linear_texture.surface)

    # Collect image data for all mip levels
    image_data = b''
    for level_data in levels:
        # Append the level's size
        image_data += struct.pack('<I', len(level_data))
        # Append the level's data
        image_data += level_data
        # Pad to 4-byte boundaries
        padding = (4 - (len(level_data) % 4)) % 4
        image_data += b'\x00' * padding

    # Combine header and image data
    ktx_file = ktx_header.save() + image_data
    """
    # Write to file
    with open(filename, 'wb') as f:
        f.write(ktx_file)

    if printInfo:
        print(f"KTX file '{filename}' exported successfully.")
    """
    return ktx_file

# Note: You need to define GL_RGBA, GL_UNSIGNED_BYTE, etc., or use a library like PyOpenGL to get these constants.
