# encoding: utf-8
# author: Marko Čibej
# file: sql.py
"""
A collection of SQL strings, kept separate from python and js code
for the sake of decency.
"""

upgrade_db = {'0.0': ['0.1',
                      '''
                    create table meta (
                        id integer primary key,
                        database_version text,
                        system_version,
                        last_saved text
                    );
                    insert into meta (database_version) values ('0.0');
                    create table works (
                        id integer primary key, 
                        name text not null,
                        level text not null,   -- whether
                        parent integer,
                        json text not null
                    );
                    create table history (
                        id integer primary key, 
                        history_work integer not null,
                        foreign key(history_work) references works(id),
                        value_type text,
                        timestamp text,
                        value text
                    );
                    '''],
             '0.1': ''}

insert_work = 'insert into works (work) values (?)'