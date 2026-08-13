# DSM, DTM and DCHM generation code from point cloud
This code is to generate DSM, DTM and DCHM from point cloud.

# Install Python Libraries
pip install -r requirements.txt

# How to use
Configure output paths and parameters in pdal_DSM_DTM.py.

In "input_las", set the path to the point cloud data (LAS format).
In "resolution", set the resolution of the DSM, DTM, and DCHM (unit: m).
In "output_dtm", set the output path for the DTM, which is exported in GeoTIFF format.
In "output_dsm", set the output path for the DSM, which is exported in GeoTIFF format.
In "output_dchm", set the output path for the DCHM, which is exported in GeoTIFF format.


SMRF is used to distinguish ground points from non-ground points in the point cloud.
In "smrf_scalar", set the parameter related to the height scale of SMRF.
In "smrf_slope", set the parameter related to the terrain slope of SMRF.
In "smrf_threshold", set the height threshold for ground classification.
In "smrf_window", set the spatial scale used for terrain classification.


Outlier removal is used to remove point cloud data that are statistically inconsistent with their surrounding points.
In "mean_k", set the number of neighboring points used to calculate local statistics.
In "multiplier", set the parameter that determines how much a point must differ from its surrounding points to be considered an outlier.


In "window_size_dtm", set the neighborhood size used for DTM interpolation.
In "radius_dtm", set the search distance for finding nearby point cloud data used for DTM interpolation.
To calculate the DTM, the minimum value within each raster cell is used.

In "window_size_dsm", set the neighborhood size used for DSM interpolation.
In "radius_dsm", set the search distance for finding nearby point cloud data used for DSM interpolation.
To calculate the DSM, the maximum value within each raster cell is used.



Next, run as follows.<P>

python pdal_DSM_DTM.py

# Notice
This code is MIT license and non-commercial use ONLY.
