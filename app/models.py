from pydantic import BaseModel


class Secret(BaseModel):
    content: str
    passphrase: str
    delete_after_minutes: float = None
