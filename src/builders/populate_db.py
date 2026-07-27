import database

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

database.run('src/builders/populate-db.sql')
