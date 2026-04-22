# %% [markdown]
# # Build Graphs
#
# In this notebook we build graphs from the raw data.

# %%
from preprocessing.point_cloud_builder import PointCloudBuilder
from pathlib import Path
import sys

# %%
n_sectors = 1

tp = sys.argv[1]

# %%
data_path = Path("./")
# Unprocessed data should live here
input_dir = data_path / f"formatted_{tp}"
assert data_path.is_dir()
detector_config_path = data_path / f"raw_signal" / "detectors.csv" #TODO: TEMPORARY, CURRENTLY HARDCODED TO SIGNAL DETECTOR

# %%
# build point clouds for each sector in the pixel layers only
pc_builder = PointCloudBuilder(
    indir=input_dir,
    outdir=data_path / f"tracking-{tp}",
    n_sectors=n_sectors,
    pixel_only=False, # TODO: CHANGED TO FALSE
    redo=True,
    measurement_mode=False,
    sector_di=0,
    sector_ds=1.3,
    thld=0.9,
    collect_data=False,
    add_true_edges=True,
    detector_config=detector_config_path,
)
pc_builder.process(stop=None, ignore_loading_errors=True)

# %%
