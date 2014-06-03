#!/usr/bin/env python
from migrate.versioning import api
from config import SQLALCHEMY_DATABSE_URI
from config import SQLALCHEMY_MIGRATE_REPO
api.upgrade(SQLALCHEMY_DATABSE_URI, SQLALCHEMY_MIGRATE_REPO)
print 'Current database versionl ' + str(api.db_version(SQLALCHEMY_DATABSE_URI, SQLALCHEMY_MIGRATE_REPO))
