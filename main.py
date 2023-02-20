from fastapi import FastAPI
import pandas as pd
import os
from deta import Deta
from fastapi.responses import StreamingResponse, FileResponse
from io import BytesIO

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# load deta using 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/files")
async def get_files(exchange: str = "US"):
    """
    """
    project_key = os.getenv("DETA_DRIVE_KEY")
    deta = Deta(project_key)
    drive = deta.Drive("stonk_events")
    # get files in deta
    result = drive.list()
    all_files = result.get("names")
    paging = result.get("paging")
    last = paging.get("last") if paging else None

    while (last):
        # provide last from previous call
        result = drive.list(last=last)

        all_files += result.get("names")
        # update last
        paging = result.get("paging")
        last = paging.get("last") if paging else None
    return all_files


# get file by name from deta /file/{id}
# reason it was likely failing is because of the response size limit
@app.get("/file/{id}")
async def get_file(id: str):
    project_key = os.getenv("DETA_DRIVE_KEY")
    deta = Deta(project_key)
    drive = deta.Drive("stonk_events")
    res = drive.get(id)
    return StreamingResponse(res.iter_chunks(1024), media_type="application/pdf")
