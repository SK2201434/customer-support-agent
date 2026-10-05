from fastapi import FastAPI

from app.agent.graph import graph
from app.api.models import ChatRequest, ChatResponse
from app.auth.models import AuthenticatedUser
from langchain_core.messages import HumanMessage
from app.api.models import (ChatRequest, ChatResponse,RegisterRequest)
from app.auth.service import AuthenticationService
from app.repositories.user import UserRepository


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

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    result = graph.invoke(
        {
            "messages": [
                HumanMessage(content=request.message)
            ],
            "user": AuthenticatedUser(
                user_id=request.user_id,
                role=request.role,
            ),
        },
        config={
            "configurable": {
                "thread_id": f"api-{request.user_id}",
            }
        },
    )

    final_message = result["messages"][-1]

    return ChatResponse(
        response=final_message.content,
    )