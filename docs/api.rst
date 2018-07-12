***************
EHB SERVICE API
***************

The eHB Service provides a RESTful API for retrieving and updating data in the application.

The API calls listed below are formatted such that:

- 'Example Request' includes all of the necessary user inputs for a successful API call.
- 'Example Response' are the exact contents outputted by the API.

.. contents:: Table of Contents


User Input for Example Request
==============================

+-------------------------+------------------+--------------------------------------------+
| Key                     | Value            | Description                                |
+=========================+==================+============================================+
| Host                    | example.com      | EHB host URL                               |
+-------------------------+------------------+--------------------------------------------+
| URL                     | /api/api_call/   | API call URL                               |
+-------------------------+------------------+--------------------------------------------+
| Accept OR Content-Type  | application/json | GET and DELETE requests will use Accept;   |
|                         |                  | POST and PUT requests will use Content-Type|
+-------------------------+------------------+--------------------------------------------+
| Group-Client-Key        | ex: testck       | This is set by the client and serves as a  |
| (for Group and          |                  | password for controlling groups.           |
| Subject_Group calls)    |                  | Client_key is not sent in any response     |
|                         |                  | provided by eHB                            |
+-------------------------+------------------+--------------------------------------------+
| Body (optional)         |                  | POST and PUT requests to create and edit   |
|                         |                  | typically require body. Body is typically  |
|                         |                  | in json.                                   |
+-------------------------+------------------+--------------------------------------------+

User Input for URL
==================

URL format is always HOST_URL/API_URL. (example.com/api/api_call)

Common user inputs required for the API_URL include:

+-------------------------+---------------------------------------------------------------+
| URL Input               | Description                                                   |
+=========================+===============================================================+
| (int: subject_id)       | This is the primary key used to identify every subject        |
|                         | stored on the eHB. Can be obtained through API call           |
|                         | Subject Group::GET, as the value ‘id’.                        |
+-------------------------+---------------------------------------------------------------+
| (int: organization_id)  | This is the primary key used to identify every                |
|                         | organization stored on the eHB. Can be obtained through API   |
|                         | call Organization::POST(query), as the value 'id'             |
+-------------------------+---------------------------------------------------------------+
| (str: os_id)            | This is the organization_subject_id, or MRN of a subject. Can |
|                         | be obtained through various API calls, including Subject::GET |
+-------------------------+---------------------------------------------------------------+
| (int: group_id)         | This is the primary key used to identify every group record   |
|                         | in the eHB. Can be obtained through API call GROUP::GET       |
+-------------------------+---------------------------------------------------------------+
| (int: externalrecord_id)| This is the primary key used to identify every external record|
|                         | in the eHB. Can be obtained through API call ExternalRecord:: |
|                         | POST(query)                                                   |
+-------------------------+---------------------------------------------------------------+
| (int: externalsystem_id)| This is the primary key used to identify every external system|
|                         | in the eHB. Can be obtained through API call ExternalSystem:: |
|                         | POST(query) if External System name or URL is known.          |
+-------------------------+---------------------------------------------------------------+



Subjects
========

GET a subject's info with id
-----------------------------

**URL**:

.. http:get:: /api/subject/id/(int: subject_id)/

**Example Request**:

.. sourcecode:: http

    Host: example.com
    GET /api/subject/id/5856/
    Accept: application/json
    Api-token:

**Example Response**:

.. sourcecode:: http

    HTTP/1.1 200 OK
    Vary: Accept
    Content-Type: application/json

    {
    "first_name": "Test",
    "last_name": "Sub",
    "created": "2016-06-03 15:03:16.603638",
    "dob": "2013-01-01",
    "modified": "2016-06-03 15:03:16.603664",
    "organization_id_label": "Medical Record Number",
    "organization_subject_id": "testtest123",
    "organization": 2,
    "id": 5856
    }

GET a subject's info with organization ID and MRN
-------------------------------------------------

**URL**:

.. http:get:: /api/subject/organization/(int: organization_id)/osid/(str: os_id)

**Example Request**:

.. sourcecode:: http

      Host: example.com
      GET /api/subject/organization/2/osid/testtest123
      Accept: application/json
      Api-token:

**Example Response**:

.. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: application/json

      {
      "first_name": "Test",
      "last_name": "Sub",
      "created": "2016-06-03 15:03:16.603638",
      "dob": "2013-01-01",
      "modified": "2016-06-03 15:03:16.603664",
      "organization_id_label": "Medical Record Number",
      "organization_subject_id": "testtest123",
      "organization": 2,
      "id": 5856
      }

GET a subject with external record ID and external system ID
------------------------------------------------------------
**URL**:

.. http:get:: /api/subject/externalrecsys/(int: externalsystem_id)/erid/(int: externalrecord_id)

**Example Request**:

.. sourcecode:: http

      Host: example.com
      GET /api/subject/externalrecsys/19/erid/
      Accept: application/json
      Api-token:

**Example Response**:

.. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: application/json

    


DELETE a subject with subject_id
--------------------------------

**URL**:

.. http:delete:: api/subject/id/(int: subject_id)/

**Example Request**:

.. sourcecode:: http

    Host: example.com
    DELETE /api/subject/id/5856
    Accept: application/json
    Api-token:

**Example Response**:

.. sourcecode:: http

    HTTP/1.1 200 OK
    Vary: Accept
    Content-Type: application/json

    {
    "first_name": "Test",
    "last_name": "Sub",
    "created": "2016-06-03 15:03:16.603638",
    "dob": "2013-01-01",
    "modified": "2016-06-03 15:03:16.603664",
    "organization_id_label": "Medical Record Number",
    "organization_subject_id": "testtest123",
    "organization": 2,
    "id": 5856

    }

DELETE a subject with organization_id and MRN
---------------------------------------------
**URL**:

.. http:delete:: api/subject/organization/(int: organization_id)/osid/(int: os_id)/


POST to create a subject
------------------------

**URL**:

.. http:post:: /api/subject/

**Example Request**:

.. sourcecode:: http

      POST /api/subject/
      Host: example.com
      Content-type: application/json
      Api-token:
      Body:
      [
      {
        "first_name":"value",
        "last_name":"value",
        "organization":"6",
        "organization_subject_id":"334",
        "dob":"2000-02-02"
        }
        ]

**Example Response**:

.. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: application/json

      [
      {
        "success": true,
        "created": "2018-6-7 11:23:7",
        "modified": "2018-6-7 11:23:7",
        "organization_id": "6",
        "organization_subject_id": "334",
        "id": "22"
        }
        ]

PUT to modify a subject
-----------------------

**URL**:

.. http:put:: /api/subject/

**Example Request**:

.. sourcecode:: http

      PUT /api/subject/
      Host: example.com
      Content-Type: application/json
      Api-token:
      Body:
      [
       {
          "id": "11",
          "old_subject": {
             "first_name": "sdfsd",
             "last_name": "sdfsdf",
             "group_name": "",
             "organization_subject_id": "6665",
             "organization": 6,
             "organization_id_label": "Record ID",
             "dob": "2222-2-2",
             "id": 11,
             "modified": "2018-06-06 11:55:49.423644",
             "created": "2018-06-06 11:55:49.423626"
          },
          "new_subject": {
             "first_name": "thisisthe",
             "last_name": "newname2",
             "group_name": "",
             "organization_subject_id": "6665",
             "organization": 6,
             "organization_id_label": "Record ID",
             "dob": "2222-2-2",
             "id": 11,
             "modified": "2018-06-06 11:55:49.423644",
             "created": "2018-06-06 11:55:49.423626"
          }
        }
        ]

**Example Response**:

.. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: application/json

      [
      {
        "created": "2018-6-6 11:55:49",
        "id": "11",
        "success": true,
        "modified": "2018-6-7 16:21:9"
      }
      ]

Subject Group
=============
GET a list of subjects in a subject group
-----------------------------------------

**URL**:

.. http:get:: api/group/id/(int: group_id)/subjects/

**Example Request**:

.. sourcecode:: http

    GET /api/group/id/9624/subjects/
    Host: example.com
    Accept: application/json
    Api-token:
    GROUP-CLIENT-KEY:

**Example Response**:

.. sourcecode:: http

    HTTP/1.1 200 OK
    Vary: Accept
    Content-Type: application/json

    [
    {
      "first_name": "Alexander",
      "last_name": "Gonzalez",
      "created": "2016-11-22 13:56:51.581028",
      "dob": "1990-07-01",
      "modified": "2016-11-22 13:56:51.581049",
      "organization_id_label": "Medical Record Number",
      "organization_subject_id": "Test1",
      "organization": 2,
      "id": 6738
      }
      ]

POST to create a subject group
------------------------------
**URL**:

.. http:post:: api/group/

**Example Request**:

.. sourcecode:: http

    POST /api/group/
    Host: example.com
    Content-Type: application/json
    Api-token:
    Body:
    [
    {
      "name": "testforgroupost",
      "client_key": "hello",
      "is_locking": "true",
      "description": "value"
    }
    ]

**Example Response**:

.. sourcecode:: http

    HTTP/1.1 200 OK
    Vary: Accept
    Content-Type: application/json

    [
    {
        "ehb_key": "UDY8HSLY1MNFB906",
        "name": "testforgroupost",
        "success": true,
        "created": "2018-6-7 16:46:58",
        "modified": "2018-6-7 16:46:58",
        "id": "24"
    }
    ]


POST to add subject to group
----------------------------
**URL**:

.. http:post:: api/group/id/(int: group_id)/subjects/

**Example Request**:

.. sourcecode:: http

    POST /api/group/
    Host: example.com
    Content-Type: application/json
    Api-token: (api token)
    Group-Client-Key: (client key for subj group)
    Body:
    [6738] # this value is subject_id

**Example Response**:

.. sourcecode:: http

    HTTP/1.1 200 OK
    Vary: Accept
    Content-Type: application/json

    [
    {"id": 6738, "success": true}
    ]

DELETE a subject from Subject Group
-----------------------------------------

**URL**:

.. http:delete:: api/group/id/(int: group_id)/subjects/id/(int: subject)id)/

**Example Request**:

.. sourcecode:: http

    DELETE /api/group/id/9624/subjects/id/6738/
    Host: example.com
    Accept: application/json
    Api-token:
    GROUP-CLIENT-KEY:

**Example Response**:

.. sourcecode:: http

    HTTP/1.1 204 OK
    Vary: Accept
    Content-Type: application/json

    (no return content)


Group
=====
GET to get Group info (group id)
--------------------------------
**URL**:

.. http:get:: api/group/?id=(int: group_id)

**Example Request**:

.. sourcecode:: http

  GET /api/group/?id=451
  Host: example.com
  Accept: application/json

**Example Response**:

.. sourcecode:: http

  HTTP/1.1 200 OK
  Vary: Accept
  Content-Type: application/json

  {
  "ehb_key": "M4EI66ZYST8KZ2UY",
  "description": "A BRP Protocol Group",
  "created": "2012-11-19 13:53:56.945841",
  "modified": "2012-11-19 13:53:56.945861",
  "is_locking": "True",
  "id": "451",
  "name": "BRP:AV2PD77NXURSHEEI"
  }

GET to get Group info (group name)
-----------------------------------
**URL**:

.. http:get:: api/group/?name=(str: group_name)

**Example Request**:

.. sourcecode:: http

  GET /api/group/?name=BRP:AV2PD77NXURSHEEI
  Host: example.com
  Accept: application/json

**Example Response**:

.. sourcecode:: http

  HTTP/1.1 200 OK
  Vary: Accept
  Content-Type: application/json

  {
  "ehb_key": "M4EI66ZYST8KZ2UY",
  "description": "A BRP Protocol Group",
  "created": "2012-11-19 13:53:56.945841",
  "modified": "2012-11-19 13:53:56.945861",
  "is_locking": "True",
  "id": "451",
  "name": "BRP:AV2PD77NXURSHEEI"
  }


POST to create a group
-----------------------
**URL**:

.. http:post:: api/group/

**Example Request**:

.. sourcecode:: http

  POST /api/group/
  Host: example.com
  Content-Type: application/json
  Api-token:
  Body:
  [
  {
    "name": "testforgroupost",
    "client_key": "hello",
    "is_locking": "true",
    "description": "value"
  }
  ]

**Example Response**:

.. sourcecode:: http

  HTTP/1.1 200 OK
  Vary: Accept
  Content-Type: application/json

  [
  {
      "ehb_key": "UDY8HSLY1MNFB906",
      "name": "testforgroupost",
      "success": true,
      "created": "2018-6-7 16:46:58",
      "modified": "2018-6-7 16:46:58",
      "id": "24"
  }
  ]

PUT to modify a group
---------------------
**URL**:

.. http:put:: api/group/

**Example Request**:

.. sourcecode:: http

  PUT /api/group/
  Host: example.com
  Content-Type: application/json
  Api-token:
  Body:
  [
  {
    "name": "testforgroupost",
    "client_key": "hello",
    "is_locking": "true",
    "description": "value"
  }
  ]

**Example Response**:

.. sourcecode:: http

  HTTP/1.1 200 OK
  Vary: Accept
  Content-Type: application/json

  [
  {
      "ehb_key": "UDY8HSLY1MNFB906",
      "name": "testforgroupost",
      "success": true,
      "created": "2018-6-7 16:46:58",
      "modified": "2018-6-7 16:46:58",
      "id": "24"
  }
  ]




Organization
============

GET an organization's details with organization_id
---------------------------------------------------

**URL**:

.. http:get:: /api/organization/id/(int: organization_id)/

**Example Request**:

.. sourcecode:: http

      GET /api/organization/id/2
      Host: example.com
      Accept: application/json
      Api-token:

**Example Response**:

.. sourcecode:: http

    HTTP/1.1 200 OK
    Vary: Accept
    Content-Type: application/json
    Api-token:

    {
    "id": "2",
    "subject_id_label": "Medical Record Number",
    "name": "AMAZING CHILDREN'S HOSPITAL",
    "modified": "2013-06-27 10:48:46.635666",
    "created": "2013-06-27 10:48:46.635639"
    }

POST to create an organization
------------------------------

**URL**:

.. http:post:: /api/organization/

**Example Request**:

.. sourcecode:: http

      POST /api/organization/
      Host: example.com
      Content-type: application/json
      Api-token:
      Body:
      [
      {
        "name": "value",
        "subject_id_label": "value"
      }
      ]

**Example Response**:

.. sourcecode:: http

    HTTP/1.1 200 OK
    Vary: Accept
    Content-Type: application/json
    Api-token:

    [
    {
        "name": "value",
        "created": "2018-6-7 14:44:1",
        "id": "7",
        "success": true,
        "modified": "2018-6-7 14:44:1"
    }
    ]

POST (query) to obtain organization info
---------------------------------------------------

**URL**:

.. http:post:: /api/organization/query/

**Example Request**:

.. sourcecode:: http

      POST /api/organization/query/
      Host: example.com
      Content-Type: application/json
      Api-token:
      Body:
      [
      {
        "name": "value"
      }
      ]

**Example Response**:

.. sourcecode:: http

    [
      {
          "organization": {
              "id": "7",
              "subject_id_label": "value",
              "name": "value",
              "modified": "2018-06-07 14:44:01.328518",
              "created": "2018-06-07 14:44:01.328456"
          },
          "name": "value"
      }
    ]


DELETE a subject in an organization
-----------------------------------

**URL**:
.. http:delete:: /api/organization/id/(int: organization_id)

**Example Request**:

.. sourcecode:: http

      DELETE /api/organization/id/7
      Host: example.com
      Accept: application/json
      Api-token:


**Example Response**:

.. sourcecode:: http

    HTTP/1.1 200 OK
    Vary: Accept
    Content-Type: application/json

PUT to modify an organization
-----------------------------

**URL**:

.. http:put:: /api/organization/

**Example Request**:

.. sourcecode:: http

      PUT /api/subject/
      Host: example.com
      Content-Type: application/json
      Api-token:
      Body:

**Example Response**:

.. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: application/json

      [
      {
      "id": "11",
      "old_subject": {
         "first_name": "sdfsd",
         "last_name": "sdfsdf",
         "group_name": "",
         "organization_subject_id": "6665",
         "organization": 6,
         "organization_id_label": "Record ID",
         "dob": "2222-2-2",
         "id": 11,
         "modified": "2018-06-06 11:55:49.423644",
         "created": "2018-06-06 11:55:49.423626"
      },
      "new_subject": {
         "first_name": "thisisthe",
         "last_name": "newname2",
         "group_name": "",
         "organization_subject_id": "6665",
         "organization": 6,
         "organization_id_label": "Record ID",
         "dob": "2222-2-2",
         "id": 11,
         "modified": "2018-06-06 11:55:49.423644",
         "created": "2018-06-06 11:55:49.423626"
      }
      }
      ]

External System
===============

GET an external system's information
------------------------------------

**URL**:

.. http:get:: /api/externalsystem/id/(int: externalsystem_id)

**Example Request:**

.. sourcecode:: http

      GET /api/externalsystem/id/15
      Host: example.com
      Accept: application/json
      Api-token:

**Example Response:**

.. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: application/json

      {
      "description": "Test Instance of REDCap",
      "created": "2016-06-10 10:58:05.230277",
      "url": "https://redcap-test.research.chop.edu/api/",
      "modified": "2016-06-10 10:58:05.230297",
      "id": "15",
      "name": "REDCap Test"
      }

GET a list of subjects in the external system
---------------------------------------------

**URL**:

.. http:get:: /api/externalsystem/id/(int: externalsystem_id)/subjects/

**Example Request:**

.. sourcecode:: http

    GET /api/externalsystem/id/6/subjects/
    Host: example.com
    Content-Type: application/json
    Api-token:

**Example Response:**

.. sourcecode:: http

    HTTP/1.1 200 OK
    Vary: Accept
    Content-Type: application/json

    [
      {
        "first_name": "Tyler",
        "last_name": "Test",
        "created": "2013-07-17 08:38:06.668080",
        "dob": "2010-07-01",
        "modified": "2013-09-10 12:09:11.946897",
        "organization_id_label": "Medical Record Number",
        "organization_subject_id": "11251125",
        "organization": 2,
        "id": 681
      },
      {
        "first_name": "DMZ",
        "last_name": "Validation",
        "created": "2013-08-05 15:24:51.963083",
        "dob": "2010-07-25",
        "modified": "2013-08-05 15:24:51.963112",
        "organization_id_label": "Medical Record Number",
        "organization_subject_id": "1234567888",
        "organization": 2,
        "id": 695
      }
    ]

GET a list of records in an external system
-------------------------------------------
**URL**:

.. http:get:: api/externalsystem/id/(int: externalsystem_id)/records/

**Example Request**:

.. sourcecode:: http

    GET /api/externalsystem/id/6/records/
    Host: example.com
    Accept: application/json
    Api-token:

**Example Response**:

.. sourcecode:: http

    HTTP/1.1 200 OK
    Vary: Accept
    Content-Type: application/json

    [
    {
        "created": "2013-07-16 14:58:43.619833",
        "modified": "2015-01-13 01:13:47.757278",
        "label": 1,
        "record_id": "7316-402",
        "path": "CBTTC - Training",
        "external_system": 6,
        "id": 1372,
        "subject": 673
    },
    {
        "created": "2013-07-16 14:59:02.208497",
        "modified": "2015-01-13 01:13:47.765353",
        "label": 1,
        "record_id": "7316-403",
        "path": "CBTTC - Training",
        "external_system": 6,
        "id": 1373,
        "subject": 675
    },
    ]

GET a list of records in external system with specified organization
--------------------------------------------------------------------

**URL**:
.. http::get:: api/externalsystem/id/(int: externalsystem_id)/organization/(int: organization_id)/records/

**Example Request**:

.. sourcecode:: http

    GET /api/externalsystem/id/6/organization/2/records/
    Host: example.com
    Accept: application/json
    Api-token:

**Example Response**:

.. sourcecode:: http

    HTTP/1.1 200 OK
    Vary: Accept
    Content-Type: application/json

    [
        {
            "created": "2013-07-16 14:58:43.619833",
            "modified": "2015-01-13 01:13:47.757278",
            "label": 1,
            "record_id": "7316-402",
            "path": "CBTTC - Training",
            "external_system": 6,
            "id": 1372,
            "subject": 673
        },
        {
            "created": "2013-07-16 14:59:02.208497",
            "modified": "2015-01-13 01:13:47.765353",
            "label": 1,
            "record_id": "7316-403",
            "path": "CBTTC - Training",
            "external_system": 6,
            "id": 1373,
            "subject": 675
        },
      ]

POST to create External System(s)
-----------------------------------

**URL**:
.. http:post:: /api/externalsystem/

**Example Request**:

.. sourcecode:: http

      POST /api/externalsystem/
      Host: example.com
      Content-Type: application/json
      Api-token:

      [
       {
          "name": "test",
          "description": "value",
          "url": "http://example.com/test/"
       },
       {
          "name": "test2",
          "description": "value",
          "url": "http://example.com/test2/"
       }
      ]


**Example Response**:

.. sourcecode:: http

    HTTP/1.1 200 OK
    Vary: Accept
    Content-Type: application/json

    [
     {
        "name": "test",
        "created": "2018-7-9 13:14:17",
        "id": "20",
        "success": true,
        "modified": "2018-7-9 13:14:17"
     },
     {
        "name": "test2",
        "created": "2018-7-9 13:14:17",
        "id": "21",
        "success": true,
        "modified": "2018-7-9 13:14:17"
     }
    ]

POST (query) to obtain external system info
-------------------------------------------
**URL**:

.. http:post:: /api/externalsystem/query/

**Example Request**:

.. sourcecode:: http

      POST /api/externalsystem/query/
      Host: example.com
      Content-Type: application/json
      Api-token:
      Body:
      [{"name": "Nautilus"}]
      OR
      [{"url": "http://10.30.9.218:8090/api/"}]

**Example Response**:

.. sourcecode:: http

    HTTP/1.1 200 OK
    Vary: Accept
    Content-Type: application/json

    [
     {
        "externalSystem": {
           "description": "RESLIMS01 production Nautilus",
           "created": "2012-06-02 10:36:49.773564",
           "url": "http://10.30.9.218:8090/api/",
           "modified": "2014-04-23 11:01:21.261794",
           "id": "3",
           "name": "Nautilus"
        },
        "name": "Nautilus"
     }
    ]

    OR

    [
     {
        "url": "http://10.30.9.218:8090/api/",
        "externalSystem": {
           "description": "RESLIMS01 production Nautilus",
           "created": "2012-06-02 10:36:49.773564",
           "url": "http://10.30.9.218:8090/api/",
           "modified": "2014-04-23 11:01:21.261794",
           "id": "3",
           "name": "Nautilus"
        }
     }
    ]

PUT to modify External System(s)
-----------------------------------

**URL**:
.. http:put:: /api/externalsystem/

**Example Request**:

.. sourcecode:: http

    PUT /api/externalsystem/
    Host: example.com
    Content-Type: application/json
    Api-token:

    [
       {
          "id": 20,
          "external_system": {
             "description": "new description"
          }
       }
    ]


**Example Response**:

.. sourcecode:: http

  HTTP/1.1 200 OK
  Vary: Accept
  Content-Type: application/json

  [
     {
        "created": "2018-7-9 13:14:17",
        "id": "20",
        "success": true,
        "modified": "2018-7-9 13:20:3"
     }
  ]

DELETE an external system
-------------------------
**URL**:

.. http:delete:: api/externalsystem/id/(int: externalsystem_id)

**Example Request**:

.. sourcecode:: http

    DELETE /api/externalsystem/id/3/
    Host: example.com
    Accept: application/json
    Api-token:

**Example Response**:

.. sourcecode:: http

    HTTP/1.1 204 OK
    Vary: Accept
    Content-Type: application/json


External Record
===============

GET an external record
----------------------
**URL**:

.. http:get:: api/externalrecord/id/(int: externalrecord_id)/

**Example Request**:

.. sourcecode:: http

    GET /api/externalrecord/id/27871
    Host: example.com
    Accept: application/json
    Api-token:

**Example Response**:

.. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: application/json

      {
      "created": "2018-06-04 16:47:40.320305",
      "modified": "2018-06-04 16:47:40.320347",
      "label": 1,
      "record_id": "QLUBPG4Y0U8Y67TZ:JIEEDIOEP",
      "path": "CBTTC - Specimen Only",
      "external_system": 2,
      "id": 27871,
      "subject": 4921
      }

GET an external record with label
---------------------------------
**URL**:

.. http:get:: /api/externalrecord/labels/(int: externalrecordlabel_id)/

**Example Request**:

.. sourcecode:: http

      GET /api/externalrecord/labels/82/
      Host: example.com
      Accept: application/json
      Api-token:

**Example Response**:

.. sourcecode:: http

      {
      "id": 82,
      "label": "This is a test"
      }


POST (query) to obtain external record info
-------------------------------------------
**URL**:

.. http:post:: /api/externalrecord/query/

**Example Request**:

.. sourcecode:: http

      Host: example.com
      POST: /api/externalrecord/query/
      Content-Type: application/json
      Api-token:
      Body:
      [
      {
        "subject_id":"2",
        "external_system_id":"2",
        "path":"Test Protocol"
      },
      {
        "subject_org":,
        "subject_org_id"
      },
      {
        "subject_id":,
        "external_system_name":,
      },
      {
        "subect_id":,
        "external_system_url":
      }
      ]

**Example Response**:

.. sourcecode:: http

    HTTP/1.1 200 OK
    Vary: Accept
    Content-Type: application/json

    [
    {
        "external_record": [
            {
                "created": "2014-01-28 13:42:41.693000",
                "modified": "2014-01-28 13:42:41.693000",
                "label": 1,
                "record_id": "NXB546EUZSDLZKGR:5EM3AOORG",
                "path": "Test Protocol",
                "external_system": 2,
                "id": 1,
                "subject": 2
            }
        ],
        "path": "Test Protocol",
        "subject_id": "2",
        "external_system_id": "2"
    }
]

POST to create an external Record
-----------------------------------------
**URL**:

.. http:post:: /api/externalrecord/

**Example Request**:

.. sourcecode:: http

      POST /api/externalrecord/
      Host: example.com
      Content-Type: application/json
      Api-token:
      Body:
      [
       {
          "subject": "2",
          "external_system": "2",
          "record_id": "98797",
          "path": "Test Protocol",
          "label": "1"
       }
      ]

**Example Response**:

.. sourcecode:: http

    HTTP/1.1 200 OK
    Vary: Accept
    Content-Type: application/json

    [
    {
      "success": true,
      "created": "2018-6-8 11:47:53",
      "modified": "2018-6-8 11:47:53",
      "label_id": 1,
      "record_id": "98797",
      "path": "Test Protocol",
      "id": "5"
    }
    ]

PUT to modify an external record
--------------------------------
**URL**:

.. http:put:: /api/externalrecord/

**Example Request**:

.. sourcecode:: http

      POST /api/externalrecord/
      Host: example.com
      Content-Type: application/json
      Api-token:
      Body:
      [
       {
          "id": "5",
          "external_record": {
             "subject": "2",
             "external_system": "2",
             "record_id": "33333"
          }
       }
       ]

**Example Response**:

.. sourcecode:: http

    HTTP/1.1 200 OK
    Vary: Accept
    Content-Type: application/json

    [
    {
        "created": "2018-6-8 11:47:53",
        "id": "5",
        "success": true,
        "modified": "2018-6-8 11:57:52"
    }
    ]
