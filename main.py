from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime
from jose import JWTError, jwt
import models
import schemas
import database
import hashing
import jwt_token as token_file

# Create all database tables on startup
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Task Manager API", version="1.0.0")

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # decode the JWT token to get the user's email (sub)
        payload = jwt.decode(token, token_file.SECRET_KEY, algorithms=[token_file.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

# ==================== LOGIN OPERATION ====================
@app.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """User login to get JWT Access Token."""
    
    # step 1: Check if the user exists in the database
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Credentials (Email not found)")
    
    # step 2: Check if the password matches using hashing.verify
    if not hashing.Hash.verify(request.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")
    
    # step 3: Generate a token and return the response
    access_token = token_file.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# ==================== USER REGISTRATION ====================
@app.post("/users/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Create a new user with a hashed password."""
    hashed_password = hashing.Hash.bcrypt(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# ==================== 1. CREATE OPERATION (Protected) ====================
@app.post("/tasks/", response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task: schemas.TaskCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    """Create a new task for the currently logged-in user."""
    db_task = models.Task(**task.model_dump(), owner_id=current_user.id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# ==================== 2. READ (ALL) OPERATION ====================
@app.get("/tasks/", response_model=list[schemas.TaskResponse])
def get_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve all tasks from the database with pagination support."""
    tasks = db.query(models.Task).offset(skip).limit(limit).all()
    return tasks

# ==================== 3. READ (SINGLE) OPERATION ====================
@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """Retrieve a single task by its unique ID."""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# ==================== 4. UPDATE OPERATION ====================
@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: int, updated_task: schemas.TaskCreate, db: Session = Depends(get_db)):
    """Update an existing task by its ID."""
    task_query = db.query(models.Task).filter(models.Task.id == task_id)
    task = task_query.first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task_query.update(updated_task.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(task)
    return task

# ==================== 5. DELETE OPERATION ====================
@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task permanently from the database by its ID."""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return None

# ==================== GET MY TASKS (Protected) ====================
@app.get("/my-tasks/", response_model=list[schemas.TaskResponse])
def get_my_tasks(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """Get tasks only for the currently logged-in user."""
    tasks = db.query(models.Task).filter(models.Task.owner_id == current_user.id).all()
    return tasks


@app.get("/my-tasks/search/", response_model=list[schemas.TaskResponse])
def search_my_tasks(
    keyword: str | None = None,
    is_completed: bool | None = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Search or filter tasks for the currently logged-in user."""
    query = db.query(models.Task).filter(models.Task.owner_id == current_user.id)
    
    # Filter by search keyword
    if keyword:
        query = query.filter(models.Task.title.contains(keyword))
        
    # Filter by completion status
    if is_completed is not None:
        query = query.filter(models.Task.is_completed == is_completed)
        
    tasks = query.all()
    return tasks

@app.get("/users/me", response_model=schemas.UserResponse)
def get_current_user_profile(current_user: models.User = Depends(get_current_user)):
    """Get the profile details of the currently logged-in user."""
    return current_user