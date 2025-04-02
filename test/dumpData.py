import subprocess
import datetime
import os
from fastapi import HTTPException
from fastapi.responses import FileResponse
import shutil


MONGO_URI = "mongodb://root:example@localhost:27017/autoStock?authSource=admin"
DATABASE_NAME = "autoStock"
DATABASE_COLLECTION = "itemList"

def dump_database():
    timestamp = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M")
    backup_dir = f"itemList_backup{timestamp}"
    zip_file = f"database_dump_{timestamp}"

    # Ensure backup directory exists
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    try:
        # Run mongodump
        result = subprocess.run(
            ["mongodump", "--uri", MONGO_URI, "--collection",DATABASE_COLLECTION,"--out", backup_dir],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        print("Mongodump Output:", result.stdout)
        print("Mongodump Error (if any):", result.stderr)

        # Zip the backup directory
        shutil.make_archive(f"database_dump_{timestamp}", "zip", backup_dir)

    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Backup failed: {e.stderr}")

    return FileResponse(zip_file, filename=zip_file, media_type="application/zip")

if __name__ == "__main__":
    dump_database()