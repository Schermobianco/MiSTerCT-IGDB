CREATE TABLE IF NOT EXISTS "platforms" (
	"id"	INTEGER NOT NULL UNIQUE,
	"abbreviation"	TEXT,
	"alternative_name"	TEXT,
	"category"	INTEGER,
	"checksum"	TEXT,
	"created_at"	INTEGER,
	"generation"	INTEGER,
	"name"	TEXT,
	"platform_family"	INTEGER,
	"platform_logo"	INTEGER,
	"slug"	TEXT,
	"summary"	TEXT,
	"updated_at"	INTEGER,
	"url"	TEXT,
	"versions"	TEXT,
	"websites"	TEXT,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "companies" (
	"id"	INTEGER NOT NULL UNIQUE,
	"change_date"	INTEGER,
	"change_date_category"	INTEGER,
	"changed_company_id"	INTEGER,
	"checksum"	TEXT,
	"country"	INTEGER,
	"created_at"	INTEGER,
	"description"	TEXT,
	"developed"	INTEGER,
	"logo"	INTEGER,
	"name"	TEXT,
	"parent"	INTEGER,
	"published"	INTEGER,
	"slug"	TEXT,
	"start_date"	INTEGER,
	"start_date_category"	INTEGER,
	"updated_at"	INTEGER,
	"url"	TEXT,
	"websites"	INTEGER,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "genres" (
	"id"	INTEGER NOT NULL UNIQUE,
	"checksum"	TEXT,
	"created_at"	INTEGER,
	"name"	TEXT,
	"slug"	TEXT,
	"updated_at"	INTEGER,
	"url"	TEXT,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "regions" (
	"id"	INTEGER NOT NULL UNIQUE,
	"category"	TEXT,
	"checksum"	TEXT,
	"created_at"	INTEGER,
	"identifier"	TEXT,
	"name"	TEXT,
	"updated_at"	INTEGER,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "release_dates#category" (
	"name"	INTEGER,
	"value"	INTEGER NOT NULL UNIQUE,
	PRIMARY KEY("value")
);
CREATE TABLE IF NOT EXISTS "release_dates#region" (
	"name"	TEXT,
	"value"	INTEGER NOT NULL UNIQUE,
	PRIMARY KEY("value")
);
CREATE TABLE IF NOT EXISTS "games#category" (
	"name"	TEXT,
	"value"	INTEGER NOT NULL UNIQUE,
	PRIMARY KEY("value")
);
CREATE TABLE IF NOT EXISTS "games#status" (
	"name"	TEXT,
	"value"	INTEGER NOT NULL UNIQUE,
	PRIMARY KEY("value")
);
CREATE TABLE IF NOT EXISTS "companies#change_date_category" (
	"name"	TEXT,
	"value"	INTEGER NOT NULL UNIQUE,
	PRIMARY KEY("value")
);
CREATE TABLE IF NOT EXISTS "companies#start_date_category" (
	"name"	TEXT,
	"value"	INTEGER NOT NULL UNIQUE,
	PRIMARY KEY("value")
);
CREATE TABLE IF NOT EXISTS "platforms#category" (
	"name"	TEXT,
	"value"	INTEGER NOT NULL UNIQUE,
	PRIMARY KEY("value")
);
CREATE TABLE IF NOT EXISTS "country_ISO3166-1" (country_name TEXT, official_name TEXT, alpha2 TEXT, alpha3 TEXT, code INTEGER PRIMARY KEY NOT NULL UNIQUE);
CREATE TABLE franchises (id PRIMARY KEY UNIQUE NOT NULL, checksum TEXT, created_at TEXT, games INTEGER, name TEXT, slug TEXT, updated_at INTEGER, url TEXT);
CREATE TABLE game_engines (id INTEGER PRIMARY KEY UNIQUE NOT NULL, checksum TEXT, companies INTEGER, created_at INTEGER, description TEXT, logo INTEGER, name TEXT, platforms INTEGER, slug TEXT, updated_at INTEGER, url TEXT);
CREATE TABLE [games](
  [id] INTEGER PRIMARY KEY NOT NULL UNIQUE,
  [age_ratings] TEXT,
  [aggregated_rating] INTEGER,
  [aggregated_rating_count] INTEGER,
  [alternative_names] TEXT,
  [artworks] TEXT,
  [bundles] TEXT,
  [category] INTEGER,
  [checksum] TEXT,
  [collection] INTEGER,
  [cover] INTEGER,
  [created_at] INTEGER,
  [dlcs] TEXT,
  [expanded_games] TEXT,
  [expansions] TEXT,
  [external_games] TEXT,
  [first_release_date] INTEGER,
  [follows] INTEGER,
  [forks] TEXT,
  [franchise] INTEGER,
  [franchises] TEXT,
  [game_engines] TEXT,
  [game_localizations] TEXT,
  [game_modes] TEXT,
  [genres] INTEGER,
  [hypes] INTEGER,
  [involved_companies] TEXT,
  [keywords] TEXT,
  [language_supports] TEXT,
  [multiplayer_modes] TEXT,
  [name] TEXT,
  [parent_game] INTEGER,
  [platforms] TEXT,
  [player_perspectives] TEXT,
  [ports] INTEGER,
  [rating] INTEGER,
  [rating_count] INTEGER,
  [release_dates] TEXT,
  [remakes] TEXT,
  [remasters] TEXT,
  [screenshots] TEXT,
  [similar_games] TEXT,
  [slug] TEXT,
  [standalone_expansions] TEXT,
  [status] INTEGER,
  [storyline] TEXT,
  [summary] TEXT,
  [tags] TEXT,
  [themes] TEXT,
  [total_rating] INTEGER,
  [total_rating_count] INTEGER,
  [updated_at] INTEGER,
  [url] TEXT,
  [version_parent] INTEGER,
  [version_title] TEXT,
  [videos] TEXT,
  [websites] TEXT
  );
CREATE TABLE [alternative_names](
  [id] INTEGER PRIMARY KEY NOT NULL UNIQUE,
  [checksum] TEXT,
  [comment] TEXT,
  [game] INTEGER,
  [name] TEXT);
CREATE TABLE [involved_companies](
  [id] INTEGER PRIMARY KEY NOT NULL UNIQUE,
  [checksum] TEXT,
  [company] INTEGER,
  [created_at] INTEGER,
  [developer] INTEGER,
  [game] INTEGER,
  [porting] INTEGER,
  [publisher] INTEGER,
  [supporting] INTEGER,
  [updated_at] INTEGER);
CREATE TABLE [release_dates](
  [id] INTEGER PRIMARY KEY NOT NULL UNIQUE,
  [category] INTEGER,
  [checksum] TEXT,
  [created_at] INTEGER,
  [date] INTEGER,
  [game] INTEGER,
  [human] TEXT,
  [m] INTEGER,
  [platform] INTEGER,
  [region] INTEGER,
  [status] INTEGER,
  [updated_at] INTEGER,
  [y] INTEGER);
CREATE TABLE [game_modes](
  [id] INTEGER PRIMARY KEY NOT NULL UNIQUE,
  [checksum] TEXT,
  [created_at] INTEGER,
  [name] TEXT,
  [slug] TEXT,
  [updated_at] INTEGER,
  [url] TEXT);
CREATE TABLE [player_perspectives](
  [id] INTEGER PRIMARY KEY NOT NULL UNIQUE,
  [checksum] TEXT,
  [created_at] INTEGER,
  [name] TEXT,
  [slug] TEXT,
  [updated_at] INTEGER,
  [url] TEXT);
CREATE TABLE IF NOT EXISTS "collections" (
	"id"	INTEGER NOT NULL UNIQUE,
	"checksum"	TEXT,
	"created_at"	INTEGER,
	"games"	INTEGER,
	"name"	TEXT,
	"slug"	TEXT,
	"updated_at"	INTEGER,
	"url"	TEXT,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "age_ratings" (
	"id"	INTEGER NOT NULL UNIQUE,
	"category"	INTEGER,
	"checksum"	TEXT,
	"content_descriptions"	INTEGER,
	"rating"	INTEGER,
	"rating_cover_url"	TEXT,
	"synopsis"	TEXT,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "age_rating#category" (
	"name"	TEXT,
	"value"	INTEGER NOT NULL UNIQUE,
	PRIMARY KEY("value")
);
CREATE TABLE IF NOT EXISTS "age_rating#rating" (
	"name"	TEXT,
	"value"	INTEGER NOT NULL UNIQUE,
	PRIMARY KEY("value")
);
CREATE TABLE IF NOT EXISTS "game_localizations" (
	"id"	INTEGER NOT NULL UNIQUE,
	"checksum"	TEXT,
	"cover"	INTEGER,
	"created_at"	INTEGER,
	"game"	INTEGER,
	"name"	TEXT,
	"region"	INTEGER,
	"updated_at"	INTEGER,
	PRIMARY KEY("id")
);
CREATE TABLE t_agr_all(
  id INT,
  name TEXT,
  platform INT,
  platform_name TEXT,
  platform_category TEXT,
  region_name TEXT,
  date TEXT,
  collection_name,
  category_name,
  game_modes_name,
  player_perspectives_name,
  genres_name,
  franchise,
  publishers_name,
  developers_name,
  game_engines_name
);
CREATE INDEX [games_gameID] ON [games]([id]);
CREATE INDEX [alternative_names_gameID] ON [alternative_names]([game]);
CREATE INDEX [involved_companies_gameID] ON [involved_companies]([game]);
CREATE INDEX [release_dates_gameID] ON [release_dates]([game]);
CREATE VIEW v_simple_games
AS
SELECT games.id,games.name,Null as comment,platforms,games.release_dates,games.genres,games.involved_companies FROM games

UNION
SELECT alternative_names.game,alternative_names.name,alternative_names.comment,games.platforms,games.release_dates,games.genres,games.involved_companies FROM games
LEFT JOIN
alternative_names ON alternative_names.game = games.id

WHERE
alternative_names.game IS NOT NULL

ORDER BY games.id;
CREATE VIEW v_official_names
AS
SELECT games.id, games.name, platforms FROM games;
CREATE VIEW v_alternative_names
AS

SELECT alternative_names.game as 'id', alternative_names.name, alternative_names.comment, games.platforms FROM games
LEFT JOIN
alternative_names ON alternative_names.game = games.id

WHERE
alternative_names.game IS NOT NULL

ORDER BY games.id, alternative_names.id;
CREATE VIEW v_official_names_regions
AS
SELECT * FROM
(
	SELECT games.id, games.name, v_simple_releases.region, v_simple_releases.region_name, platforms FROM games

	LEFT JOIN -- RELEASES
	v_simple_releases ON v_simple_releases.id = games.id

	GROUP BY v_simple_releases.id, v_simple_releases.region
)
ORDER BY id;
CREATE VIEW v_alternative_names_regions
AS
SELECT * FROM
(
	SELECT alternative_names.game as 'id', alternative_names.name, alternative_names.comment, v_simple_releases.region, v_simple_releases.region_name, games.platforms FROM games
	LEFT JOIN
	alternative_names ON alternative_names.game = games.id

	LEFT JOIN -- RELEASES
	v_simple_releases ON v_simple_releases.id = games.id

	WHERE
	alternative_names.game IS NOT NULL

	GROUP BY v_simple_releases.id, v_simple_releases.region

	ORDER BY games.id, alternative_names.id
)
ORDER BY id;
CREATE VIEW v_complete_names
AS
SELECT id,name,comment,platforms FROM
(
	SELECT games.id, games.name, 'Official' as comment, platforms, '1' as 'ord', Null FROM games

	UNION
	SELECT alternative_names.game, alternative_names.name, alternative_names.comment, games.platforms, '2' as 'ord', alternative_names.id FROM games
	LEFT JOIN
	alternative_names ON alternative_names.game = games.id

	WHERE
	alternative_names.game IS NOT NULL

	ORDER BY games.id, ord, alternative_names.id
);
CREATE VIEW [v_agr_publishers]
AS
SELECT
       [id],
       '[' || GROUP_CONCAT ([companies], '][') || ']' AS 'publishers',
       GROUP_CONCAT ([companies_name] || CC, ', ') AS 'publishers_name'
FROM   (WITH RECURSIVE
          [split]([id], [involved_companies], [str]) AS(
            SELECT
                   [id],
                   '',
                   REPLACE (REPLACE (REPLACE ([involved_companies], '][', ','), ']', ''), '[', '') || ','
            FROM   [games]
            UNION ALL
            SELECT
                   [id],
                   SUBSTR ([str], 0, INSTR ([str], ',')),
                   SUBSTR ([str], INSTR ([str], ',') + 1)
            FROM   [split]
            WHERE  [str] != ''
          )
        SELECT
               [split].[id],
               [split].[involved_companies],
               [involved_companies].[company] AS 'companies',
               [companies].[name] AS 'companies_name',
			   IFNULL(' (' || [country_ISO3166-1].[alpha2] || ')','') AS 'CC'
        FROM   [split]
               LEFT JOIN [involved_companies] ON [involved_companies].[id] = [split].[involved_companies]
               LEFT JOIN [companies] ON [companies].[id] = [involved_companies].[company]
               LEFT JOIN [country_ISO3166-1] ON [country_ISO3166-1].[code] = [companies].[country]
        WHERE  [involved_companies].[publisher] = 1) t
GROUP  BY [id];
CREATE VIEW [v_agr_developers]
AS
SELECT
       [id],
       '[' || GROUP_CONCAT ([companies], '][') || ']' AS 'developers',
       GROUP_CONCAT ([companies_name] || CC, ', ') AS 'developers_name'
FROM
(
	WITH RECURSIVE
	  [split]([id], [involved_companies], [str]) AS(
		SELECT
			   [id],
			   '',
			   REPLACE (REPLACE (REPLACE ([involved_companies], '][', ','), ']', ''), '[', '') || ','
		FROM   [games]
		UNION ALL
		SELECT
			   [id],
			   SUBSTR ([str], 0, INSTR ([str], ',')),
			   SUBSTR ([str], INSTR ([str], ',') + 1)
		FROM   [split]
		WHERE  [str] != ''
     )
        SELECT
               [split].[id],
               [split].[involved_companies],
               [involved_companies].[company] AS 'companies',
               [companies].[name] AS 'companies_name',
			   IFNULL(' (' || [country_ISO3166-1].[alpha2] || ')','') AS 'CC'
        FROM   [split]
               LEFT JOIN [involved_companies] ON [involved_companies].[id] = [split].[involved_companies]
               LEFT JOIN [companies] ON [companies].[id] = [involved_companies].[company]
               LEFT JOIN [country_ISO3166-1] ON [country_ISO3166-1].[code] = [companies].[country]
        WHERE  [involved_companies].[developer] = 1
) t
GROUP  BY [id];
CREATE VIEW [v_simple_publishers]
AS
WITH RECURSIVE
  [split]([id], [involved_companies], [str]) AS(
	SELECT
		   [id],
		   '',
		   REPLACE (REPLACE (REPLACE ([involved_companies], '][', ','), ']', ''), '[', '') || ','
	FROM   [games]
	UNION ALL
	SELECT
		   [id],
		   SUBSTR ([str], 0, INSTR ([str], ',')),
		   SUBSTR ([str], INSTR ([str], ',') + 1)
	FROM   [split]
	WHERE  [str] != ''
  )
SELECT
	   [split].[id],
	   [split].[involved_companies],
	   [involved_companies].[company] AS 'companies',
	   [companies].[name] AS 'companies_name',
	   IFNULL(' (' || [country_ISO3166-1].[alpha2] || ')','') AS 'CC'
FROM   [split]
	   LEFT JOIN [involved_companies] ON [involved_companies].[id] = [split].[involved_companies]
	   LEFT JOIN [companies] ON [companies].[id] = [involved_companies].[company]
	   LEFT JOIN [country_ISO3166-1] ON [country_ISO3166-1].[code] = [companies].[country]
WHERE  [involved_companies].[publisher] = 1

ORDER by split.id;
CREATE VIEW [v_simple_developers]
AS

WITH RECURSIVE
  [split]([id], [involved_companies], [str]) AS(
	SELECT
		   [id],
		   '',
		   REPLACE (REPLACE (REPLACE ([involved_companies], '][', ','), ']', ''), '[', '') || ','
	FROM   [games]
	UNION ALL
	SELECT
		   [id],
		   SUBSTR ([str], 0, INSTR ([str], ',')),
		   SUBSTR ([str], INSTR ([str], ',') + 1)
	FROM   [split]
	WHERE  [str] != ''
 )
	SELECT
		   [split].[id],
		   [split].[involved_companies],
		   [involved_companies].[company] AS 'companies',
		   [companies].[name] AS 'companies_name',
		   IFNULL(' (' || [country_ISO3166-1].[alpha2] || ')','') AS 'CC'
	FROM   [split]
		   LEFT JOIN [involved_companies] ON [involved_companies].[id] = [split].[involved_companies]
		   LEFT JOIN [companies] ON [companies].[id] = [involved_companies].[company]
		   LEFT JOIN [country_ISO3166-1] ON [country_ISO3166-1].[code] = [companies].[country]
	WHERE  [involved_companies].[developer] = 1
ORDER by split.id;
CREATE VIEW v_agr_genres
AS
SELECT id, '['||group_concat(genres, '][')||']' AS 'genres', group_concat(genres_name, ', ') AS 'genres_name' FROM
(
	WITH RECURSIVE split(id, genres, str) AS (
		SELECT id, '',
		REPLACE(REPLACE(REPLACE(genres,'][',','),']',''),'[','')||',' FROM games
		UNION ALL SELECT
		id,
		substr(str, 0, instr(str, ',')),
		substr(str, instr(str, ',')+1)
		FROM split WHERE str!=''
	)
	SELECT split.id, split.genres, genres.name as 'genres_name'
	FROM split

	JOIN
	genres ON genres.id = split.genres

) t
GROUP BY id;
CREATE VIEW v_simple_genres
AS

	WITH RECURSIVE split(id, genres, str) AS (
		SELECT id, '',
		REPLACE(REPLACE(REPLACE(genres,'][',','),']',''),'[','')||',' FROM games
		UNION ALL SELECT
		id,
		substr(str, 0, instr(str, ',')),
		substr(str, instr(str, ',')+1)
		FROM split WHERE str!=''
	)
	SELECT split.id, split.genres, genres.name as 'genres_name'
	FROM split

	JOIN
	genres ON genres.id = split.genres

ORDER by split.id;
CREATE VIEW [v_agr_player_perspectives]
AS
SELECT
       [id],
       '[' || GROUP_CONCAT ([player_perspectives], '][') || ']' AS 'player_perspectives',
       GROUP_CONCAT ([player_perspectives_name], ', ') AS 'player_perspectives_name'
FROM   (WITH RECURSIVE
          [split]([id], [player_perspectives], [str]) AS(
            SELECT
                   [id],
                   '',
                   REPLACE (REPLACE (REPLACE ([player_perspectives], '][', ','), ']', ''), '[', '') || ','
            FROM   [games]
            UNION ALL
            SELECT
                   [id],
                   SUBSTR ([str], 0, INSTR ([str], ',')),
                   SUBSTR ([str], INSTR ([str], ',') + 1)
            FROM   [split]
            WHERE  [str] != ''
          )
        SELECT
               [split].[id],
               [split].[player_perspectives],
               [player_perspectives].[name] AS 'player_perspectives_name'
        FROM   [split]
               JOIN [player_perspectives] ON [player_perspectives].[id] = [split].[player_perspectives]) t
GROUP  BY [id];
CREATE VIEW [v_simple_player_perspectives]
AS
WITH RECURSIVE
  [split]([id], [player_perspectives], [str]) AS(
	SELECT
		   [id],
		   '',
		   REPLACE (REPLACE (REPLACE ([player_perspectives], '][', ','), ']', ''), '[', '') || ','
	FROM   [games]
	UNION ALL
	SELECT
		   [id],
		   SUBSTR ([str], 0, INSTR ([str], ',')),
		   SUBSTR ([str], INSTR ([str], ',') + 1)
	FROM   [split]
	WHERE  [str] != ''
  )
SELECT
	   [split].[id],
	   [split].[player_perspectives],
	   [player_perspectives].[name] AS 'player_perspectives_name'
FROM   [split]
	   JOIN [player_perspectives] ON [player_perspectives].[id] = [split].[player_perspectives]
ORDER BY split.id;
CREATE VIEW [v_agr_game_modes]
AS
SELECT
       [id],
       '[' || GROUP_CONCAT ([game_modes], '][') || ']' AS [game_modes],
       GROUP_CONCAT ([game_modes_name], ', ') AS [game_modes_name]
FROM   (WITH RECURSIVE
          [split]([id], [game_modes], [str]) AS(
            SELECT
                   [id],
                   '',
                   REPLACE (REPLACE (REPLACE ([game_modes], '][', ','), ']', ''), '[', '') || ','
            FROM   [games]
            UNION ALL
            SELECT
                   [id],
                   SUBSTR ([str], 0, INSTR ([str], ',')),
                   SUBSTR ([str], INSTR ([str], ',') + 1)
            FROM   [split]
            WHERE  [str] != ''
          )
        SELECT
               [split].[id],
               [split].[game_modes],
               [game_modes].[name] AS [game_modes_name]
        FROM   [split]
               JOIN [game_modes] ON [game_modes].[id] = [split].[game_modes]) t
GROUP  BY [id];
CREATE VIEW [v_simple_game_modes]
AS
WITH RECURSIVE
  [split]([id], [game_modes], [str]) AS(
	SELECT
		   [id],
		   '',
		   REPLACE (REPLACE (REPLACE ([game_modes], '][', ','), ']', ''), '[', '') || ','
	FROM   [games]
	UNION ALL
	SELECT
		   [id],
		   SUBSTR ([str], 0, INSTR ([str], ',')),
		   SUBSTR ([str], INSTR ([str], ',') + 1)
	FROM   [split]
	WHERE  [str] != ''
  )
SELECT
	   [split].[id],
	   [split].[game_modes],
	   [game_modes].[name] AS [game_modes_name]
FROM   [split]
	   JOIN [game_modes] ON [game_modes].[id] = [split].[game_modes]
ORDER BY split.id;
CREATE VIEW v_agr_game_engines AS SELECT id,
           '[' || group_concat(game_engines, '][') || ']' AS game_engines,
           group_concat(game_engines_name, ', ') AS game_engines_name
      FROM (
           WITH RECURSIVE split (
                   id,
                   game_engines,
                   str
               )
               AS (
                   SELECT id,
                          '',
                          REPLACE(REPLACE(REPLACE(game_engines, '][', ','), ']', ''), '[', '') || ','
                     FROM games
                   UNION ALL
                   SELECT id,
                          substr(str, 0, instr(str, ',') ),
                          substr(str, instr(str, ',') + 1)
                     FROM split
                    WHERE str != ''
               )
               SELECT split.id,
                      split.game_engines,
                      game_engines.name AS game_engines_name
                 FROM split
                      JOIN
                      game_engines ON game_engines.id = split.game_engines
           )
           t
     GROUP BY id;
CREATE VIEW v_simple_game_engines AS
WITH RECURSIVE split (
	   id,
	   game_engines,
	   str
   )
   AS (
	   SELECT id,
			  '',
			  REPLACE(REPLACE(REPLACE(game_engines, '][', ','), ']', ''), '[', '') || ','
		 FROM games
	   UNION ALL
	   SELECT id,
			  substr(str, 0, instr(str, ',') ),
			  substr(str, instr(str, ',') + 1)
		 FROM split
		WHERE str != ''
   )
   SELECT split.id,
		  split.game_engines,
		  game_engines.name AS game_engines_name
	 FROM split
		  JOIN
		  game_engines ON game_engines.id = split.game_engines
ORDER by split.id;
CREATE VIEW [v_agr_all]
AS
SELECT
       [games].[id],
       [games].[name],
       [v_simple_releases].[platform],
       [platforms].[name] AS 'platform_name',
       [platforms#category].[name] AS 'platform_category',
       --[v_simple_releases].[region],
       [v_simple_releases].[region_name],
       --[v_simple_releases].[release_dates],
       [v_simple_releases].[date],
	   --IFNULL ([collections].[id], '') AS 'collection',
       IFNULL ([collections].[name], '') AS 'collection_name',
       --[games].[category] AS 'category',
       IFNULL ([games#category].[name], '') AS 'category_name',
       --[v_agr_game_modes].[game_modes],
       [v_agr_game_modes].[game_modes_name],
       --[v_agr_player_perspectives].[player_perspectives],
       [v_agr_player_perspectives].[player_perspectives_name],
       --[v_agr_genres].[genres],
       [v_agr_genres].[genres_name],
       IFNULL ([franchises].[name], '') AS 'franchise',
       --[v_agr_publishers].[publishers],
       [v_agr_publishers].[publishers_name],
       --[v_agr_developers].[developers],
       [v_agr_developers].[developers_name],
       --IFNULL ([v_agr_game_engines].[game_engines], '') AS 'game_engines',
       IFNULL ([v_agr_game_engines].[game_engines_name], '') AS 'game_engines_name'
FROM   [games]
       LEFT JOIN [v_simple_releases] ON [v_simple_releases].[id] = [games].[id]
	   LEFT JOIN [collections] ON [collections].[id] = [games].[collection]
       LEFT JOIN [games#category] ON [games#category].[value] = [games].[category]
       LEFT JOIN [v_agr_game_modes] ON [v_agr_game_modes].[id] = [games].[id]
       LEFT JOIN [v_agr_player_perspectives] ON [v_agr_player_perspectives].[id] = [games].[id]
       LEFT JOIN [v_agr_genres] ON [v_agr_genres].[id] = [games].[id]
       LEFT JOIN [franchises] ON [franchises].[id] = [games].[franchise]
       LEFT JOIN [platforms] ON [platforms].[id] = [v_simple_releases].[platform]
       LEFT JOIN [platforms#category] ON [platforms#category].[value] = [platforms].[category]
       LEFT JOIN [v_agr_publishers] ON [v_agr_publishers].[id] = [games].[id]
       LEFT JOIN [v_agr_developers] ON [v_agr_developers].[id] = [games].[id]
       LEFT JOIN [v_agr_game_engines] ON [v_agr_game_engines].[id] = [games].[id];
CREATE VIEW v_simple_releases AS
SELECT
    games_table.id AS 'id',
    json_each.value AS 'release_dates',
    reldates_table.human AS 'date',
    reldates_table.region AS 'region',
    region_table.name AS 'name',
    reldates_table.platform AS 'platform'
FROM
    games AS 'games_table',
    json_each(games_table.release_dates)
    JOIN release_dates AS 'reldates_table' ON reldates_table.id = json_each.value
    LEFT JOIN [release_dates#region] AS 'region_table' ON reldates_table.region = region_table.value
    LEFT JOIN platforms AS 'platforms_table' ON reldates_table.platform = platforms_table.id
ORDER BY
    id;
/* No STAT tables available */
