from pydantic import BaseModel

class CustomDomainBase(BaseModel):
    domain: str

class CustomDomainCreate(CustomDomainBase):
    pass

class CustomDomain(CustomDomainBase):
    id: int
    tenant_id: int
    tls_status: str

    class Config:
        orm_mode = True
