#ifndef NIN_TEX_UTILS_GX2_SURFACE_H_
#define NIN_TEX_UTILS_GX2_SURFACE_H_

#include "gx2Enum.h"
#include <assert.h>

typedef struct _GX2Surface
{
    GX2SurfaceDim dim;
    u32 width;
    u32 height;
    u32 depth;
    u32 numMips;
    GX2SurfaceFormat format;
    GX2AAMode aa;
    GX2SurfaceUse use;
    u32 imageSize;
    void* imagePtr;
    u32 mipSize;
    void* mipPtr;
    GX2TileMode tileMode;
    u32 swizzle;
    u32 alignment;
    u32 pitch;
    u32 mipOffset[13];
}
GX2Surface;
static_assert32(sizeof(GX2Surface) == 0x74, "GX2Surface size mismatch");

#ifdef __cplusplus
extern "C"
{
#endif

void GX2CalcSurfaceSizeAndAlignment(GX2Surface* surf);

void GX2CopySurface(
    const GX2Surface* src,
    u32               srcLevel,
    u32               srcSlice,
    GX2Surface*       dst,
    u32               dstLevel,
    u32               dstSlice
);

void GX2SurfaceVerifyForSerialization(const GX2Surface* surf);

void LoadGX2Surface(
    const void* data,
    GX2Surface* surf,
#ifdef __cplusplus
    bool        serialized  = true,
    bool        isBigEndian = true
#else
    bool        serialized,
    bool        isBigEndian
#endif
);

inline void SaveGX2Surface(
    void* data,
    const GX2Surface* surf,
#ifdef __cplusplus
    bool        isBigEndian = true
#else
    bool        isBigEndian
#endif
)
{
    assert(surf);

    void* imagePtr = surf->imagePtr;
    void* mipPtr = surf->mipPtr;

    GX2Surface* surf_cc = (GX2Surface*)surf;
    surf_cc->imagePtr = (void*)0;
    surf_cc->mipPtr = (void*)0;

    GX2SurfaceVerifyForSerialization(surf);
    LoadGX2Surface(surf, (GX2Surface*)data, false, isBigEndian);

    if (surf != data)
    {
        surf_cc->imagePtr = imagePtr;
        surf_cc->mipPtr = mipPtr;
    }
}

void GX2SurfacePrintInfo(const GX2Surface* surf);

#ifdef __cplusplus
}
#endif

#endif
