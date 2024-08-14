#pragma once

// This file is included inside gfdStruct.h
//#include "gfdStruct.h"

#include <ninTexUtils/gx2/gx2Shaders.h>
#include <ninTexUtils/gx2/gx2Texture.h>

#include <vector>

//typedef struct _GX2ComputeShader  GX2ComputeShader;

class GFDFile
{
public:
    GFDFile()
        : mHeader() // Zero-initialize
    {
        mHeader.magic = 0x47667832u; // Gfx2
        mHeader.size = sizeof(GFDHeader);
        mHeader.majorVersion = 7;
        mHeader.minorVersion = 1;
        mHeader.gpuVersion = GFD_GPU_VERSION_GPU7;
        mHeader.alignMode = GFD_ALIGN_MODE_ENABLE;
    }

    ~GFDFile()
    {
        destroy();
    }

    bool setVersion(u32 majorVersion, u32 minorVersion, bool updateTextureRegs = true)
    {
        if (majorVersion != 6 && majorVersion != 7)
            return false;

        mHeader.majorVersion = majorVersion;
        mHeader.minorVersion = minorVersion;

        const bool gfd_v7 = majorVersion == 7 ? true : false;

        if (updateTextureRegs)
            for (u32 i = 0; i < mTextures.size(); i++)
                GX2InitTextureRegs(&mTextures[i], gfd_v7);

        return true;
    }

    size_t load(const void* data);
    std::vector<u8> saveGTX() const;
    void destroy();

public:
    GFDHeader mHeader;
    std::vector<GX2Texture> mTextures;
    std::vector<GX2VertexShader> mVertexShaders;
    std::vector<GX2PixelShader> mPixelShaders;
    std::vector<GX2GeometryShader> mGeometryShaders;
    //std::vector<GX2ComputeShader> mComputeShaders;
};
