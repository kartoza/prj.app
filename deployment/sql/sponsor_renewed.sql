CREATE TABLE changes_sponsorrenewed (
    id integer NOT NULL,
    datetime_created timestamp with time zone NOT NULL,
    datetime_modified timestamp with time zone NOT NULL,
    creator_id integer,
    editor_id integer,
    sponsor_id integer NOT NULL,
    start_date timestamp with time zone,
    end_date timestamp with time zone
);

CREATE SEQUENCE changes_sponsorrenewed_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE changes_sponsorrenewed ALTER id SET DEFAULT NEXTVAL('changes_sponsorrenewed_id_seq');

ALTER TABLE ONLY changes_sponsorrenewed
ADD CONSTRAINT changes_sponsorrenewed_pkey PRIMARY KEY (id);

ALTER TABLE ONLY changes_sponsorrenewed
    ADD CONSTRAINT changes_sponsor_sponsorrenewed_id FOREIGN KEY (sponsor_id) REFERENCES changes_sponsor(id) DEFERRABLE INITIALLY DEFERRED;
