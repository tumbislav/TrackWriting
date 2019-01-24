-- Just a helper file for developing SQL statements. It is never
-- accessed directly, statements have to be copied into appropriate python strings

create table meta (
  id integer primary key,
  database_version text,
  system_version text,
  upgraded_on text,
  last_saved text,
  is_current text
);

insert into meta (database_version, system_version) values ('0.0');

create table works (
  id integer primary key,
  name text not null,
  level text not null,   -- collection, work, version or part
  parent integer,        -- when
  json text not null
);

create table history (
  id integer primary key,
  history_work integer not null,
  value_type text,
  timestamp text,
  value text,
  foreign key(history_work) references works(id)
);

create table collections (

);