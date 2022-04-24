#!/usr/bin/env python

from sqlalchemy import (Column, ForeignKey, Integer, MetaData, Table,
                        create_engine)
from sqlalchemy.dialects.mysql import CHAR, DOUBLE, SMALLINT, VARCHAR

engine = create_engine(
    'mysql+pymysql://user:user_pass@127.0.0.1/territory',
    connect_args=dict(host='127.0.0.1', port=3306)
)
metadata_obj = MetaData()


districts = Table(
    'districts',
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('ntacode', CHAR(4), nullable=False),
    Column('shape_area', DOUBLE(10, 2), nullable=False),
    Column('county_fips', CHAR(3), nullable=False),
    Column('ntaname', VARCHAR(100), nullable=False),
    Column('boro_name', VARCHAR(50), nullable=False),
    Column('boro_code', SMALLINT(1), nullable=False),
)


plots = Table(
    'plots',
    metadata_obj,
    Column('bbl', Integer, primary_key=True, autoincrement=False),
    Column(
        'district_id',
        ForeignKey('districts.id', ondelete="CASCADE"),
        nullable=False
    ),
    Column('shape_area', DOUBLE(10, 2), nullable=False)
)


if __name__ == '__main__':
    metadata_obj.create_all(engine)
