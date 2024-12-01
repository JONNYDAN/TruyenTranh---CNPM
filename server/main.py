from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from bson import ObjectId
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả các nguồn, có thể giới hạn theo cần thiết
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các phương thức
    allow_headers=["*"],  # Cho phép tất cả các header
)

# Cấu hình MongoDB và mật khẩu
MONGO_URI = "mongodb://localhost:27017/"  # Đảm bảo MongoDB đang chạy ở địa chỉ này
DATABASE_NAME = "transcriptions_db"
COLLECTION_NAME = "transcriptions"

client = AsyncIOMotorClient(MONGO_URI)
db = client[DATABASE_NAME]
users_collection = db[COLLECTION_NAME]

# Tạo đối tượng CryptContext để mã hóa mật khẩu
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Mô hình Pydantic cho đăng nhập và đăng ký
class LoginUser(BaseModel):
    email: EmailStr
    password: str

class UserInDB(LoginUser):
    hashed_password: str
    
class CheckUser(BaseModel):
    username: str
    email: EmailStr
 
class RegisterUser(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    password: str

# Hàm mã hóa mật khẩu
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Hàm kiểm tra mật khẩu
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


@app.post("/register/")
async def register(user: RegisterUser):
    # Kiểm tra xem người dùng đã tồn tại chưa
    existing_user = await users_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    existing_email = await users_collection.find_one({"email": user.email})
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)
    new_user = {
        "username": user.username,
        "password": hashed_password,  # Lưu mật khẩu đã mã hóa
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "role": "user",
        "status": "active",
        "created_date": datetime.utcnow().isoformat(),
    }
    
    result = await users_collection.insert_one(new_user)
    return {"message": "User registered successfully", "user_id": str(result.inserted_id)}

@app.post("/login/")
async def login(user: LoginUser):
    # Tìm người dùng theo email
    existing_user = await users_collection.find_one({"email": user.email})  # Sử dụng trường email
    if not existing_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Kiểm tra mật khẩu
    if not verify_password(user.password, existing_user["password"]):  # Kiểm tra trường 'password'
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    return {"message": "Login successful", "user": existing_user["email"]}  # Trả về email người dùng đăng nhập

@app.post("/check_user/")
async def check_user(user: CheckUser):
    print(user)
    existing_user = await users_collection.find_one({"username": user.username})
    existing_email = await users_collection.find_one({"email": user.email})
    return {"exists": bool(existing_user or existing_email)}


# Hàm để lấy dữ liệu người dùng (dành cho mục đích tham khảo)
@app.get("/users/{user_id}")
async def get_user(user_id: str):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return {"username": user["username"], "email": user["email"]}
    raise HTTPException(status_code=404, detail="User not found")
