#!/usr/bin/env python

import json
import os
import sys

import geopandas as gpd

script_dir = os.path.dirname(__file__)
sys.path.insert(1, script_dir)

from db import engine  # noqa
from utilities import (fillna_district_ids, gpd_geographic_area,  # noqa
                       upload_to_db)

with open(os.path.join(script_dir, '..', 'data', 'districts.json'), 'r') as f:
    data = json.load(f)
districts_df = gpd.GeoDataFrame.from_features(data['features'])
districts_df.index += 1
districts_df = districts_df.set_crs('epsg:3857')
districts_df = districts_df.assign(
    shape_area=gpd_geographic_area(districts_df)
)

with open(os.path.join(script_dir, '..', 'data', 'plots.json'), 'r') as f:
    data = json.load(f)
plots_df = gpd.GeoDataFrame.from_features(data['features'])
plots_df = plots_df.set_crs('epsg:3857')
plots_df = plots_df.assign(shape_area=gpd_geographic_area(plots_df))
plots_df = gpd.sjoin(
    plots_df,
    districts_df[['geometry']],
    how='left',
    predicate='within'
)
plots_df = plots_df.rename(columns={'index_right': 'district_id'})
plots_df = fillna_district_ids(plots_df, districts_df)

upload_to_db(plots_df, districts_df, engine)
