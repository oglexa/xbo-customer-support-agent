from auth import CURRENT_AUTHENTICATED_USER

MOCK_USERS = {
    "user_123": {
        "status": "verified",
        "balance": 15200,
        "transactions": [
            {
                "id": "tx_001",
                "type": "withdrawal",
                "amount": 500
            },
            {
                "id": "tx_002",
                "type": "deposit",
                "amount": 2000
            }
        ]
    },
    "user_999": {
        "status": "frozen",
        "balance": 0,
        "transactions": []
    }
}


class UnauthorizedError(Exception):
    pass


def validate_user(requested_user_id: str):
    if requested_user_id != CURRENT_AUTHENTICATED_USER:
        raise UnauthorizedError(
            "Unauthorized access attempt"
        )


def get_account_status(user_id: str):
    validate_user(user_id)

    return {
        "user_id": user_id,
        "status": MOCK_USERS[user_id]["status"],
        "balance": MOCK_USERS[user_id]["balance"]
    }


def get_recent_transactions(user_id: str, limit: int = 10):
    validate_user(user_id)

    return MOCK_USERS[user_id]["transactions"][:limit]
