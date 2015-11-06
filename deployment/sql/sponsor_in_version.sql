
 ALTER TABLE changes_version ADD COLUMN sponsor_id integer;
 ALTER TABLE ONLY changes_version
    ADD CONSTRAINT changes_version_sponsor_id FOREIGN KEY (sponsor_id) REFERENCES changes_sponsor(id) DEFERRABLE INITIALLY DEFERRED;
