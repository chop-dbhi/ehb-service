**How to use the eHB**
=======================

**What is an Honest Broker**
----------------------------
from Chop's institutional Review Board:


    "An honest broker can provide a firewall between the investigator and subjects' identifiable information. For example, an honest broker could generate or receive a dataset and then strip out subject identifiers so that the data was no longer readily identifiable."


**Definitions**
----------------

- **External Record Identifier:** An identifier that is linked to  subject, but is generated and stored in a system other than the eHB.
- **Subject:** A research subject (could be a patient or a subject from another source)
- **Subject Group:** A group of subjects (protocol or a dataset)
- **External Record Group:** a group of external records for a subject in a given protocol
- **Group ID:** each protocol, subject in a protocol, external record group receives a unique group id.

**Steps to add a subject to a protocol and add external records**
-----------

These steps are how the BRP and the eHB import tool adds subjects to the eHB.
The eHB import tool repository can be found _here: https://github.research.chop.edu/dbhi/ehb-import-tool

**Assumptions**
^^^^^^^^^^^^^^^

* Organization is already in the eHB. If not see 'POST to create an organization' in the API documentation to create a new organization
* A Subject group has already been created. If not see 'POST to create a subject group' in the API documentation to create a new subject group.
* System or person making the request has an API token and group client key. See system administrators for this information.
* External System has been created and PK of system is known.

**1. Add a subject to the eHB**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This will only add a subject to the subject table in the eHB, no identifiers are created. The following fields are required:
      * First name
      * Last name
      * Organization
      * Organization ID
      * Date of birth

See 'POST to create a subject' in the API documentation. if you receive successful
response with error code 3 then this subject already exists in the eHB.

**2. Add a subject to a protocol or dataset**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Create a group for a subject on a given Protocol
  * Required fields:
    **name**
    **client_key** receive from eHB administrators;
    **is_locking** should be true, this means that the item can be changed;
    **description** should be, "A BRP Protocol Subject Record Group";
  * See 'POST to create a group' in the API documentation.
  * This group name is what is used to connect an external record in step 3.
2. Add subject to subject group (Subject group name should be stored by the external system)
  * Required Fields:
    **group_id**
    **subject_id**
  * see 'POST add subject to group' in the API documentation.

**3. Add External Identifier for a given Subject**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. If this external ID is only at the subject group level, then create an external record group, else skip to 2
  * Required fields:
    **name**
    **client_key**
    **is_locking**
    **description**
  * See 'POST to create a group' in the API documentation.
2. Add external Record ID
  * Required fields:
    **subject PK**
    **external_system PK**
    **Record id**
    **path**
    **label**
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
