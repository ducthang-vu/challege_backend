# Main script of the application. Run in terminal "uvicorn main:app" to start the server.

from tempfile import TemporaryFile

from fastapi import FastAPI, File, UploadFile, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
from challenge_backend.MobileNumber import MobileNumber


app = FastAPI(debug=True)
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def send_form_check_number(request: Request):
    """Return a HTML page with a form"""
    return templates.TemplateResponse('formCheckNumber.html', context={"request": request})


@app.post("/")
def form_post(request: Request, number: str = Form(...)):
    """Return a HTML page with the last result, and a form for further requests"""
    record = MobileNumber(None, number)
    context = {
        "request": request,
        "number": record.number,
        "response": record.number_evaluation_message
    }
    return templates.TemplateResponse('formCheckNumber.html', context=context)


@app.post("/upload-file")
async def create_upload_file(file: UploadFile = File(...)):
    """Endpoint for uploading files. Returns json."""
    chunks = pd.read_csv(file.file, chunksize=100000, dtype={'sms_phone': 'string'})
    dataframe = pd.concat(chunks)
    data_dict = {}
    storage = TemporaryFile('w+t')
    for row in dataframe.itertuples():
        try:
            record = MobileNumber(row.id, row.sms_phone)
        except KeyError:
            raise HTTPException(status_code=422, detail="File must have column lines: 'id' and 'sms_phone")
        storage.write(str(record))
        data_dict.setdefault(record.status, []).append(record)
    storage.close()
    return {"filename": file.filename, 'content': data_dict}
