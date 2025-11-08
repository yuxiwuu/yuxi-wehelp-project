from typing import Annotated
from fastapi import FastAPI, Form , Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse,RedirectResponse,JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.sessions import SessionMiddleware
import csv

app=FastAPI()

app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(SessionMiddleware, secret_key="key1108")  

app.mount("/static", StaticFiles(directory="static"), name="static")
templates=Jinja2Templates(directory="templates")

@app.get("/",response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html",{"request": request})


@app.post("/login",response_class=HTMLResponse)
async def login(
    request: Request,
    email:Annotated[str,Form()],
    password:Annotated[str,Form()],
):
    if not email or not password:
        return JSONResponse({"ok":False, "msg":"請輸入信箱和密碼"})
    if email == "abc@abc.com" and password == "abc":
        request.session["logged_in"] = True
        return JSONResponse({"ok":True})
    return JSONResponse({"ok": False, "msg": "信箱或密碼輸入錯誤"})

@app.get("/member",response_class=HTMLResponse)
async def member(request:Request):
    if not request.session.get("logged_in"):
        return RedirectResponse("/",status_code=302)
    return templates.TemplateResponse("member.html",{"request":request})

@app.get("/ohoh",response_class=HTMLResponse)
async def ohoh(request:Request,msg:str="發生錯誤"):
    return templates.TemplateResponse("error.html",{"request":request, "msg": msg})

@app.get("/logout")
async def logout(request:Request):
    request.session.clear()
    return RedirectResponse("/",status_code=302)


hotels = {}
with open("hotels.csv",mode="r",newline="",encoding="utf-8") as file:
    reader=csv.reader(file)
    for index, row in enumerate(reader, start=1):
        hotels[index]={
            "cname":row[0],
            "ename":row[1],
            "phone":row[-2],
        }
        

@app.get("/hotel/{hotel_id}", response_class=HTMLResponse)
async def show_hotel(request: Request, hotel_id: int):
    hotel = hotels.get(hotel_id)
    return templates.TemplateResponse(
        "hotel.html",
        {"request":request,"hotel": hotel,"hotel_id": hotel_id},
    )
