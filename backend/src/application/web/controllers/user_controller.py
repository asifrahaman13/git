# src/application/web/controllers/user_controller.py

from fastapi import APIRouter, Depends, HTTPException, Header, status
from src.domain.use_cases.auth_service import AuthenticationService
from src.domain.interfaces.auth_interface import AuthInterface
from fastapi.responses import RedirectResponse

router = APIRouter()

auth_service = AuthenticationService()


@router.get("/callback")
async def authenticate(code: str, auth_interface: AuthInterface = Depends(auth_service)):
    try:
        redirect_url = auth_interface.authenticate_user(code)
        return RedirectResponse(redirect_url)

    except HTTPException as http_exception:
        # Handle HTTP exceptions
        return http_exception

    except Exception as e:
        # Handle other exceptions
        print(e)
        return HTTPException(status_code=500, detail="Internal Server Error")
