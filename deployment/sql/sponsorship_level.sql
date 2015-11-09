CREATE TABLE changes_sponsorshiplevel (
    id integer NOT NULL,
    datetime_created timestamp with time zone NOT NULL,
    datetime_modified timestamp with time zone NOT NULL,
    creator_id integer,
    editor_id integer,
    name character varying(255) NOT NULL,
    logo character varying(255) NOT NULL
);

CREATE SEQUENCE changes_sponsorshiplevel_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE changes_sponsorshiplevel ALTER id SET DEFAULT NEXTVAL('changes_sponsorshiplevel_id_seq');

ALTER TABLE ONLY changes_sponsorshiplevel
ADD CONSTRAINT changes_sponsorshiplevel_pkey PRIMARY KEY (id);
