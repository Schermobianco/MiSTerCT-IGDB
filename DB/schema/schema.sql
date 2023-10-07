CREATE TABLE IF NOT EXISTS [platforms] (
  "id" INTEGER NOT NULL UNIQUE,
  "abbreviation" TEXT,
  "alternative_name" TEXT,
  "category" INTEGER,
  "checksum" TEXT,
  "created_at" INTEGER,
  "generation" INTEGER,
  "name" TEXT,
  "platform_family" INTEGER,
  "platform_logo" INTEGER,
  "slug" TEXT,
  "summary" TEXT,
  "updated_at" INTEGER,
  "url" TEXT,
  "versions" TEXT,
  "websites" TEXT,
  PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS [companies] (
  "id" INTEGER NOT NULL UNIQUE,
  "change_date" INTEGER,
  "change_date_category" INTEGER,
  "changed_company_id" INTEGER,
  "checksum" TEXT,
  "country" INTEGER,
  "created_at" INTEGER,
  "description" TEXT,
  "developed" INTEGER,
  "logo" INTEGER,
  "name" TEXT,
  "parent" INTEGER,
  "published" INTEGER,
  "slug" TEXT,
  "start_date" INTEGER,
  "start_date_category" INTEGER,
  "updated_at" INTEGER,
  "url" TEXT,
  "websites" INTEGER,
  PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS [genres] (
  "id" INTEGER NOT NULL UNIQUE,
  "checksum" TEXT,
  "created_at" INTEGER,
  "name" TEXT,
  "slug" TEXT,
  "updated_at" INTEGER,
  "url" TEXT,
  PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS [regions] (
  "id" INTEGER NOT NULL UNIQUE,
  "category" TEXT,
  "checksum" TEXT,
  "created_at" INTEGER,
  "identifier" TEXT,
  "name" TEXT,
  "updated_at" INTEGER,
  PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS [release_dates#category] (
  "name" INTEGER,
  "value" INTEGER NOT NULL UNIQUE,
  PRIMARY KEY("value")
);

CREATE TABLE IF NOT EXISTS [release_dates#region] (
  "name" TEXT,
  "value" INTEGER NOT NULL UNIQUE,
  PRIMARY KEY("value")
);

CREATE TABLE IF NOT EXISTS [games#category] (
  "name" TEXT,
  "value" INTEGER NOT NULL UNIQUE,
  PRIMARY KEY("value")
);

CREATE TABLE IF NOT EXISTS [games#status] (
  "name" TEXT,
  "value" INTEGER NOT NULL UNIQUE,
  PRIMARY KEY("value")
);

CREATE TABLE IF NOT EXISTS [companies#change_date_category] (
  "name" TEXT,
  "value" INTEGER NOT NULL UNIQUE,
  PRIMARY KEY("value")
);

CREATE TABLE IF NOT EXISTS [companies#start_date_category] (
  "name" TEXT,
  "value" INTEGER NOT NULL UNIQUE,
  PRIMARY KEY("value")
);

CREATE TABLE IF NOT EXISTS [platforms#category] (
  "name" TEXT,
  "value" INTEGER NOT NULL UNIQUE,
  PRIMARY KEY("value")
);

CREATE TABLE IF NOT EXISTS [country_ISO3166-1] (
  country_name TEXT,
  official_name TEXT,
  alpha2 TEXT,
  alpha3 TEXT,
  code INTEGER PRIMARY KEY NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS [franchises] (
  id PRIMARY KEY UNIQUE NOT NULL,
  checksum TEXT,
  created_at TEXT,
  games INTEGER,
  name TEXT,
  slug TEXT,
  updated_at INTEGER,
  url TEXT
);

CREATE TABLE IF NOT EXISTS [game_engines] (
  id INTEGER PRIMARY KEY UNIQUE NOT NULL,
  checksum TEXT,
  companies INTEGER,
  created_at INTEGER,
  description TEXT,
  logo INTEGER,
  name TEXT,
  platforms INTEGER,
  slug TEXT,
  updated_at INTEGER,
  url TEXT
);

CREATE TABLE IF NOT EXISTS [games](
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

CREATE TABLE IF NOT EXISTS [alternative_names](
  [id] INTEGER PRIMARY KEY NOT NULL UNIQUE,
  [checksum] TEXT,
  [comment] TEXT,
  [game] INTEGER,
  [name] TEXT
);

CREATE TABLE IF NOT EXISTS [involved_companies](
  [id] INTEGER PRIMARY KEY NOT NULL UNIQUE,
  [checksum] TEXT,
  [company] INTEGER,
  [created_at] INTEGER,
  [developer] INTEGER,
  [game] INTEGER,
  [porting] INTEGER,
  [publisher] INTEGER,
  [supporting] INTEGER,
  [updated_at] INTEGER
);

CREATE TABLE IF NOT EXISTS [release_dates](
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
  [y] INTEGER
);

CREATE TABLE IF NOT EXISTS [game_modes](
  [id] INTEGER PRIMARY KEY NOT NULL UNIQUE,
  [checksum] TEXT,
  [created_at] INTEGER,
  [name] TEXT,
  [slug] TEXT,
  [updated_at] INTEGER,
  [url] TEXT
);

CREATE TABLE IF NOT EXISTS [player_perspectives](
  [id] INTEGER PRIMARY KEY NOT NULL UNIQUE,
  [checksum] TEXT,
  [created_at] INTEGER,
  [name] TEXT,
  [slug] TEXT,
  [updated_at] INTEGER,
  [url] TEXT
);

CREATE TABLE IF NOT EXISTS [collections] (
  "id" INTEGER NOT NULL UNIQUE,
  "checksum" TEXT,
  "created_at" INTEGER,
  "games" INTEGER,
  "name" TEXT,
  "slug" TEXT,
  "updated_at" INTEGER,
  "url" TEXT,
  PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS [age_ratings] (
  "id" INTEGER NOT NULL UNIQUE,
  "category" INTEGER,
  "checksum" TEXT,
  "content_descriptions" INTEGER,
  "rating" INTEGER,
  "rating_cover_url" TEXT,
  "synopsis" TEXT,
  PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS [age_rating#category] (
  "name" TEXT,
  "value" INTEGER NOT NULL UNIQUE,
  PRIMARY KEY("value")
);

CREATE TABLE IF NOT EXISTS [age_rating#rating] (
  "name" TEXT,
  "value" INTEGER NOT NULL UNIQUE,
  PRIMARY KEY("value")
);

CREATE TABLE IF NOT EXISTS [game_localizations] (
  "id" INTEGER NOT NULL UNIQUE,
  "checksum" TEXT,
  "cover" INTEGER,
  "created_at" INTEGER,
  "game" INTEGER,
  "name" TEXT,
  "region" INTEGER,
  "updated_at" INTEGER,
  PRIMARY KEY("id")
);

DROP VIEW IF EXISTS [v_simple_games];

CREATE VIEW [v_simple_games] AS
SELECT
  games.id,
  games.name,
  Null as comment,
  platforms,
  games.release_dates,
  games.genres,
  games.involved_companies
FROM
  games
UNION
SELECT
  alternative_names.game,
  alternative_names.name,
  alternative_names.comment,
  games.platforms,
  games.release_dates,
  games.genres,
  games.involved_companies
FROM
  games
  LEFT JOIN alternative_names ON alternative_names.game = games.id
WHERE
  alternative_names.game IS NOT NULL
ORDER BY
  games.id;

DROP VIEW IF EXISTS [v_official_names];

CREATE VIEW [v_official_names] AS
SELECT
  games.id,
  games.name,
  platforms
FROM
  games;

DROP VIEW IF EXISTS [v_alternative_names];

CREATE VIEW [v_alternative_names] AS
SELECT
  alternative_names.game as 'id',
  alternative_names.name,
  alternative_names.comment,
  games.platforms
FROM
  games
  LEFT JOIN alternative_names ON alternative_names.game = games.id
WHERE
  alternative_names.game IS NOT NULL
ORDER BY
  games.id,
  alternative_names.id;

DROP VIEW IF EXISTS [v_official_names_regions];

CREATE VIEW [v_official_names_regions] AS
SELECT
  *
FROM
  (
    SELECT
      games.id,
      games.name,
      v_simple_releases.region,
      v_simple_releases.region_name,
      platforms
    FROM
      games
      LEFT JOIN -- RELEASES
      v_simple_releases ON v_simple_releases.id = games.id
    GROUP BY
      v_simple_releases.id,
      v_simple_releases.region
  )
ORDER BY
  id;

DROP VIEW IF EXISTS [v_alternative_names_regions];

CREATE VIEW [v_alternative_names_regions] AS
SELECT
  *
FROM
  (
    SELECT
      alternative_names.game as 'id',
      alternative_names.name,
      alternative_names.comment,
      v_simple_releases.region,
      v_simple_releases.region_name,
      games.platforms
    FROM
      games
      LEFT JOIN alternative_names ON alternative_names.game = games.id
      LEFT JOIN -- RELEASES
      v_simple_releases ON v_simple_releases.id = games.id
    WHERE
      alternative_names.game IS NOT NULL
    GROUP BY
      v_simple_releases.id,
      v_simple_releases.region
    ORDER BY
      games.id,
      alternative_names.id
  )
ORDER BY
  id;

DROP VIEW IF EXISTS [v_complete_names];

CREATE VIEW [v_complete_names] AS
SELECT
  id,
  name,
  comment,
  platforms
FROM
  (
    SELECT
      games.id,
      games.name,
      'Official' as comment,
      platforms,
      '1' as 'ord',
      Null
    FROM
      games
    UNION
    SELECT
      alternative_names.game,
      alternative_names.name,
      alternative_names.comment,
      games.platforms,
      '2' as 'ord',
      alternative_names.id
    FROM
      games
      LEFT JOIN alternative_names ON alternative_names.game = games.id
    WHERE
      alternative_names.game IS NOT NULL
    ORDER BY
      games.id,
      ord,
      alternative_names.id
  );

DROP VIEW IF EXISTS [v_simple_releases];

CREATE VIEW [v_simple_releases] AS
WITH wdates AS (
  SELECT
    reldates_table.id AS 'id',
    reldates_table.region AS 'region' ,
    reldates_table.human AS 'human',
    reldates_table.platform AS 'platform',
    region_table.name AS 'region_name'
  FROM
    release_dates AS 'reldates_table'
  LEFT join [release_dates#region] AS 'region_table' ON reldates_table.region = region_table.value
  LEFT JOIN platforms AS 'platforms_table' ON reldates_table.platform = platforms_table.id
)
SELECT
  games.id,
  jj.value AS 'release_dates',
  wdates.human AS 'date',
  wdates.region AS 'region',
  wdates.region_name AS 'region_name',
  wdates.platform AS 'platform'
FROM
  games AS 'games',
  json_each(games.release_dates) AS 'jj'
LEFT JOIN wdates ON wdates.id = jj.value
ORDER BY
  games.id;


SELECT
  games_table.id AS 'id',
  jj AS 'release_dates',
  reldates_table.human AS 'date',
  reldates_table.region AS 'region',
  region_table.name AS 'region_name',
  reldates_table.platform AS 'platform'
FROM
  games AS 'games_table',
  json_each(games_table.release_dates) AS 'jj'
  JOIN release_dates AS 'reldates_table' ON reldates_table.id = jj
  LEFT JOIN [release_dates#region] AS 'region_table' ON reldates_table.region = region_table.value
  LEFT JOIN platforms AS 'platforms_table' ON reldates_table.platform = platforms_table.id
ORDER BY
  id;

DROP VIEW IF EXISTS [v_agr_publishers];

CREATE VIEW [v_agr_publishers] AS
WITH wcompanies AS (
	SELECT
    ic.id AS 'iid',
		ic.company AS 'cid',
		c.name AS 'name',
		isocode.alpha2 AS 'alpha2'
	FROM
		involved_companies AS 'ic'
		LEFT JOIN 'companies' AS 'c' on ic.company = c.id
		LEFT JOIN [country_ISO3166-1] AS 'isocode' ON isocode.code = c.country
	WHERE
		ic.publisher = 1
)
SELECT
	games.id AS 'id',
	JSON('[' || GROUP_CONCAT(wcompanies.cid) || ']') AS 'publishers',
	GROUP_CONCAT(
		wcompanies.name || COALESCE(' (' || wcompanies.alpha2 || ')', ''),
		', '
	) AS 'publishers_name'
FROM
	games AS 'games',
	json_each(games.involved_companies) AS 'jj'
	LEFT JOIN wcompanies on wcompanies.iid = jj.value
GROUP BY
	games.id;

DROP VIEW IF EXISTS [v_agr_developers];

CREATE VIEW [v_agr_developers] AS
WITH wcompanies AS (
	SELECT
    ic.id AS 'iid',
		ic.company AS 'cid',
		c.name AS 'name',
		isocode.alpha2 AS 'alpha2'
	FROM
		involved_companies AS 'ic'
		LEFT JOIN 'companies' AS 'c' on ic.company = c.id
		LEFT JOIN [country_ISO3166-1] AS 'isocode' ON isocode.code = c.country
	WHERE
		ic.developer = 1
)
SELECT
	games.id AS 'id',
	JSON('[' || GROUP_CONCAT(wcompanies.cid) || ']') AS 'developers',
	GROUP_CONCAT(
		wcompanies.name || COALESCE(' (' || wcompanies.alpha2 || ')', ''),
		', '
	) AS 'developers_name'
FROM
	games AS 'games',
	json_each(games.involved_companies) AS 'jj'
	LEFT JOIN wcompanies on wcompanies.iid = jj.value
GROUP BY
	games.id;

DROP VIEW IF EXISTS [v_simple_publishers];

CREATE VIEW [v_simple_publishers] AS
SELECT
  games_table.id AS 'id',
  json_each.value AS 'involved_companies',
  companies_table.id AS 'companies',
  companies_table.name AS 'companies_name',
  IFNULL(country_table.alpha2, '') AS 'CC'
FROM
  games AS 'games_table',
  json_each(games_table.involved_companies)
  LEFT JOIN involved_companies AS 'involved_companies_table' ON involved_companies_table.id = json_each.value
  LEFT JOIN companies AS 'companies_table' ON companies_table.id = involved_companies_table.company
  LEFT JOIN [country_ISO3166-1] as 'country_table' ON country_table.code = companies_table.country
WHERE
  involved_companies_table.publisher = 1
ORDER BY
  games_table.id;

DROP VIEW IF EXISTS [v_simple_developers];

CREATE VIEW [v_simple_developers] AS
SELECT
  games_table.id AS 'id',
  json_each.value AS 'involved_companies',
  companies_table.id AS 'companies',
  companies_table.name AS 'companies_name',
  IFNULL('(' || country_table.alpha2 || ')', '') AS 'CC'
FROM
  games AS 'games_table',
  json_each(games_table.involved_companies)
  LEFT JOIN involved_companies AS 'involved_companies_table' ON involved_companies_table.id = json_each.value
  LEFT JOIN companies AS 'companies_table' ON companies_table.id = involved_companies_table.company
  LEFT JOIN [country_ISO3166-1] as 'country_table' ON country_table.code = companies_table.country
WHERE
  involved_companies_table.developer = 1
ORDER BY
  games_table.id;

DROP VIEW IF EXISTS [v_agr_genres];

CREATE VIEW [v_agr_genres] AS
SELECT
  g.id AS 'id',
  g.genres AS 'genres',
  GROUP_CONCAT(gen.name, ', ') AS 'genres_name'
FROM
  games AS g,
  json_each(g.genres) AS jj
  LEFT JOIN genres AS gen ON gen.id = jj.value
GROUP BY
  g.id;

DROP VIEW IF EXISTS [v_simple_genres];

CREATE VIEW [v_simple_genres] AS
SELECT
  games_table.id AS 'id',
  json_each.value AS 'genres',
  genres_table.name AS 'player_perspectives_name'
FROM
  games AS 'games_table',
  json_each(games_table.genres)
  LEFT JOIN genres AS 'genres_table' ON genres_table.id = json_each.value
ORDER BY
  games_table.id;

DROP VIEW IF EXISTS [v_agr_player_perspectives];

CREATE VIEW [v_agr_player_perspectives] AS
SELECT
  g.id AS 'id',
  g.player_perspectives AS 'player_perspectives',
  GROUP_CONCAT(p.name, ', ') AS 'player_perspectives_name'
FROM
  games AS g,
  json_each(g.player_perspectives) AS jj
  LEFT JOIN player_perspectives AS p ON p.id = jj.value
GROUP BY
  g.id;

DROP VIEW IF EXISTS [v_simple_player_perspectives];

CREATE VIEW [v_simple_player_perspectives] AS
SELECT
  games_table.id AS 'id',
  json_each.value AS 'player_perspectives',
  player_perspectives_table.name AS 'player_perspectives_name'
FROM
  games AS 'games_table',
  json_each(games_table.player_perspectives)
  LEFT JOIN player_perspectives AS 'player_perspectives_table' ON player_perspectives_table.id = json_each.value
ORDER BY
  games_table.id;

DROP VIEW IF EXISTS [v_agr_game_modes];

CREATE VIEW [v_agr_game_modes] AS
SELECT
  g.id AS 'id',
  g.game_modes AS 'game_modes',
  GROUP_CONCAT(gm.name, ', ') AS 'game_modes_name'
FROM
  games AS 'g',
  json_each(g.game_modes) AS jj
  JOIN game_modes AS gm ON gm.id = jj.value
GROUP BY
  g.id;

DROP VIEW IF EXISTS [v_simple_game_modes];

CREATE VIEW [v_simple_game_modes] AS
SELECT
  games_table.id AS 'id',
  json_each.value AS 'game_modes',
  game_modes_table.name AS 'game_modes_name'
FROM
  games AS 'games_table',
  json_each(games_table.game_modes)
  JOIN game_modes AS 'game_modes_table' ON game_modes_table.id = json_each.value
ORDER BY
  games_table.id;

DROP VIEW IF EXISTS [v_agr_game_engines];

CREATE VIEW [v_agr_game_engines] AS
SELECT
  g.id AS 'id',
  g.game_engines AS 'game_engines',
  GROUP_CONCAT(ge.name, ', ') as 'game_engines_name'
FROM
  games AS g,
  json_each(g.game_engines) as jj
  JOIN game_engines AS ge ON ge.id = jj.value
GROUP BY
  g.id;

DROP VIEW IF EXISTS [v_simple_game_engines];

CREATE VIEW [v_simple_game_engines] AS
SELECT
  games_table.id AS 'id',
  json_each.value AS 'game_engines',
  game_engines_table.name AS 'game_engines_name'
FROM
  games AS 'games_table',
  json_each(games_table.game_engines)
  JOIN game_engines AS 'game_engines_table' ON game_engines_table.id = json_each.value
ORDER BY
  games_table.id;

DROP VIEW IF EXISTS [v_agr_all];

CREATE VIEW [v_agr_all] AS
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
FROM
  [games]
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

DROP VIEW IF EXISTS [t_agr_all];

CREATE VIEW t_agr_all AS
SELECT
  *
FROM
  v_agr_all
WHERE
  platform in (
    SELECT
      id
    from
      "platforms#selected"
  );


CREATE INDEX IF NOT EXISTS [idx_alternative_names_game] ON [alternative_names]([game]);
CREATE INDEX IF NOT EXISTS [idx_games_id] ON [games]([id]);
CREATE INDEX IF NOT EXISTS [idx_age_rating#category_value] ON [age_rating#category]([value]);
CREATE INDEX IF NOT EXISTS [idx_age_rating#rating_value] ON [age_rating#rating]([value]);
CREATE INDEX IF NOT EXISTS [idx_age_ratings_id] ON [age_ratings]([id]);
CREATE INDEX IF NOT EXISTS [idx_alternative_names_game] ON [alternative_names]([game]);
CREATE INDEX IF NOT EXISTS [idx_alternative_names_id] ON [alternative_names]([id]);
CREATE INDEX IF NOT EXISTS [idx_alternative_names_idgame] ON [alternative_names]([id], [game]);
CREATE INDEX IF NOT EXISTS [idx_collections_id] ON [collections]([id]);
CREATE INDEX IF NOT EXISTS [idx_collections_idname] ON [collections]([id], [name]);
CREATE INDEX IF NOT EXISTS [idx_collections_name] ON [collections]([name]);
CREATE INDEX IF NOT EXISTS [idx_companies_country] ON [companies]([country]);
CREATE INDEX IF NOT EXISTS [idx_companies_developed] ON [companies]([developed]);
CREATE INDEX IF NOT EXISTS [idx_companies_id] ON [companies]([id]);
CREATE INDEX IF NOT EXISTS [idx_companies_published] ON [companies]([published]);
CREATE INDEX IF NOT EXISTS [idx_franchises_games] ON [franchises]([games]);
CREATE INDEX IF NOT EXISTS [idx_franchises_id] ON [franchises]([id]);
CREATE INDEX IF NOT EXISTS [idx_game_engines_id] ON [game_engines]([id]);
CREATE INDEX IF NOT EXISTS [idx_game_engines_platform] ON [game_engines]([platforms]);
CREATE INDEX IF NOT EXISTS [idx_game_localizations_id] ON [game_localizations]([id]);
CREATE INDEX IF NOT EXISTS [idx_game_localizations_platform] ON [game_localizations]([game]);
CREATE INDEX IF NOT EXISTS [idx_involved_companies_company] ON [involved_companies]([company]);
CREATE INDEX IF NOT EXISTS [idx_involved_companies_developer] ON [involved_companies]([developer]);
CREATE INDEX IF NOT EXISTS [idx_involved_companies_id] ON [involved_companies]([id]);
CREATE INDEX IF NOT EXISTS [idx_involved_companies_publisher] ON [involved_companies]([publisher]);
CREATE INDEX IF NOT EXISTS [idx_release_dates_game] ON [release_dates]([game]);
CREATE INDEX IF NOT EXISTS [idx_release_dates_id] ON [release_dates]([id]);
CREATE INDEX IF NOT EXISTS [involved_companies_gameID] ON [involved_companies]([game]);
CREATE INDEX IF NOT EXISTS [release_dates_gameID] ON [release_dates]([game]);
/* No STAT tables available */
