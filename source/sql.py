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
              name text not null,
              work_type text not null,    -- collection, work, version or part
              parent integer,             -- when the work has a parent
              do_aggregate text,          -- whether this contributes to the parent's word count
              json text not null
            );
            
            create table history (
              id integer primary key,
              history_work integer not null,
              history_type text,
              history_value text,
              valid_from timestamp,
              foreign key(history_work) references works(id)
            );
            
            create table classifiers (
              id integer primary key,
              classifier_name text not null,
              json text not null
            );
            
            create table i18n (
              id integer primary key,
              language text not null,
              context text not null,
              key text not null,
              value text not null
            );
            '''
        },
    '0.1': {
        'target-version': '0.2',
        'ddl': ''';'''
    }
}

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

insert_work = '''
    insert into works (name, work_type, parent, do_aggregate, json) 
        values (:name, :type, :parent, aggregate, :json);
    '''

get_works = '''
    select json from works;
    '''

get_classifiers = '''
    select json from classifiers;
    '''

insert_classifier = '''
    insert into classifiers (classifier_name, json) values (:name, :json);
'''