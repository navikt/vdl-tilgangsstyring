#!/bin/bash

#snowbird
export PERMISSION_BOT_USER=$DBT_USR
export PERMISSION_BOT_ACCOUNT="wx23413.europe-west4.gcp"
export PERMISSION_BOT_WAREHOUSE="regnskap_loader"
export PERMISSION_BOT_DATABASE=${TILGANGSSTYRING_DB}
export PERMISSION_BOT_ROLE="securityadmin"
export PERMISSION_BOT_AUTHENTICATOR='externalbrowser'