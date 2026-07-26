import pdal
import json
import numpy as np
from scipy import ndimage
import rasterio

# =========================
# config
# =========================
input_las = "/path/to/lasfile.las"
resolution = 1.0
output_dtm =  "/path/to/DTM.tif"
output_dsm =  "/path/to/DSM.tif"
output_dchm = "/path/to/DHCM.tif"

# SMRF
smrf_scalar = 1.25
smrf_slope = 0.15
smrf_threshold = 0.5
smrf_window = 16.0

# outlier removal
mean_k = 8
multiplier = 2.0

# interpolation parameter (DTM）
window_size_dtm = 10   # window size
radius_dtm = 5      # search radius

# interpolation parameter（DSM）
window_size_dsm = 5  # window size
radius_dsm  = 1.5      # search radius


# =========================
# DTM
# =========================
dtm_pipeline = {
    "pipeline": [
        input_las,
        {
            "type": "filters.outlier",
            "method": "statistical",
            "mean_k": mean_k,
            "multiplier": multiplier
        },
        {
            "type": "filters.smrf",
            "scalar": smrf_scalar,
            "slope": smrf_slope,
            "threshold": smrf_threshold,
            "window": smrf_window
        },
        {
            "type": "filters.range",
            "limits": "Classification[2:2]"
        },
        {
            "type": "writers.gdal",
            "resolution": resolution,
            "output_type": "min",
            "window_size": window_size_dtm,
            "radius": radius_dtm,
            "filename": output_dtm
        }
    ]
}

pdal.Pipeline(json.dumps(dtm_pipeline)).execute()

# =========================
# DSM
# =========================
dsm_pipeline = {
    "pipeline": [
        input_las,
        {
            "type": "filters.outlier",
            "method": "statistical",
            "mean_k": mean_k,
            "multiplier": multiplier
        },
        {
            "type": "writers.gdal",
            "resolution": resolution,
            "output_type": "max",
            "window_size": window_size_dsm,
            "radius": radius_dsm,
            "filename": output_dsm
        }
    ]
}

pdal.Pipeline(json.dumps(dsm_pipeline)).execute()

# =========================
# Raad DTM DSM file
# =========================
with rasterio.open(output_dtm) as src:
    dtm = src.read(1).astype(float)
    transform = src.transform
    profile = src.profile

with rasterio.open(output_dsm) as src:
    dsm = src.read(1).astype(float)

# =========================
# calc CHM
# =========================
chm = dsm - dtm
chm[chm < 0] = 0

# （オプション）平滑化
chm = ndimage.gaussian_filter(chm, sigma=1)

# =========================
# save DCHM
# =========================
profile.update(dtype=rasterio.float32, count=1)

with rasterio.open(output_dchm, "w", **profile) as dst:
    dst.write(chm.astype(np.float32), 1)

print("finished")