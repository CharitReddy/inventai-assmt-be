from fastapi import APIRouter, Request

router = APIRouter()

# Check for connection.
@router.get("/")
async def hello_endpoint(request: Request,name: str = 'World',):
    print(f"----------------hello--------------called------\n{request}")
    return {"message": f"Hello, {name}!"}
