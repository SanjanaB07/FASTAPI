from fastapi.responses import JSONResponse

USER = "admin"
PASS = "1234"


def validate_auth(request):
    header = request.headers.get("Authorization")

    if header == f"{USER}:{PASS}":
        return {"user": USER}

    return None
