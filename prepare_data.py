import numpy as np
import pandas as pd
import datetime
import csv
from pyproj import Transformer  # !pip install pyproj


def clean_csv_data(file_name, min_cols=None):
    rows = []
    with open(file_name, "r") as f:
        for i, row in enumerate(f.readlines()):
            row = row.replace('\n', '')  # remove \n at the end
            if i == 0:
                rows.append(row.split(","))
                if min_cols is None:
                    min_cols = len(rows[0])
            else:
                cleaned_row = [str_value for str_value in row.split(",") if len(str_value) > 2]
                if min_cols <= len(cleaned_row) <= len(rows[0]):
                    rows.append(cleaned_row)
    
    new_file_name = file_name[:-4]+"_cleaned.csv"
    with open(new_file_name, 'w', newline='') as f:
        write = csv.writer(f)
        write.writerows(rows)
    return new_file_name


transformer = Transformer.from_crs("EPSG:3794", "EPSG:4326", always_xy=True)

def convert_coordinates(x, y, reverse_coords=False):
    """
    Convert D96 coordinates to WGS84 (lon, lat).
    NOTE: x, y are coordinates of point on my plot that I use in analysis. 
          Real X and Y are switched. (use reverse_coords parameter).
    """
    if reverse_coords:
        x, y = y, x
    lon, lat = transformer.transform(x, y)
    return lon, lat

def clean_and_get_coordinates(df, xy_properties=["X", "Y"], xlim=(35000, 200000), ylim=(350000, 700000), reverse=False, return_df=False):
    df = df.loc[(df[xy_properties[0]] >= xlim[0]) & (df[xy_properties[0]] <= xlim[1])]
    df = df.loc[(df[xy_properties[1]] >= ylim[0]) & (df[xy_properties[1]] <= ylim[1])]

    X = [df[xy_properties[0]][key] for key in df[xy_properties[0]].keys()]
    Y = [df[xy_properties[1]][key] for key in df[xy_properties[1]].keys()]

    if reverse:
        X, Y = Y, X  # switch coordinates

    if return_df:
        return df
    return X, Y




