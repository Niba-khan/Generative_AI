from fastapi import FastAPI, Depends, Query, HTTPException, status
from typing import Annotated

# Initialize FastAPI app
app: FastAPI = FastAPI(title="Dependency Injection Demo")

# ✅ Added Root Route
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Dependency Injection Demo!"}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 1. Basic Dependency
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_simple_goal():
    return {"goal": "We are building AI Agents Workforce"}
    
@app.get("/get-simple-goal")
def simple_goal(response: Annotated[dict, Depends(get_simple_goal)]):
    return response

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 2. Dependency with Parameter
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_goal(username: str):
    return {"goal": "We are building AI Agents Workforce", "username": username}
    
@app.get("/get-goal")
def get_my_goal(response: Annotated[dict, Depends(get_goal)]):
    return response

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3. Dependency with Query Parameters
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def dep_login(username: str = Query(None), password: str = Query(None)):
    if username == "admin" and password == "admin":
        return {"message": "Login Successful"}
    else:
        return {"message": "Login Failed"}
    
@app.get("/signin")
def login_api(user: Annotated[dict, Depends(dep_login)]):
    return user

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 4. Multiple Dependencies
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def depfunc1(num: int): 
    num = int(num)
    num += 1
    return num

def depfunc2(num: int): 
    num = int(num)
    num += 2
    return num

@app.get("/main/{num}")
def get_main(
    num: int, 
    num1: Annotated[int, Depends(depfunc1)], 
    num2: Annotated[int, Depends(depfunc2)]
):
    total = num + num1 + num2
    return f"Pakistan {total}"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 5. Class-based Dependencies
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
blogs = {
    "1": "Generative AI Blog",
    "2": "Machine Learning Blog",
    "3": "Deep Learning Blog"
}

users = {
    "8": "Niba",
    "9": "Farooq"
}

class GetObjectOr404:
    def __init__(self, model) -> None:
        self.model = model

    def __call__(self, id: str):
        obj = self.model.get(id)
        if not obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Object ID {id} not found"
            )
        return obj

blog_dependency = GetObjectOr404(blogs)
user_dependency = GetObjectOr404(users)

@app.get("/blog/{id}")
def get_blog(blog_name: Annotated[str, Depends(blog_dependency)]):
    return blog_name

@app.get("/user/{id}")
def get_user(user_name: Annotated[str, Depends(user_dependency)]):
    return user_name

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 6. Sub-dependencies
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_db_connection():
    print("Getting DB connection")
    return {"db_connection": "active"}

def get_current_user(db: Annotated[dict, Depends(get_db_connection)]):
    print("Getting current user")
    return {"user_id": "123", "username": "admin", "db_status": db["db_connection"]}

@app.get("/profile")
def user_profile(user: Annotated[dict, Depends(get_current_user)]):
    return {"message": "User profile", "user_data": user}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 7. Dependency in Decorator
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def verify_token(token: str = Query(...)):
    if token != "secret":
        raise HTTPException(status_code=400, detail="Invalid token")
    return {"token": token}

@app.get("/secure", dependencies=[Depends(verify_token)])
def secure_endpoint():
    return {"message": "This is a secure endpoint"}

# ✅ Entry Point
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
