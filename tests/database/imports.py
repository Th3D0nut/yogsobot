import os
from os.path import join, dirname
import sqlite3

import pytest


DIR = dirname(__file__)
PATH_TO_DB = join(DIR, "test.db")
