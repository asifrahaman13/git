from pydantic import BaseModel


class RespositoyData(BaseModel):
    repo_name: str | None = None
