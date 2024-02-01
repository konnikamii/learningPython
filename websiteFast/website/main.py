from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="websiteFast/static"), name="static")

# Define the path to the templates folder
templates = Jinja2Templates(directory="websiteFast/templates")


@app.get("/")
async def read_root(request: Request):
    # Use the Jinja2 template to render the HTML page
    return templates.TemplateResponse("base.html", {"request": request})
