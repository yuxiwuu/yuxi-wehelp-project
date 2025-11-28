from typing import Annotated
from fastapi import FastAPI,Request,Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,RedirectResponse,JSONResponse
from starlette.middleware.sessions import SessionMiddleware 

from dotenv import load_dotenv
import os

load_dotenv()

import mysql.connector
from mysql.connector import errorcode

app=FastAPI()

app.add_middleware(SessionMiddleware, os.getenv("SECRET_KEY"))

app.mount("/static",StaticFiles(directory="static"),name="static")
templates=Jinja2Templates(directory="templates")

def get_connection():
    try:
        cnx = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        return cnx
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("帳號或密碼錯誤")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("資料庫不存在")
        else:
            print(err)
        return None
    
@app.get("/",response_class=HTMLResponse)
async def home(request:Request):
    return templates.TemplateResponse("home.html",{"request":request})

@app.post("/signup",response_class=HTMLResponse)
async def signup(
    request:Request,
    name:Annotated[str, Form()],
    email:Annotated[str,Form()],
    password:Annotated[str,Form()],
):
    if not name or not email or not password:
        return JSONResponse ({"ok":False, "msg":"請確認資料是否填寫完整"})
    
    cnx=get_connection()
    cursor=cnx.cursor()
    query="SELECT id FROM member WHERE email = %s"
    cursor.execute(query,(email,))

    exists=False
    for row in cursor:
        exists = True
        break
    if exists:
        return JSONResponse ({"ok":False, "msg":"重複的電子郵件"})
    
    insert_query=("INSERT INTO member(name,email,password) VALUES (%s, %s, %s)")
    cursor.execute(insert_query,(name,email,password))
    cnx.commit()

    cursor.close()
    cnx.close()

    return JSONResponse({"ok": True})

@app.post("/login",response_class=HTMLResponse)
async def login(
    request:Request,
    email:Annotated[str,Form()],
    password:Annotated[str,Form()],
):
    if not email or not password:
        return JSONResponse({"ok":False,"msg":"請輸入信箱和密碼"})
    
    cnx=get_connection()
    cursor=cnx.cursor()
    query=("SELECT id, name, email FROM member "
           "WHERE email = %s AND password = %s")
    cursor.execute(query,(email, password))

    user=None
    for (id,name,email) in cursor:
        user={"id":id,"name":name,"email":email}
        break

    cursor.close()
    cnx.close()

    if not user:
        return JSONResponse({"ok": False, "msg": "信箱或密碼輸入錯誤"})
    
    request.session["logged_in"] = True
    request.session["user_id"] = user["id"]
    request.session["name"]=user["name"]
    request.session["email"]=user["email"]
    return JSONResponse({"ok":True})

@app.get("/logout")
async def logout(request:Request):
    request.session.clear()
    return RedirectResponse("/",status_code=302)

@app.get("/member",response_class=HTMLResponse)
async def member(request:Request):
    if not request.session.get("logged_in"):
        return RedirectResponse("/",status_code=302)
    name=request.session.get("name")
    user_id=request.session.get("user_id")
    messages=[]
    cnx=get_connection()
    cursor=cnx.cursor()
    query=("SELECT message.id,member.name,message.content,message.member_id "
           "FROM message JOIN member ON message.member_id =member.id "
           "ORDER BY message.id DESC"
           )
    cursor.execute(query)
    for (message_id, author_name, content, member_id) in cursor:
        messages.append(
            {
            "id":message_id,
            "name": author_name,
            "content":content,
            "member_id":member_id,
            }
        )
    cursor.close()
    cnx.close()

    return templates.TemplateResponse(
        "member.html",
        {
            "request":request,
            "name": name,
            "messages":messages,
            "user_id":user_id,
        },
    )

@app.get("/api/member/search_log")
async def get_search_log(request:Request):
    if not request.session.get("user_id"):
        return JSONResponse({"data": None})
    user_id = request.session.get("user_id")

    cnx=get_connection()
    cursor=cnx.cursor()

    query = """SELECT member.name, memberSearch.search_time FROM memberSearch
            INNER JOIN member on memberSearch.searcher_id = member.id
            WHERE memberSearch.target_id = %s
            ORDER BY memberSearch.search_time DESC LIMIT 10"""
    cursor.execute(query,(user_id,))

    logs = []
    for (name,search_time) in cursor:
        logs.append({
            "name":name,
            "time":str(search_time)
        })
    
    cursor.close()
    cnx.close()

    return JSONResponse({"data":logs})

@app.get("/api/member/{id}")
async def show_memberId(request:Request,id:int):
    if not request.session.get("user_id"):
        return JSONResponse({"data": None})
    current_user_id = request.session.get("user_id")
    
    cnx=get_connection()
    cursor=cnx.cursor()

    query="SELECT id, name, email FROM member WHERE id= %s"
    cursor.execute(query, (id,))

    user=None
    for (id,name,email) in cursor:
        user={"id":id,"name":name,"email":email}
        break

    if user == None:
        cursor.close()
        cnx.close()
        return JSONResponse({"data": None})
    
    if current_user_id != id:
        log_query = "iNSERT INTO memberSearch (searcher_id,target_id) VALUES (%s, %s)"
        cursor.execute(log_query,(current_user_id,id))
        cnx.commit()
    
    cursor.close()
    cnx.close()

    return JSONResponse({"data":user})

    
@app.patch("/api/member")
async def update_member(request:Request):
    if not request.session.get("user_id"):
        return JSONResponse({"error": True})
    
    data = await request.json()
    new_name=data["name"]

    if not new_name:
        return JSONResponse({"error":True})
    
    user_id = request.session.get("user_id")
    cnx = get_connection()
    cursor = cnx.cursor()

    check_query = "SELECT id FROM member WHERE name= %s AND id!= %s"
    cursor.execute(check_query,(new_name,user_id))
    exists=False
    for (other_id) in cursor:
        exists = True
        break
    if exists:
        cursor.close()
        cnx.close()
        return JSONResponse({"error": True, "msg": "姓名已被使用"})

    query = "UPDATE member SET name= %s WHERE id= %s"
    cursor.execute(query,(new_name,user_id))
    cnx.commit()

    cursor.close()
    cnx.close()

    request.session["name"] = new_name
    return JSONResponse({"ok": True})


@app.get("/ohoh",response_class=HTMLResponse)
async def ohoh(request:Request,msg:str="發生錯誤"):
    return templates.TemplateResponse("error.html",{"request":request,"msg":msg})
