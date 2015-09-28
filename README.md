# eHB Service

### Overview
Federal privacy laws allow for an individual or group of individuals to serve
as "Honest Brokers" within their institutions. The honest broker de-identifies
data to be used for research, essentially allowing researchers some flexibility
in using data from systems such as an electronic health record and providing
protection to the individuals whose data are being used for research. To ensure
integrity of the service, the Honest Broker must be listed on the study protocol
and must otherwise be independent of the research team.

CBMi's data reporting and management group provides an Honest Broker service as
a part of its more comprehensive EHR data extraction and management services.

## Installation

-- Section to be written --


## Configuration

ehb-service uses [django-environ](https://github.com/joke2k/django-environ) to handle configuration values for the application.

A default user is created with the login `admin@email.chop.edu` and a password of `Chopchop1234`

The following environment variables need to be set. If you prefer storing your configuration values in a file -- create a file in the root director of the application i.e. `local.env`. ehb-service will look for a `.env` file in the root that corresponds to the `APP_ENV` environment variable. So, if `APP_ENV=local` ehb-service will look for `local.env` in the root of the application.

Otherwise, you will want to set the following values:

```bash
# Django DEBUG value
DEBUG=1
# Django SECRET_KEY
SECRET_KEY=my_secret_key
# Default Django db
DATABASE_URL=postgres://user@localhost:5432/ehb_service

# Set the following if you plan on using LDAP for authentication to the admin
# portion of the app. Note, ehb-service uses token-based authentication
# so this really applies only to the Django admin portion of the app.
LDAP_DEBUG=0
LDAP_PREBINDDN=
LDAP_SEARCHDN=
LDAP_SEARCH_FILTER=
LDAP_SERVER_URI=
LDAP_PREBINDPW=

# Standard Django admin settings
EMAIL_HOST=localhost
EMAIL_PORT=25
EMAIL_DOMAIN=example.com

# Whether the eHB should use encryption
EHB_USE_ENCRYPTION=0
# Encryption key for the key management service
EHB_KMS_SECRET=my_kms_secret
# Seed values for key creation
EHB_CLIENT_KEY_SEED=123456789
EHB_GROUP_KEY_SEED=1235456789
