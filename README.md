# MiSTerCT-IGDB

Classification tool for MiSTer cores based on IGDB data.

The tool is still in development and not ready for use however it will allow you to have organized roms in folder and filenames based on IGDB data.

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

It then can be run using:
```
python3 MiSTerCT-IGDB/main.py
```

More information and functionalities coming soon since at the moment it's just a proof of concept.
