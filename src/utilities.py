import geopandas as gpd
import numpy as np
from shapely.geometry.polygon import orient


BBL_MAP = {
    1018030060: 180,
    1009660050: 159,
    1018080028: 180,
    1006510048: 125
}


def gpd_geographic_area(geodf):
    """Count the area of polygon"""
    geod = geodf.crs.get_geod()

    def area_calc(geom):
        if geom.geom_type == 'MultiPolygon':
            return np.sum([area_calc(p) for p in geom.geoms])
        return np.around(geod.geometry_area_perimeter(orient(geom, 1))[0], 2)

    return geodf.geometry.apply(area_calc)


def fillna_by_overlay_area(df, districts_df):
    """
    Add ntacode column based on max intersection area.
    
    Some of plots in the dataframe intersect with several districts.
    Function assign ntacode based on max intersection area.
    """
    df_with_nan = df[df.isna().any(axis=1)]
    df_with_nan = gpd.overlay(
        df_with_nan,
        districts_df[['geometry', 'ntacode']],
        how='intersection',
        keep_geom_type=False
    )
    df_with_nan = df_with_nan.assign(
        overlay_area=gpd_geographic_area(df_with_nan)
    )
    return df_with_nan.drop_duplicates(subset='bbl', keep="last")


def fillna_district_ids(df, districts_df):
    """Fill NaN in district_id column with correspondent values"""
    df_with_ntacodes = fillna_by_overlay_area(df, districts_df)

    nan_rows_df = df[df['district_id'].isna()]
    nan_rows_df = nan_rows_df.merge(
        df_with_ntacodes[['bbl', 'ntacode']],
        on='bbl',
        how='left'
    )
    nan_rows_df = nan_rows_df.merge(
        districts_df.reset_index()[['ntacode', 'index']],
        on='ntacode',
        how='left'
    )
    df = df.merge(nan_rows_df[['bbl', 'index']], on='bbl', how='left')

    def fill_nans(row):
        if np.isnan(row['district_id']):
            if not np.isnan(row['index']):
                return row['index']
            else:
                return BBL_MAP.get(int(row['bbl']))
        else:
            return row['district_id']

    df['district_id'] = df[['bbl', 'district_id', 'index']].apply(
        fill_nans,
        axis=1
    )
    return df[['geometry', 'bbl', 'district_id', 'shape_area']]


def upload_to_db(plots_df, districts_df, engine):
    plots_df = plots_df[
        [
            'bbl',
            'district_id',
            'shape_area'
        ]
    ]
    districts_df = districts_df[
        [
            'ntacode',
            'shape_area',
            'county_fips',
            'ntaname',
            'boro_name',
            'boro_code'
        ]
    ]

    with engine.connect() as conn:
        districts_df.to_sql('districts', conn, if_exists='append', index=False)
        plots_df.to_sql('plots', conn, if_exists='append', index=False)
