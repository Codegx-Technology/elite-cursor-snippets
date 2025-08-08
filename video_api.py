from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import subprocess
import uuid
import os
import asyncio
from pathlib import Path
from typing import Optional
import json
from user_limits import user_limits
from payment_integration import payment_integration

app = FastAPI(title="Shujaa Studio API", version="1.0.0")
security = HTTPBearer()

class PromptRequest(BaseModel):
    prompt: str
    lang: str = "sheng"
    scenes: int = 3
    vertical: bool = True
    output_format: str = "mp4"

class VideoResponse(BaseModel):
    status: str
    video_id: str
    video_path: str
    message: str

class UserRegister(BaseModel):
    email: str
    phone: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class PaymentRequest(BaseModel):
    amount: int
    payment_method: str  # "mpesa" or "stripe"
    phone_number: Optional[str] = None  # Required for M-Pesa

class MpesaStatusRequest(BaseModel):
    checkout_request_id: str

class StripeConfirmRequest(BaseModel):
    payment_intent_id: str

# Ensure output directories exist
os.makedirs("videos", exist_ok=True)
os.makedirs("temp", exist_ok=True)

# Authentication dependency
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Get current user from token"""
    token = credentials.credentials
    # For now, use token as user_id (in production, implement proper JWT)
    user_info = user_limits.get_user_info(token)
    if not user_info:
        raise HTTPException(status_code=401, detail="Invalid token")
    return token

@app.get("/")
async def root():
    return {"message": "Shujaa Studio API - AI Video Generation Service"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "shujaa-studio"}

@app.post("/register")
async def register_user(req: UserRegister):
    """Register a new user"""
    result = user_limits.register_user(req.email, req.phone, req.password)
    if result["success"]:
        return {
            "success": True,
            "user_id": result["user_id"],
            "message": "Registration successful. Use user_id as your API token."
        }
    else:
        raise HTTPException(status_code=400, detail=result["message"])

@app.post("/login")
async def login_user(req: UserLogin):
    """Login user and return token"""
    user_id = user_limits.authenticate_user(req.email, req.password)
    if user_id:
        return {
            "success": True,
            "user_id": user_id,
            "message": "Login successful. Use user_id as your API token."
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/user/info")
async def get_user_info(current_user: str = Depends(get_current_user)):
    """Get current user information"""
    user_info = user_limits.get_user_info(current_user)
    if user_info:
        return user_info
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.post("/purchase-credits")
async def purchase_credits(req: PaymentRequest, current_user: str = Depends(get_current_user)):
    """Purchase credits using M-Pesa or Stripe"""
    try:
        result = payment_integration.process_credit_purchase(
            user_id=current_user,
            amount=req.amount,
            payment_method=req.payment_method,
            phone_number=req.phone_number
        )
        
        if result["success"]:
            # Record payment transaction
            user_limits.record_payment(
                user_id=current_user,
                amount=req.amount,
                payment_method=req.payment_method,
                transaction_id=result.get("checkout_request_id") or result.get("payment_intent_id", "unknown")
            )
            
            return {
                "success": True,
                "payment_info": result,
                "message": "Payment initiated successfully"
            }
        else:
            raise HTTPException(status_code=400, detail=result["message"])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Payment failed: {str(e)}")

@app.post("/mpesa/status")
async def check_mpesa_status(req: MpesaStatusRequest):
    """Check M-Pesa payment status"""
    result = payment_integration.check_mpesa_payment_status(req.checkout_request_id)
    
    if result["success"] and result.get("result_code") == "0":
        # Payment successful, add credits
        # Note: In production, you'd get user_id from the reference
        return {
            "success": True,
            "status": "completed",
            "amount": result.get("amount"),
            "receipt": result.get("mpesa_receipt_number")
        }
    else:
        return {
            "success": False,
            "status": "pending" if result["success"] else "failed",
            "message": result.get("message", "Payment status unknown")
        }

@app.post("/stripe/confirm")
async def confirm_stripe_payment(req: StripeConfirmRequest):
    """Confirm Stripe payment and add credits"""
    result = payment_integration.confirm_stripe_payment(req.payment_intent_id)
    
    if result["success"] and result.get("status") == "succeeded":
        # Payment successful, add credits
        # Note: In production, you'd get user_id from metadata
        return {
            "success": True,
            "status": "completed",
            "amount": result.get("amount"),
            "currency": result.get("currency")
        }
    else:
        return {
            "success": False,
            "status": "failed",
            "message": result.get("message", "Payment confirmation failed")
        }

@app.post("/generate-video", response_model=VideoResponse)
async def generate_video(req: PromptRequest, current_user: str = Depends(get_current_user)):
    """
    Generate AI video from prompt using Shujaa Studio pipeline
    Requires authentication and checks usage limits
    """
    # Check usage limits
    limit_check = user_limits.check_usage_limit(current_user)
    if not limit_check["allowed"]:
        raise HTTPException(
            status_code=429, 
            detail=f"Usage limit exceeded: {limit_check['reason']}"
        )
    
    try:
        video_id = str(uuid.uuid4())[:8]
        output_path = f"videos/{video_id}.{req.output_format}"
        
        # Sanitize prompt for command line
        sanitized_prompt = req.prompt.replace('"', '\\"')
        
        # Build pipeline command
        cmd = [
            "python", "pipeline.py",
            "--prompt", sanitized_prompt,
            "--lang", req.lang,
            "--scenes", str(req.scenes),
            "--out", output_path
        ]
        
        if req.vertical:
            cmd.append("--vertical")
        
        # Execute pipeline
        print(f"[API] Executing: {' '.join(cmd)}")
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode != 0:
            raise HTTPException(
                status_code=500, 
                detail=f"Pipeline failed: {result.stderr}"
            )
        
        # Check if output file exists
        if not os.path.exists(output_path):
            raise HTTPException(
                status_code=500,
                detail="Video file not generated"
            )
        
        # Record usage
        user_limits.record_usage(current_user, video_id)
        
        return VideoResponse(
            status="success",
            video_id=video_id,
            video_path=output_path,
            message="Video generated successfully"
        )
        
    except subprocess.TimeoutExpired:
        raise HTTPException(
            status_code=408,
            detail="Video generation timed out"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Generation failed: {str(e)}"
        )

@app.get("/videos/{video_id}")
async def get_video_info(video_id: str):
    """Get information about a generated video"""
    video_path = f"videos/{video_id}.mp4"
    
    if not os.path.exists(video_path):
        raise HTTPException(
            status_code=404,
            detail="Video not found"
        )
    
    file_size = os.path.getsize(video_path)
    return {
        "video_id": video_id,
        "path": video_path,
        "size_bytes": file_size,
        "exists": True
    }

@app.get("/list-videos")
async def list_videos():
    """List all generated videos"""
    videos_dir = Path("videos")
    if not videos_dir.exists():
        return {"videos": []}
    
    videos = []
    for video_file in videos_dir.glob("*.mp4"):
        videos.append({
            "video_id": video_file.stem,
            "filename": video_file.name,
            "size_bytes": video_file.stat().st_size,
            "created": video_file.stat().st_ctime
        })
    
    return {"videos": videos}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
