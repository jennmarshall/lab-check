from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

import database

database.run('src/builders/build-db.sql')