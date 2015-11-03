
CREATE TABLE changes_sponsor (
    id SERIAL NOT NULL,
    datetime_created timestamp with time zone NOT NULL,
    datetime_modified timestamp with time zone NOT NULL,
    creator_id integer,
    editor_id integer,
    name character varying(255) NOT NULL,
    sponsor_url character varying(255),
    contact_person character varying(255),
    sponsor_email character varying(255),
    sponsor_duration character varying(100),
    start_date timestamp with time zone,
    end_date timestamp with time zone,
    level character varying(10),
    agreement character varying(255),
    logo character varying(255),
    approved boolean NOT NULL,
    project_id integer NOT NULL,
    slug character varying(50),
    author_id integer NOT NULL
);

CREATE INDEX changes_sponsor_creator_id ON changes_sponsor USING btree (creator_id);
CREATE INDEX changes_sponsor_editor_id ON changes_sponsor USING btree (editor_id);
CREATE INDEX changes_sponsor_name_like ON changes_sponsor USING btree (name varchar_pattern_ops);
CREATE INDEX changes_sponsor_project_id ON changes_sponsor USING btree (project_id);
CREATE INDEX changes_sponsor_slug ON changes_sponsor USING btree (slug);
CREATE INDEX changes_sponsor_slug_like ON changes_sponsor USING btree (slug varchar_pattern_ops);
CREATE INDEX changes_sponsor_author_id ON changes_sponsor USING btree (author_id);

ALTER TABLE ONLY changes_sponsor
ADD CONSTRAINT changes_sponsor_pkey PRIMARY KEY (id);

INSERT INTO changes_sponsor (datetime_created, datetime_modified, name, sponsor_url, contact_person, sponsor_email, sponsor_duration, start_date, end_date, level, agreement, logo, approved, project_id, slug, author_id)
    VALUES ('2013-08-07 22:37:10.312+00', '2013-08-08 12:30:05.049+00', 'Kartoza', 'http://kartoza.com', '08628282', 'kartoza@kartoza.com','10','2013-08-07 22:37:10.312+00','2013-08-08 12:30:05.049+00', '1', '', '', 't',1,'sponsor-slug',1);