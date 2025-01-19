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

#### 2. Rate Limiting
The application uses rate limiting to prevent abuse and denial-of-service attacks. The rate limiting is implemented using the Limiter class from the limits library:

```python
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

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


### From auth.py

####1. Password Hashing
The application uses secure password hashing to store user passwords. This is implemented using the bcrypt library:

```python
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
def get_password_hash(password):
    return pwd_context.hash(password)

####2. JWT Authentication
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



Reporting a Vulnerability
If you discover any security vulnerabilities, please report them to the project maintainers immediately. We take security issues seriously and will address them promptly.

License
This project is licensed under the MIT License. 