-- adding a new column into the changes_entry table

 ALTER TABLE changes_entry ADD COLUMN funded_by character varying(225);
 ALTER TABLE changes_entry ADD COLUMN funder_url character varying(225);
 ALTER TABLE changes_entry ADD COLUMN developed_by character varying(225);
 ALTER TABLE changes_entry ADD COLUMN developer_url character varying(225);

