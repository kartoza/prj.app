CREATE TABLE changes_sponsorlevel (
    id integer NOT NULL,
    datetime_created timestamp with time zone NOT NULL,
    datetime_modified timestamp with time zone NOT NULL,
    creator_id integer,
    editor_id integer,
    name character varying(255) NOT NULL,
    logo character varying(255) NOT NULL
);

CREATE SEQUENCE changes_sponsorlevel_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE changes_sponsorlevel ALTER id SET DEFAULT NEXTVAL('changes_sponsorlevel_id_seq');

ALTER TABLE ONLY changes_sponsorlevel
ADD CONSTRAINT changes_sponsorlevel_pkey PRIMARY KEY (id);

