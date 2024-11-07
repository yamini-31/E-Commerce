import jwt
from datetime import datetime, timedelta
from django.conf import settings
from functools import wraps
from django.http import JsonResponse

# Secret key for encoding/decoding tokens (add a secret key in your settings.py)
SECRET_KEY = settings.SECRET_KEY

def generate_jwt_token(customer):
    """Generate a JWT token containing customer data with a specific expiration time."""
    expiration_time = datetime.utcnow() + timedelta(hours=10)  # Set expiration to 10 hours
    payload = {
        "user_id": customer.id,
        "customer_name": customer.customer_name,
        "customer_address": customer.customer_address,
        "customer_phoneNo": customer.customer_phoneNo,
        "customer_username": customer.customer_username,
        "exp": expiration_time,
        "iat": datetime.utcnow()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def decode_jwt_token(token):
    """Decode the JWT token to get the payload, if valid."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token
    
def auth_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        # Get the Authorization header
        auth_header = request.headers.get("Authorization")
        
        if auth_header and auth_header.startswith("Bearer "):
            # Extract the token
            token = auth_header.split(" ")[1]
            # Decode the JWT token
            payload = decode_jwt_token(token)
            
            if payload is None:
                return JsonResponse({"error": "Token is invalid or expired"}, status=401)
            
            # Optionally pass payload to the view
            request.payload = payload  # Add the payload to the request for access in the view
            return func(request, *args, **kwargs)  # Call the original function
        else:
            return JsonResponse({"error": "Token is invalid or expired"}, status=401)
    
    return wrapper
