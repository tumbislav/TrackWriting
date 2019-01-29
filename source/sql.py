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
              id integer primary key,  -- ROWID
              code text not null,      -- the id that the UI uses
              name text not null,
              parent integer,
              json text not null
            );
            
            create unique index works_by_code on works (code);
            
            create table history (
              work_code integer not null,
              timestamp text not null,
              attribute text not null,
              value text not null,
              primary key (work_code, timestamp, attribute),
              foreign key (work_code) references works(code)
            );
            
            create index history_by_work on history (work_code);
            
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
    insert into works (code, name, parent, json) 
        values (:code, :name, :parent, :json);
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
    insert into history (work_code, timestamp, attribute, value) values (:work_code, :timestamp, :attribute, :value);
    '''
update_history = '''
    update history set value=:value where work_code=:work_code and timestamp=:timestamp and attribute=:attribute;
    '''
delete_history = '''
    delete from history where work_code=:work_code and timestamp=:timestamp and attribute=:attribute;
    '''
get_history = '''
    select value from history where work_code=:work_code and timestamp=:timestamp and attribute=:attribute;
    '''
get_history_by_work = '''
    select timestamp, attribute, value from history where work_code=:work_code;
'''
