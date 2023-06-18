from typing import Union
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


clusteringAPI = FastAPI()

clusteringAPI.mount("/assets", StaticFiles(directory="templates/assets"), name="assets")
clusteringAPI.mount("/vendor", StaticFiles(directory="templates/vendor"), name="vendor")

templates = Jinja2Templates(directory="templates")

@clusteringAPI.get("/", response_class=HTMLResponse)
async def render_home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
