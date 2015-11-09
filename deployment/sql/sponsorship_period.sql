CREATE TABLE changes_sponsorshipperiod (
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

ALTER TABLE changes_sponsorshipperiod ALTER id SET DEFAULT NEXTVAL('changes_sponsorshipperiod_id_seq');

ALTER TABLE ONLY changes_sponsorshipperiod
ADD CONSTRAINT changes_sponsorshipperiod_pkey PRIMARY KEY (id);

ALTER TABLE ONLY changes_sponsorshipperiod
    ADD CONSTRAINT changes_sponsor_sponsorshipperiod_id FOREIGN KEY (sponsor_id) REFERENCES changes_sponsor(id) DEFERRABLE INITIALLY DEFERRED;
