from fastapi import FastAPI,HTTPException,Depends   

from app.agent.graph import graph
from app.api.models import ChatRequest, ChatResponse
from app.auth.models import AuthenticatedUser
from langchain_core.messages import HumanMessage
from app.api.models import (ChatRequest, ChatResponse,RegisterRequest,LoginRequest,AuthResponse,)
from app.auth.service import AuthenticationService
from app.repositories.user import UserRepository
from app.auth.dependencies import get_current_user



app = FastAPI(
    title="Customer Support Agent",
    version="1.0.0",
)

auth_service = AuthenticationService(
    UserRepository()
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "customer-support-agent",
    }

@app.post("/auth/register")
def register(request: RegisterRequest):
    try:
        user = auth_service.register_user(
            email=request.email,
            password=request.password,
        )

        return {
            "message": "User registered successfully.",
            "user_id": user["id"],
            "email": user["email"],
            "role": user["role"],
        }

    except ValueError as error:
        return {
            "error": str(error),
        }

@app.post("/auth/login", response_model=AuthResponse)
def login(request: LoginRequest):
    token = auth_service.login_user(
        email=request.email,
        password=request.password,
    )

    if token is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password.",
        )

    return AuthResponse(
        access_token=token,
    )

@app.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    current_user: AuthenticatedUser = Depends(get_current_user),
):
    result = graph.invoke(
        {
            "messages": [
                HumanMessage(content=request.message)
            ],
            "user": current_user,
        },
        config={
            "configurable": {
                "thread_id": f"api-{current_user.user_id}",
            }
        },
    )

    final_message = result["messages"][-1]

    return ChatResponse(
        response=final_message.content,
    )