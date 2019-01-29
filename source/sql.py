# encoding: utf-8
# author: Marko Čibej
# file: sql.py
"""
A collection of SQL strings, kept separate from python and js code
for the sake of decency.
"""

upgrade_db = {
    '0.0': {
        'target-version': '0.1',
        'ddl':
            '''
            create table meta (
              id integer primary key,
              database_version text not null,
              application_version text,
              upgraded_on text,
              is_current text
            );
            
            create table works (
              id integer primary key,
              outer_id text not null,
              name text not null,
              parent integer,
              aggregate text,
              last_change text,
              json text not null,
              unique (outer_id)
            );
            
            create index works_by_outer_id on works (outer_id);
            
            create table history (
              history_work integer not null,
              tstamp text not null,
              attribute text not null,
              value text not null,
              primary key (history_work, tstamp, attribute),
              foreign key(history_work) references works(id)
            );
            
            create index history_by_work on history (history_work);
            
            create table classifiers (
              id integer primary key,
              classifier_name text not null,
              json text not null
            );
            
            create table i18n (
              language text not null,
              context text not null,
              key text not null,
              value text not null,
              primary key (language, context, key)
            );
            '''
        }
}

# housekeeping
is_initialized = '''
    select name from sqlite_master where type='table' and name='meta';
    '''
get_db_version = '''
    select max(database_version) from (
        select database_version from meta where is_current='true' 
        union select '0.0'); 
    '''
invalidate_db_version = '''
    update meta set is_current='' where is_current='true';
    '''
update_db_version = '''
    insert into meta (database_version, application_version, upgraded_on, is_current) 
        values (:db_version, :app_version, strftime('%Y-%m-%dT%H:%M:%S', 'now'), 'true');
    '''
clear_database = '''
    delete from history;
    delete from works;
    delete from classifiers;
    delete from i18n;
    '''

# works
insert_work = '''
    insert into works (name, outer_id, parent, aggregate, last_change, json) 
        values (:name, :outer_id, :parent, :aggregate, :last_change, :json);
    '''
get_works = '''
    select json from works;
    '''

# classifiers
insert_classifier = '''
    insert into classifiers (classifier_name, json) values (:name, :json);
'''
get_classifiers = '''
    select json from classifiers;
    '''

# translations
insert_translation = '''
    insert into i18n (language, context, key, value) values (:language, :context, :key, :value);
    '''
update_translation = '''
    update i18n set value=:value where language=:language and context=:context and key=:key;
    '''
delete_translation = '''
    delete from i18n where language=:language and context=:context and key=:key;
    '''
get_translation = '''
    select value from i18n where language=:language and context=:context and key=:key;
    '''
get_translations = '''
    select language, context, key, value from i18n where language like :language_pattern order by language, context;
    '''

# history
insert_history = '''
    insert into history (history_work, tstamp, attribute, value) values (:work, :tstamp, :attribute, :value);
    '''
update_history = '''
    update history set value=:value where history_work=:work and tstamp=:tstamp and attribute=:attribute;
    '''
delete_history = '''
    delete from history where history_work=:work and tstamp=:tstamp and attribute=:attribute;
    '''
get_history = '''
    select value from history where history_work=:work and tstamp=:tstamp and attribute=:attribute;
    '''
get_history_by_work = '''
    select tstamp, attribute, value from history where history_work=:work;
'''
