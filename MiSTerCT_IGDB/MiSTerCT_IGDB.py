import os
import click
from core import (
    get_files_from_txt,
    get_data,
    get_official_names,
    get_alternative_names,
    prepare_names,
    search_game_name,
    write_csv,
    print_results,
)

# Set the default encoding to UTF-8.
os.environ["PYTHONIOENCODING"] = "utf-8"


@click.command()
@click.option(
    "--source",
    default="sample_sources",
    help="Source folder for file names",
    type=click.Path(exists=True),
)
@click.option(
    "--output",
    default="output.csv",
    help="Output file name and path",
    type=click.Path(),
)
# for info about platforms ID check INFO\platformsID.txt file
@click.option("--platforms", default="19,58", help="Platforms ID to search")
@click.option(
    "--db",
    default="DB/IGDB.db",
    help="DB file name and path",
    type=click.Path(exists=True)
)
@click.option("--region", default="1", help="Region ID to search")
def cli(source, output, platforms, db, region):
    """MiSTerCT_IGDB CLI"""

    source_path = os.path.abspath(source)
    output_path = os.path.abspath(output)
    db_path = os.path.abspath(db)

    print(f"Source: {source_path}")
    print(f"Output: {output_path}")
    print(f"DB: {db_path}")
    print(f"Platforms: {platforms}")

    df_data = get_data(db_path, platforms)
    df_names_off = get_official_names(db_path, platforms)
    df_names_alt = get_alternative_names(db_path, platforms)

    df_names_off = prepare_names(df_names_off)
    df_names_alt = prepare_names(df_names_alt)

    # from directory
    # files = get_files_from_dir(source)

    # from txt file
    files = get_files_from_txt(os.path.join(source_path, "SNES.txt"))

    results, found, not_found = search_game_name(files, df_names_off, df_names_alt)
    write_csv(output_path, results)

    print_results(found, not_found)

    # for x in range(len(games)):
    #     genre = str(games[x]['genre'])
    #     genre = genre.split(' / ', 1)[0]
    #     print(genre)
    #     createFolder(genre)
    #     filename = str(games[x]['path']).replace('./','',1)
    #     print(subfolder + '/' + genre + '/' + filename)
    #     shutil.copyfile(source + '/' + filename, subfolder + '/' + genre + '/' + filename)


if __name__ == "__main__":
    cli()
