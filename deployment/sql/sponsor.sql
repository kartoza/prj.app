
CREATE TABLE changes_sponsor (
    id integer NOT NULL,
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
    image_file character varying(100) NOT NULL,
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