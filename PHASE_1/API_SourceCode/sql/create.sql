-- TODO: Add key_terms as attr (Array)
create table articles
(
	url varchar
		constraint articles_pk
			primary key,
	date_of_publication timestamp,
	headline varchar,
	main_text varchar
);

create table reports
(
	id serial
		constraint reports_pk
			primary key,
	article_url varchar
		constraint reports_articles_url_fk
			references articles,
	syndrome varchar,
	event_date varchar,
	disease varchar
);

create table locations
(
    report_id integer not null
        constraint locations_reports_id_fk
            references reports,
    country   varchar not null,
    location  varchar not null,
    constraint locations_pk
        primary key (report_id, country, location)
);
