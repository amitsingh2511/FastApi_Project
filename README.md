# FastApi_Project

# In This project two module Customes and memo generator for image uploading and downloading.

# Step 1 : Download the requirements of projects
command :- pip install -r requirements.txt

# Step 2 : checkout src file
command :- cd src
# Step 3 : Command for run project
Command :- python -m uvicorn app.main:app --workers 1 --host 0.0.0.0 --port 8000

# Step 4 : upload the image using this curl and with web also
Curl for upload image :- curl --location 'localhost:8000/fastapi-project/v1/image' \
--form 'name="amit"' \
--form 'file=@"/C:/Users/Amit Singh/OneDrive/Pictures/pic 2.png"'

# Step 5 : Download the image using this curl and with web also
Curl for download image :- curl --location 'localhost:8000/fastapi-project/v1/image/2'