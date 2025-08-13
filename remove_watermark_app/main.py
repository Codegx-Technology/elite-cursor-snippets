from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Optional
from logging import getLogger
# from remove_watermark_app.wm_service import process_image_bytes # This will be created later
from auth.jwt_utils import verify_jwt  # reuse JWT middleware or simple dependency

logger = getLogger("remove_watermark_app")
app = FastAPI(title="Image Processor - Watermark Removal")

@app.get("/health")
async def health():
    return {"status":"ok"}

# Simple dependency (replace with real auth)
async def get_current_user(token: Optional[str] = None):
    # if using real JWT, decode and map to user
    if not token:
        raise HTTPException(status_code=401, detail="missing token")
    try:
        claims = verify_jwt(token)
        return claims
    except Exception:
        raise HTTPException(status_code=401, detail="invalid token")

@app.post("/remove-watermark")
async def remove_watermark_endpoint(
    file: UploadFile = File(...),
    backends: Optional[str] = Form(None),
    hint: Optional[str] = Form(""),
    token: Optional[str] = Form(None), # For simple auth, can be removed if using Depends(get_current_user)
    current_user: dict = Depends(get_current_user) # Example of using auth
):
    # This is a placeholder. The actual logic will be in wm_service.py
    logger.info(f"Received request from user: {current_user.get('user_id')}")
    logger.info(f"File: {file.filename}, Backends: {backends}, Hint: {hint}")

    # Read image bytes
    image_bytes = await file.read()

    # Call the watermark removal service (placeholder)
    # out_bytes = process_image_bytes(image_bytes, backends, hint)
    
    # For now, just return original bytes
    import base64
    return JSONResponse(content={"image_b64": base64.b64encode(image_bytes).decode('utf-8')})