drop table if exists users;
create table users ( 
    id integer primary key autoincrement,
    email text not null,
    username text not null,
    password_hash text not null
);
