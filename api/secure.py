import string
import uuid
from datetime import timedelta, datetime
import random

from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import Response
from response import ErrorResponse
from utils.send_code import send_email, send_password

router = APIRouter()

from mongo import db
import hashlib


@router.post("/user/secure/password")
async def change_password(request: Request):
    request_data = await request.json()
    accessToken = request.headers.get("Authorization").split(" ")[-1]

    TokenData = db("tokens").find_one({"token": accessToken, "type": "accessToken"})
    if TokenData is None:
        raise ErrorResponse(status_code=403, cause="No login!")
    UserData = db("users").find_one({"_id": TokenData["uid"]})
    if UserData is None:
        raise ErrorResponse(status_code=403, cause="Profile Not Found!")

    _pwd1 = str(request_data["pwd1"]).encode("utf-8")
    _pwd2 = str(request_data["pwd2"]).encode("utf-8")

    pwd1 = hashlib.sha256(hashlib.sha1(_pwd1).hexdigest().encode()).hexdigest()
    pwd2 = hashlib.sha256(hashlib.sha1(_pwd2).hexdigest().encode()).hexdigest()
    if pwd1 != pwd2: raise ErrorResponse(status_code=403, cause="Password not same!")

    db("users").update_one({"_id": UserData["_id"]}, {"$set": {"password": pwd1}})
    db("tokens").delete_many({"uid": UserData["_id"]})

    return Response(status_code=204)


@router.post("/user/secure/email/code")
async def send_code(request: Request):
    request_data = await request.json()
    accessToken = request.headers.get("Authorization").split(" ")[-1]

    TokenData = db("tokens").find_one({"token": accessToken, "type": "accessToken"})
    if TokenData is None:
        raise ErrorResponse(status_code=403, cause="No login!")
    UserData = db("users").find_one({"_id": TokenData["uid"]})
    if UserData is None:
        raise ErrorResponse(status_code=403, cause="Profile Not Found!")

    email = request_data["email"]

    try:
        db("codes").create_index("expiry_time", expireAfterSeconds=3600)
    except:
        pass
    code = str(uuid.uuid4())[0:6]

    if not send_email(code, UserData["username"], email):
        raise ErrorResponse(status_code=403, cause="SMTP Server Error!")

    db("codes").insert_one(
        {"uid": UserData["_id"], "code": code, "type": "updateEmail", "email": email,
         "expiry_time": datetime.utcnow() + timedelta(seconds=3600)})

    return Response(status_code=204)


@router.post("/user/secure/email")
async def send_code(request: Request):
    request_data = await request.json()
    accessToken = request.headers.get("Authorization").split(" ")[-1]

    TokenData = db("tokens").find_one({"token": accessToken, "type": "accessToken"})
    if TokenData is None:
        raise ErrorResponse(status_code=403, cause="No login!")
    UserData = db("users").find_one({"_id": TokenData["uid"]})
    if UserData is None:
        raise ErrorResponse(status_code=403, cause="Profile Not Found!")

    email = request_data["email"]
    code = request_data["code"]

    CodeData = db("codes").find_one({"uid": UserData["_id"], "code": code, "type": "updateEmail", "email": email})
    if CodeData is None:
        raise ErrorResponse(status_code=403, cause="Code or Email error!")

    db("users").update_one({"_id": UserData["_id"]}, {"$set": {"email": email, "verified": True}})
    db("codes").delete_many({"code": code})

    return Response(status_code=204)


@router.post("/user/secure/password/reset")
async def change_password(request: Request):
    request_data = await request.json()
    email = request_data["email"]

    UserData = db("users").find_one({"email": {"$regex": f"^{email}$", "$options": "i"}})
    if UserData is None:
        raise ErrorResponse(status_code=403,
                            cause="Email not found! Reset password must input you email, CANNOT ENTER USERNAME!!!")

    new_pwd = generate_random_string(random.randint(10, 15))

    if not send_password(new_pwd, UserData["username"], email):
        raise ErrorResponse(status_code=403, cause="SMTP Server Error!")
    hash_pwd = hashlib.sha256(hashlib.sha1(new_pwd.encode()).hexdigest().encode()).hexdigest()

    db("users").update_one({"_id": UserData["_id"]}, {"$set": {"password": hash_pwd}})

    return Response(status_code=204)


special_chars = "@#$%^&*()!{}[]:\";'<>,.?/"
all_chars = string.ascii_letters + string.digits + special_chars


def generate_random_string(length):
    return ''.join(random.choice(all_chars) for _ in range(length))
