from app.auth.models import AuthenticatedUser


def is_action_allowed(
    user: AuthenticatedUser,
    action: str,
) -> bool:
    if user.role == "customer":
        return action in {
            "view_own_order",
            "view_own_account",
            "cancel_own_order",
        }

    return False