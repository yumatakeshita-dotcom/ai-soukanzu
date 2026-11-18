CREATE TABLE IF NOT EXISTS mapco (slug TEXT PRIMARY KEY, name TEXT, en TEXT, note TEXT, num TEXT, people INTEGER, acq INTEGER);
CREATE TABLE IF NOT EXISTS mapco_people (slug TEXT, name TEXT, en TEXT, role TEXT, since TEXT, until TEXT, note TEXT);
CREATE TABLE IF NOT EXISTS mapco_news (slug TEXT, d TEXT, title TEXT, url TEXT, media TEXT);
CREATE TABLE IF NOT EXISTS mapco_acq (slug TEXT, year TEXT, target TEXT, amount TEXT, note TEXT);
CREATE INDEX IF NOT EXISTS i_mapco_name ON mapco(name);
CREATE INDEX IF NOT EXISTS i_mapco_num ON mapco(num);
CREATE INDEX IF NOT EXISTS i_mapco_p ON mapco_people(slug);
CREATE INDEX IF NOT EXISTS i_mapco_n ON mapco_news(slug, d);
CREATE INDEX IF NOT EXISTS i_mapco_a ON mapco_acq(slug);
