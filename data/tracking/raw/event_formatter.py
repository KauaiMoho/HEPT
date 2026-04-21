import os
import glob
import pandas as pd

path_head = ""
input_dir = "raw_events"
output_dir = "formatted_events"

os.makedirs(path_head + output_dir, exist_ok=True)


def process_cells(prefix, df):

    # start from cells file
    # get measurement_id and value
    # rename measurement_id to hit_id

    df = df.rename(columns=
        {'measurement_id': 'hit_id',
         'channel0': 'ch0',
         'channel1': 'ch1'
        }
    )
    df = df[['hit_id', 'ch0', 'ch1', 'value']]

    return df, "cells.csv"


def process_hits(prefix, df):

    # start frome measurements file
    # get measurement_id, rename to hit_id
    # get global x/y/z, rename to x/y/z
    # get geometry_id - process into volume/layer_id

    df = df.rename(columns={
        'measurement_id': 'hit_id',
        'global_x':'x',
        'global_y':'y',
        'global_z':'z'
    })


    # CAN ALSO TRY TO GRAB FROM DETECTORS.CSV
    VOL_MASK = 0xff00000000000000
    LAY_MASK = 0x0000fff000000000
    MOD_MASK = 0x000000000fffff00
    VOL_SHIFT = 56
    LAY_SHIFT = 36
    MOD_SHIFT = 8

    geo_ids = df['geometry_id'].astype('uint64').values

    df['volume_id'] = (geo_ids & VOL_MASK) >> VOL_SHIFT
    df['layer_id'] = (geo_ids & LAY_MASK) >> LAY_SHIFT
    df['module_id'] = (geo_ids & MOD_MASK) >> MOD_SHIFT

    df = df[['hit_id', 'x', 'y', 'z', 'volume_id', 'layer_id', 'module_id']]

    return df, "hits.csv"


def process_particles(prefix, df):

    # start from particles file
    # particle_id_part
    # store px, py, pz
    # q
    # vx, vy

    df = df.rename(columns={
        'particle_id_part': 'particle_id'
    })

    df = df[['particle_id', 'px', 'py', 'pz', 'q', 'vx', 'vy']]

    return df, "particles.csv"


def process_truths(prefix, df):

    # store measurments_id from simhit-map as hit_id
    # use hit_id from FILE to access hits.csv (using index col), then compute particle id
    # that row, store next to relevant measurments_id

    dfH = pd.read_csv(path_head + input_dir + "/" + prefix + "-hits.csv")

    df['particle_id'] = df['hit_id'].map(dfH['particle_id_part'])
    df = df.drop('hit_id', axis=1)
    df = df.rename(columns=
        {'measurement_id': 'hit_id'}
    )
    

    return df, "truth.csv"

def process_detectors(prefix, df):

    df = df[["volume_id", "layer_id", "module_id", "rot_xu", "rot_xv", "rot_xw", "rot_yu",
              "rot_yv", "rot_yw", "rot_zu", "rot_zv", "rot_zw", "module_t", "pitch_u", "pitch_v"]]

    return df, "detector.csv"


def route_file(filename):
    if filename.endswith("cells.csv"):
        return process_cells
    elif filename.endswith("measurements.csv"):
        return process_hits
    elif filename.endswith("measurement-simhit-map.csv"):
        return process_truths
    elif filename.endswith("particles.csv"):
        return process_particles
    elif filename.endswith("detectors.csv"):
        return process_detectors
    else:
        return None
    
def build_output_filename(original_filename, new_suffix):
    prefix = original_filename.split("-", 1)[0]
    if (prefix != original_filename):
        return f"{prefix}-{new_suffix}"
    return new_suffix

print("Started event formatting...")

for filepath in glob.glob(os.path.join(path_head + input_dir, "*.csv")):
    filename = os.path.basename(filepath)
    prefix = filename.split('-')[0]

    process_function = route_file(filename)

    if process_function is None:
        continue

    try:

        df = pd.read_csv(filepath)

        df_processed, new_suffix = process_function(prefix, df)

        new_filename = build_output_filename(filename, new_suffix)
        output_path = os.path.join(path_head + output_dir, new_filename)

        df_processed.to_csv(output_path, index=False)

    except Exception as e:
        print(f"Error processing {filename}: {e}")

print("Done formatting.")