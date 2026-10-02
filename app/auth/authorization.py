from app.auth.models import AuthenticatedUser
from app.policy.policy import is_action_allowed

def is_allowed(
        user: AuthenticatedUser,action:str
)->bool:
    return is_action_allowed(user, action)