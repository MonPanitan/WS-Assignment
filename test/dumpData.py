import os
import subprocess
import shutil
from fastapi import HTTPException
from fastapi.responses import FileResponse

MONGO_URI = "mongodb://root:example@localhost:27017/"
DATABASE_NAME = "autoStock"

def dump_database():
    backup_dir = "database_dump"
    zip_file = "mongo_backup.zip"

    # Ensure backup directory exists
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    try:
        # Run mongodump with error capture
        result = subprocess.run(
            ["mongodump", "--uri", MONGO_URI, "--db", DATABASE_NAME, "--out", backup_dir],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        print("Mongodump Output:", result.stdout)
        print("Mongodump Error (if any):", result.stderr)

        # Zip the backup directory
        shutil.make_archive("mongo_backup", "zip", backup_dir)

    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Backup failed: {e.stderr}")

    return FileResponse(zip_file, filename="mongo_backup.zip", media_type="application/zip")
