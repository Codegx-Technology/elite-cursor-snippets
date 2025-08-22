from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from auth.user_models import Tenant
from auth.auth_service import get_current_active_user
from database import get_db
from . import schemas

router = APIRouter()

@router.get("/custom-domain", response_model=schemas.CustomDomain)
async def get_custom_domain(db: Session = Depends(get_db), current_user: Tenant = Depends(get_current_active_user)):
    tenant = db.query(Tenant).filter(Tenant.id == current_user.tenant_id).first()
    if not tenant or not tenant.custom_domain:
        raise HTTPException(status_code=404, detail="Custom domain not found")
    return tenant

@router.post("/custom-domain", response_model=schemas.CustomDomain)
async def set_custom_domain(domain: schemas.CustomDomainCreate, db: Session = Depends(get_db), current_user: Tenant = Depends(get_current_active_user)):
    tenant = db.query(Tenant).filter(Tenant.id == current_user.tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    tenant.custom_domain = domain.domain
    tenant.tls_status = "pending"
    db.add(tenant)
    db.commit()
    db.refresh(tenant)

    # Here you would trigger the TLS provisioning process
    # For now, we will just simulate it with a delay
    # and then update the status to "active"
    import asyncio
    async def provision_tls():
        await asyncio.sleep(5)
        tenant.tls_status = "active"
        db.add(tenant)
        db.commit()
    asyncio.create_task(provision_tls())

    return tenant

@router.delete("/custom-domain")
async def delete_custom_domain(db: Session = Depends(get_db), current_user: Tenant = Depends(get_current_active_user)):
    tenant = db.query(Tenant).filter(Tenant.id == current_user.tenant_id).first()
    if not tenant or not tenant.custom_domain:
        raise HTTPException(status_code=404, detail="Custom domain not found")
    
    tenant.custom_domain = None
    tenant.tls_status = "pending"
    db.add(tenant)
    db.commit()

    return {"message": "Custom domain deleted"}
