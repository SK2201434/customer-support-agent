from fastapi import FastAPI, HTTPException, Depends
from langchain_core.messages import HumanMessage
from langgraph.types import Command

from app.agent.graph import graph
from app.api.models import (
    ChatRequest,
    ChatResponse,
    RegisterRequest,
    LoginRequest,
    AuthResponse,
    ApprovalRequest,
)
from app.auth.dependencies import get_current_user
from app.auth.models import AuthenticatedUser
from app.auth.service import AuthenticationService
from app.database.connection import get_connection
from app.guardrails.pipeline import check_guardrail
from app.guardrails.result import GuardrailDecision
from app.repositories.conversation import ConversationRepository
from app.repositories.user import UserRepository
from app.services.conversation import ConversationService


app = FastAPI(
    title="Customer Support Agent",
    version="1.0.0",
)


# ---------------------------------------------------------
# Services
# ---------------------------------------------------------

auth_service = AuthenticationService(
    UserRepository()
)

conversation_service = ConversationService(
    ConversationRepository()
)


# ---------------------------------------------------------
# Health
# ---------------------------------------------------------

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "customer-support-agent",
    }


# ---------------------------------------------------------
# Authentication
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# Chat
# ---------------------------------------------------------

@app.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    current_user: AuthenticatedUser = Depends(get_current_user),
):
    # -----------------------------------------------------
    # 1. Guardrail check
    # -----------------------------------------------------

    guardrail_result = check_guardrail(
        request.message
    )

    if guardrail_result.decision == GuardrailDecision.BLOCK:
        return ChatResponse(
            response="I can't help with that request."
        )

    if guardrail_result.decision == GuardrailDecision.OUT_OF_SCOPE:
        return ChatResponse(
            response=(
                "I can only help with customer support requests "
                "such as orders, accounts, subscriptions, products, "
                "and services."
            )
        )

    # -----------------------------------------------------
    # 2. Resolve conversation
    # -----------------------------------------------------

    if request.thread_id is None:
        # New conversation
        conversation = conversation_service.create_conversation(
            current_user.user_id
        )

        thread_id = conversation["id"]

    else:
        # Existing conversation
        conversation = conversation_service.get_conversation(
            request.thread_id
        )

        if conversation is None:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found.",
            )

        if conversation["user_id"] != current_user.user_id:
            raise HTTPException(
                status_code=403,
                detail=(
                    "You are not authorized to access "
                    "this conversation."
                ),
            )

        thread_id = request.thread_id

    # -----------------------------------------------------
    # 3. Invoke LangGraph
    # -----------------------------------------------------

    result = graph.invoke(
        {
            "messages": [
                HumanMessage(
                    content=request.message
                )
            ],
            "user": current_user,
        },
        config={
            "configurable": {
                "thread_id": thread_id,
            }
        },
    )

    # -----------------------------------------------------
    # 4. LangGraph paused for human approval
    # -----------------------------------------------------

    if "__interrupt__" in result:
        interrupt_data = result["__interrupt__"][0]

        return ChatResponse(
            response=interrupt_data.value["message"],
            approval_required=True,
            approval_request=interrupt_data.value,
            thread_id=thread_id,
        )

    # -----------------------------------------------------
    # 5. Normal response
    # -----------------------------------------------------

    final_message = result["messages"][-1]

    return ChatResponse(
        response=final_message.content,
        approval_required=False,
        thread_id=thread_id,
    )


# ---------------------------------------------------------
# Chat approval
# ---------------------------------------------------------

@app.post(
    "/chat/approval/{thread_id}",
    response_model=ChatResponse,
)
def approve_chat_action(
    thread_id: str,
    request: ApprovalRequest,
    current_user: AuthenticatedUser = Depends(
        get_current_user
    ),
):
    # -----------------------------------------------------
    # 1. Verify conversation exists
    # -----------------------------------------------------

    conversation = conversation_service.get_conversation(
        thread_id
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found.",
        )

    # -----------------------------------------------------
    # 2. Verify conversation ownership
    # -----------------------------------------------------

    if conversation["user_id"] != current_user.user_id:
        raise HTTPException(
            status_code=403,
            detail=(
                "You are not authorized to resume "
                "this conversation."
            ),
        )

    # -----------------------------------------------------
    # 3. Resume LangGraph
    # -----------------------------------------------------

    result = graph.invoke(
        Command(
            resume=request.approved
        ),
        config={
            "configurable": {
                "thread_id": thread_id,
            }
        },
    )

    # -----------------------------------------------------
    # 4. Another approval is required
    # -----------------------------------------------------

    if "__interrupt__" in result:
        interrupt_data = result["__interrupt__"][0]

        return ChatResponse(
            response=interrupt_data.value["message"],
            approval_required=True,
            approval_request=interrupt_data.value,
            thread_id=thread_id,
        )

    # -----------------------------------------------------
    # 5. Final response after approval/decline
    # -----------------------------------------------------

    final_message = result["messages"][-1]

    return ChatResponse(
        response=final_message.content,
        approval_required=False,
        thread_id=thread_id,
    )