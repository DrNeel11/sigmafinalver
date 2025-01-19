# Security Policy

## Secure Coding Practices

This project follows several secure coding practices to ensure the security and integrity of the application.

### From `app.py`

#### 1. Content Security Policy (CSP)
The application sets a Content Security Policy (CSP) to prevent various types of attacks such as Cross-Site Scripting (XSS) and data injection attacks. The CSP is defined as follows:
```python
response.headers["Content-Security-Policy"] = (
    "default-src 'self'; "
    "img-src 'self' data: https://fastapi.tiangolo.com; "
    "connect-src 'self'; "
    "font-src 'self' https://fonts.gstatic.com; "
    "form-action 'self'; "
    "base-uri 'self';"
)
```
#### 2. Rate Limiting
The application uses rate limiting to prevent abuse and denial-of-service attacks. The rate limiting is implemented using the Limiter class from the limits library:

```python
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
```
#### 3. Logging
The application uses logging to record important events and errors. Logging is configured to write logs to both a file and the console:

```python
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  
        logging.StreamHandler(),         
    ],
)
logger = logging.getLogger("fastapi-app")
```

#### 4. Request Logging Middleware
The application includes middleware to log incoming HTTP requests. This helps in monitoring and detecting any suspicious activities:

```python
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```
5. API Documentation
The application uses Swagger to document the API. This is automatically provided by FastAPI and can be accessed at /docs.

### From auth.py

1. Password Hashing
The application uses secure password hashing to store user passwords. This is implemented using the bcrypt library:

```python
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
def get_password_hash(password):
    return pwd_context.hash(password)
```
2. JWT Authentication
The application uses JSON Web Tokens (JWT) for secure authentication. This ensures that user sessions are securely managed
```python
from jose import JWTError, jwt
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```
### From routes.py

1. Input Sanitization
The application sanitizes user input to prevent injection attacks. This is done using the bleach library:
```python
import bleach

@router.post("/")
async def create_user(user: User):
    sanitized_username = bleach.clean(user.username)
    sanitized_email = bleach.clean(user.email)
    user.password = hash_password(user.password)
    user_dict = dict(user)
    user_dict["username"] = sanitized_username
    user_dict["email"] = sanitized_email
    result = collection.insert_one(user_dict)
    new_user = collection.find_one({"_id": result.inserted_id})
    return one_user(new_user)
```
2. Generic Error Messages
The application returns generic error messages to avoid exposing sensitive information:
```python
if not user:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
```

### From users.py

1. Input Validation
The application uses Pydantic's Field to enforce constraints on user input, such as minimum and maximum lengths for strings. This helps in preventing invalid data from being processed:
```python
from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str
    password: str = Field(..., min_length=6)
    disabled: Optional[bool] = None
```
2. Separation of Concerns
The application separates the user model used for input (User) from the model used for storing in the database (UserInDB). This helps in ensuring that sensitive information like hashed passwords are not exposed unnecessarily:
```python
class UserInDB(User):
    hashed_password: str
```
Reporting a Vulnerability
If you discover any security vulnerabilities, please report them to the project maintainers immediately. We take security issues seriously and will address them promptly.

License
This project is licensed under the MIT License. 
