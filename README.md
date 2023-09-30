# MiSTerCT-IGDB

Classification tool for MiSTer cores based on IGDB data.

The tool is still in development and not ready for use however it will allow you to have organized roms in folder and filenames based on IGDB data.

## Local DB

Based on SQLite3.

The empty DB file ``IGDB_empty.db`` is prefilled with some views:

* v_agr_all
* v_agr_developers
* v_agr_game_engines
* v_agr_game_modes
* v_agr_genres
* v_agr_player_perspectives
* v_agr_publishers
* v_alternative_names
* v_alternative_names_regions
* v_complete_names
* v_official_names
* v_official_names_regions
* v_simple_developers
* v_simple_game_engines
* v_simple_game_modes
* v_simple_games
* v_simple_genres
* v_simple_player_perspectives
* v_simple_publishers
* v_simple_releases


## Usage

Since IGDB uses Twitch API authentication, you need to register your own application and get a client ID and secret. You can do this here: https://dev.twitch.tv/console/apps/create

Then you have to export the following environment variables:

```
export TWITCH_CLIENT_ID=<your client id>
export TWITCH_CLIENT_SECRET=<your secret id>
```
or like this if you're on windows:
```
set TWITCH_CLIENT_ID=<your client id>
set TWITCH_CLIENT_SECRET=<your secret id>
```
or like this if you're using VScode on windows:
> .vscode\settings.json
```
{
    "terminal.integrated.env.windows": {
        "TWITCH_CLIENT_ID": "your client id",
        "TWITCH_CLIENT_SECRET": "your secret id"
    }
}
```

It then can be run using:
```
python3 MiSTerCT-IGDB/main.py
```

More information and functionalities coming soon since at the moment it's just a proof of concept.


# License
``MiSTerCT`` is distributed under the MIT License - see the [LICENSE](LICENSE) file for details.