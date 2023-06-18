from tinydb import TinyDB

db = TinyDB('bin/database.json')  # Create a TinyDB instance and specify the database file
table = db.table('playlists')