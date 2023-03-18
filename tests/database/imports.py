import os
from os.path import join, dirname
import sqlite3

import pytest


PATH_TO_DB = join(dirname(__file__), "test.db")
