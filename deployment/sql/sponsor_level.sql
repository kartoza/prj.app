CREATE TABLE changes_sponsorlevel (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    logo character varying(255) NOT NULL,
    author_id integer NOT NULL
);

CREATE SEQUENCE changes_sponsorlevel_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE changes_sponsorlevel ALTER id SET DEFAULT NEXTVAL('changes_sponsorlevel_id_seq');
