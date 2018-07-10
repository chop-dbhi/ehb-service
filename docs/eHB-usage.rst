**How to use the eHB**
=======================

**What is an Honest Broker**
----------------------------
from Chop's institutional Review Board:


    "An honest broker can provide a firewall between the investigator and subjects' identifiable information. For example, an honest broker could generate or receive a dataset and then strip out subject identifiers so that the data was no longer readily identifiable."

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Definitions:**
----------------

    - **External Record Identifier:** An identifier that is linked to  subject, but is generated and stored in a system other than the eHB.
    - **Subject:** A research subject (could be a patient or a subject from another source)
    - **Subject Group:** A group of subjects (protocol or a dataset)
    - **External Record Group:** a group of external records for a subject in a given protocol
    - **Group ID:** each protocol, subject in a protocol, external record group receives a unique group id.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Steps:**
-----------

    **Assumptions:**

      * Organization is already in the eHB. If not see API call…. To create a new organization
      * A Subject group has already been created. If not see API call… to create a new subject group.
      * System or person making the request has an API token and group client key.

    **1 Add a subject to the eHB**

      This will only add a subject to the subject table in the eHB, no identifiers are created. The following fields are required:
      * First name
      * Last name
      * Organization
      * Organization ID
      * Date of birth
      See 'POST to create a subject' in the API documentation.

    **2 Add a subject to a protocol or dataset**

        1. Create a group for a subject on a given Protocol
        2. Add subject to subject group (Subject group name should be stored by the external system)

    **3 Add External Identifier for a given Subject**

        1. if this external ID is only at the subject group level, then create an external record group, else skip to 2
        2. Add Record ID
