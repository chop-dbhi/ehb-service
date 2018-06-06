***********************
EHB SERVICE API - Notes
***********************

- For Group API calls: can be dangerous to make modifications and/or add directly to groups table because the other tables don’t get updated, such as subject_group.

- Subject_group doesn’t have API calls - instead, see Group - produces same results.

- Client key is automatically set to ‘testck’ when you create a protocol on the BRP. (need client key for several API requests)

- External record api calls are the only ones that have changed since the white paper was written. There is an added field: "label".

- Some more api testing would be good to make sure changes in a record in one table are reflected in the same record on other tables. Example is the issue identified in the first bullet. 
