blacklisted_tokens = set()  # Store revoked tokens

def blacklist_token(token):
    """Add token to blacklist."""
    blacklisted_tokens.add(token)

def is_token_blacklisted(token):
    """Check if token is blacklisted."""
    return token in blacklisted_tokens

