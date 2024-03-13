import re
import threading
import uuid
from datetime import datetime, timedelta

import requests
from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import Response,RedirectResponse
from response import ErrorResponse
from utils.send_code import send_email
from utils.test import calculate_hash

router = APIRouter()

from mongo import db
import hashlib

from utils.serialization_profile import serialize_profile
from utils.create_token import create_token


def is_alphanumeric_underscore(input_string):
    return bool(re.match("^[A-Za-z0-9_-]*$", input_string))


def delayed_function(UserId: str):
    db("users").delete_one({"_id": UserId, "verified": False})


@router.post("/join")
async def join(request: Request, useSHA1: bool = True):
    request_data = await request.json()

    email = request_data.get("email")
    CheckLocalEmail = db("users").find_one({"email": {"$regex": f"^{email}$", "$options": "i"}})
    if CheckLocalEmail:
        raise ErrorResponse(status_code=400, cause="Email already be register!")

    username = request_data.get("username")
    if not is_alphanumeric_underscore(username):
        raise ErrorResponse(status_code=403, cause="The user name must consist of numeric, letters and \"_\"")
    CheckLocalUser = db("users").find_one({"username": {"$regex": f"^{username}$", "$options": "i"}})
    if CheckLocalUser:
        raise ErrorResponse(status_code=400, cause="Username is already exits!")
    CheckMojangUser = requests.get(f"http://api.mojang.com/users/profiles/minecraft/{username}")
    if CheckMojangUser.ok:
        raise ErrorResponse(status_code=400, cause="Username is used by mojang server!")

    password = request_data.get("password")
    if useSHA1:
        password = hashlib.sha1(password.encode())
        password = password.hexdigest()
    password = hashlib.sha256(password.encode("utf-8"))
    password = password.hexdigest()
    requestUser = request_data.get("requestUser")

    UserId = str(uuid.uuid4())
    if calculate_hash(UserId):
        skinUrl = "http://textures.minecraft.net/texture/2235c334155d2118f96a82d097e37b931c3c3b1ef13f92f19f85e107ddc4c2e5"
    else:
        skinUrl = "http://textures.minecraft.net/texture/8545513c1af03b56979583a9feefa3f0e926d388db428dcf80b9bf243fe301f5"

    db("users").insert_one(
        {"_id": UserId, "username": username, "email": email, "password": password, "textures": {
            "SKIN": {
                "url": skinUrl,
                "metadata": {
                    "model": "slim"
                }
            }
        }, "verified": False})

    db("regs").create_index("expiry_time", expireAfterSeconds=10800)
    code = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()

    _await = threading.Thread(target=send_email, args=(code, username, email, True))
    _await.start()

    db("regs").insert_one(
        {"uid": UserId, "code": code, "type": "createUser",
         "expiry_time": datetime.utcnow() + timedelta(seconds=10800)})

    timer = threading.Timer(86400, delayed_function, args=[UserId])
    timer.start()

    UserData = db("users").find_one({"username": {"$regex": f"^{username}$", "$options": "i"}})
    if UserData is None: raise ErrorResponse(status_code=403, cause="Failed to create user")

    UserProfile = serialize_profile(UserData)

    result = {
        "accessToken": create_token(UserData),
        "clientToken": None,
        "availableProfiles": [
            UserProfile
        ],
        "selectedProfile": UserProfile,
    }
    if requestUser:
        result["user"] = UserProfile

    return result


@router.get("/join/getCode")
async def send_code(request: Request):
    accessToken = request.headers.get("Authorization").split(" ")[-1]

    TokenData = db("tokens").find_one({"token": accessToken, "type": "accessToken"})
    if TokenData is None:
        raise ErrorResponse(status_code=403, cause="No login!")
    UserData = db("users").find_one({"_id": TokenData["uid"]})
    if UserData is None:
        raise ErrorResponse(status_code=403, cause="Profile Not Found!")

    db("regs").create_index("expiry_time", expireAfterSeconds=10800)
    code = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()

    if not send_email(code, UserData["username"], UserData["email"], True):
        raise ErrorResponse(status_code=403, cause="SMTP Server Error!")

    db("regs").insert_one({"uid": UserData["_id"], "code": code, "type": "createUser",
                            "expiry_time": datetime.utcnow() + timedelta(seconds=10800)})

    return Response(status_code=204)


@router.get("/verify")
async def verify_code(code: str = None):
    CodeData = db("regs").find_one({"code": code})
    if CodeData:
        db("users").update_one({"_id": CodeData["uid"]}, {"$set": {"verified": True}})
        db("regs").delete_many({"code": code})

    return RedirectResponse(url="/")
