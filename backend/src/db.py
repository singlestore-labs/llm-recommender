import singlestoredb as s2

from src.constants import DB_CONNECTION_URL

db_connection = s2.connect(DB_CONNECTION_URL)
