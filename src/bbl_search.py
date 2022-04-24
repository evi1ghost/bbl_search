#!/usr/bin/env python

import click
import os
import sys

import pandas as pd

script_dir = os.path.dirname(__file__)
sys.path.insert(1, script_dir)

from db import engine  # noqa


@click.group()
def cli():
    pass


def exit_app_with_error(msg, exit_code):
    click.echo(f'Error: {msg}')
    sys.exit(exit_code)


def get_data_from_db(query):
    with engine.connect() as conn:
        data = pd.read_sql(query, conn)
    return data.to_string(index=False)


def execute_query(query):
    with engine.connect() as conn:
        conn.execute(query)


@cli.command(name='districts-info')
def get_districts_info():
    """Show info about districts having at least one plot."""
    query = """
        SELECT
            d.ntacode,
            d.ntaname,
            d.shape_area,
            COUNT(p.bbl) as plots_number
        FROM districts d
        LEFT JOIN plots p ON d.id = p.district_id
        WHERE p.is_deleted IS FALSE
        GROUP BY d.ntacode, d.ntaname, d.shape_area
        HAVING COUNT(p.bbl) > 0
        ORDER BY COUNT(p.bbl) DESC;
    """
    click.echo(get_data_from_db(query))


@cli.command(name='bbl')
@click.argument('bbl')
def bbl_search(bbl):
    """Search plot by bbl."""
    if not bbl.isdigit():
        exit_app_with_error(
            'Invalid bbl number. Only digits is allowed.',
            2
        )
    if len(bbl) != 10:
        exit_app_with_error(
            'Invalid length of bbl number. Valid length - 10 digits.',
            2
        )
    query = f"""
        SELECT p.bbl, p.shape_area, d.ntacode, d.ntaname
        FROM plots p
        LEFT JOIN districts d ON p.district_id = d.id
        WHERE p.bbl = {bbl} AND p.is_deleted IS FALSE;
    """
    click.echo(get_data_from_db(query))


@cli.command(name='area-range')
def get_area_range():
    """Return max and min areas of plots."""
    query = """
        SELECT
            MIN(p.shape_area) AS minimum_area,
            MAX(p.shape_area) AS maximum_area
        FROM plots p
        WHERE p.is_deleted IS FALSE;
    """
    click.echo(get_data_from_db(query))


@cli.command(name='delete')
@click.argument('start')
@click.argument('stop')
def delete_by_area(start, stop):
    """Delete plots with areas within interval."""
    err_msg = (
        'Invalid value.\n'
        'To set the interval enter START and STOP values of area interval.'
        ' For float number use dots.'
    )
    try:
        start, stop = list(map(float, [start, stop]))
    except ValueError:
        exit_app_with_error(err_msg, 2)
    query = f"""
        UPDATE plots
        SET is_deleted = TRUE
        WHERE shape_area BETWEEN {start} AND {stop};
    """
    execute_query(query)
    click.echo(f'bbl with areas between {start} and {stop} were deleted.')


@cli.command(name='flush')
def flush_changes():
    """Restore deleted plots."""
    query = """
        UPDATE plots
        SET is_deleted = FALSE
        WHERE is_deleted is TRUE;
    """
    execute_query(query)
    click.echo('All changes were canceled.')


if __name__ == '__main__':
    cli()
