# src/application/web/controllers/user_controller.py

from fastapi import APIRouter, Depends, HTTPException, Header, status
from src.domain.entities.user import RespositoyData
from src.domain.interfaces.user_interface import UserInterface
from src.domain.use_cases.user_service import UserService
from src.infastructure.repositories.user_repository import UserRepository
from src.infastructure.repositories.auth_repository import AuthRepository
from src.domain.use_cases.auth_service import AuthenticationService
from src.domain.interfaces.auth_interface import AuthInterface

router = APIRouter()
user_repository = UserRepository()
user_service = UserService(user_repository)
auth_repository = AuthRepository()
auth_service = AuthenticationService()


@router.get("/repositories")
async def get_repositories(authorization: str = Header(...), user_interface: UserInterface = Depends(user_service)):
    try:
        access_token = authorization.split(" ")[1]  # Extract the token part from the Authorization header
        repositories = user_interface.fetch_all_respositories(access_token)
        return repositories
    except HTTPException as http_exception:
        # Handle HTTP exceptions
        return http_exception
    except Exception as e:
        # Handle other exceptions
        print(e)
        return HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/dependencies")
async def get_dependencies(repo: RespositoyData, authorization: str = Header(...), user_interface: UserInterface = Depends(user_service), auth_interface: AuthInterface = Depends(auth_service)):
    try:
        access_token = authorization.split(" ")[1]
        is_authenticated = auth_interface.verifiy_the_login(access_token)
        print(is_authenticated)
        if not is_authenticated:
            raise HTTPException(status_code=401, detail="Unauthorized")

        required_xml_dependencies = user_interface.fetch_all_dependencies(access_token, repo)

        if(required_xml_dependencies==False):
            return {"status":False,"xmlData":required_xml_dependencies}
        
        return {"status":True,"xmlData":required_xml_dependencies}

    except HTTPException as http_exception:
        # Handle HTTP exceptions
        return http_exception

    except Exception as e:
        # Handle other exceptions
        print(e)
        return HTTPException(status_code=500, detail="Internal Server Error")
