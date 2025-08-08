#!/usr/bin/env python3
"""
user_limits.py
User authentication and credit limits for Shujaa Studio API
Following elite-cursor-snippets patterns for Kenya-specific requirements
"""

import sqlite3
import os
import hashlib
import secrets
from datetime import date, datetime
from typing import Optional, Dict, Any
from pathlib import Path

class UserLimits:
    def __init__(self, db_path: str = "users.db"):
        """Initialize user limits system with SQLite database"""
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        # Users table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                email TEXT UNIQUE,
                phone TEXT UNIQUE,
                password_hash TEXT,
                created_at TEXT,
                subscription_type TEXT DEFAULT 'free',
                credits_remaining INTEGER DEFAULT 3
            )
        """)
        
        # Usage tracking table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                day TEXT,
                count INTEGER DEFAULT 1,
                video_id TEXT,
                created_at TEXT,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        """)
        
        # Payments table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                amount INTEGER,
                payment_method TEXT,
                transaction_id TEXT,
                status TEXT,
                created_at TEXT,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return self._hash_password(password) == hashed
    
    def register_user(self, email: str, phone: str, password: str) -> Dict[str, Any]:
        """Register a new user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            
            user_id = secrets.token_urlsafe(16)
            password_hash = self._hash_password(password)
            created_at = datetime.now().isoformat()
            
            cur.execute("""
                INSERT INTO users (user_id, email, phone, password_hash, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, email, phone, password_hash, created_at))
            
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "user_id": user_id,
                "message": "User registered successfully"
            }
            
        except sqlite3.IntegrityError:
            return {
                "success": False,
                "message": "Email or phone already exists"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Registration failed: {str(e)}"
            }
    
    def authenticate_user(self, email: str, password: str) -> Optional[str]:
        """Authenticate user and return user_id if successful"""
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            
            cur.execute("""
                SELECT user_id, password_hash FROM users 
                WHERE email = ?
            """, (email,))
            
            row = cur.fetchone()
            conn.close()
            
            if row and self._verify_password(password, row[1]):
                return row[0]
            return None
            
        except Exception:
            return None
    
    def check_usage_limit(self, user_id: str, max_per_day: int = 3) -> Dict[str, Any]:
        """Check if user has exceeded daily usage limit"""
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            
            today = date.today().isoformat()
            
            # Get user subscription info
            cur.execute("""
                SELECT subscription_type, credits_remaining FROM users 
                WHERE user_id = ?
            """, (user_id,))
            
            user_row = cur.fetchone()
            if not user_row:
                return {"allowed": False, "reason": "User not found"}
            
            subscription_type, credits_remaining = user_row
            
            # Check daily usage
            cur.execute("""
                SELECT COUNT(*) FROM usage 
                WHERE user_id = ? AND day = ?
            """, (user_id, today))
            
            daily_count = cur.fetchone()[0]
            
            # Determine limits based on subscription
            if subscription_type == "premium":
                daily_limit = 50
            elif subscription_type == "pro":
                daily_limit = 20
            else:  # free
                daily_limit = max_per_day
            
            # Check if user has credits
            if credits_remaining <= 0:
                return {
                    "allowed": False, 
                    "reason": "No credits remaining",
                    "credits_remaining": credits_remaining
                }
            
            # Check daily limit
            if daily_count >= daily_limit:
                return {
                    "allowed": False,
                    "reason": "Daily limit exceeded",
                    "daily_used": daily_count,
                    "daily_limit": daily_limit
                }
            
            return {
                "allowed": True,
                "daily_used": daily_count,
                "daily_limit": daily_limit,
                "credits_remaining": credits_remaining,
                "subscription_type": subscription_type
            }
            
        except Exception as e:
            return {"allowed": False, "reason": f"Error checking limits: {str(e)}"}
        finally:
            conn.close()
    
    def record_usage(self, user_id: str, video_id: str) -> bool:
        """Record a video generation usage"""
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            
            today = date.today().isoformat()
            created_at = datetime.now().isoformat()
            
            # Record usage
            cur.execute("""
                INSERT INTO usage (user_id, day, video_id, created_at)
                VALUES (?, ?, ?, ?)
            """, (user_id, today, video_id, created_at))
            
            # Deduct credit
            cur.execute("""
                UPDATE users SET credits_remaining = credits_remaining - 1
                WHERE user_id = ?
            """, (user_id,))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception:
            return False
    
    def add_credits(self, user_id: str, credits: int) -> bool:
        """Add credits to user account"""
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            
            cur.execute("""
                UPDATE users SET credits_remaining = credits_remaining + ?
                WHERE user_id = ?
            """, (credits, user_id))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception:
            return False
    
    def get_user_info(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user information"""
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            
            cur.execute("""
                SELECT email, phone, subscription_type, credits_remaining, created_at
                FROM users WHERE user_id = ?
            """, (user_id,))
            
            row = cur.fetchone()
            conn.close()
            
            if row:
                return {
                    "user_id": user_id,
                    "email": row[0],
                    "phone": row[1],
                    "subscription_type": row[2],
                    "credits_remaining": row[3],
                    "created_at": row[4]
                }
            return None
            
        except Exception:
            return None
    
    def record_payment(self, user_id: str, amount: int, payment_method: str, 
                      transaction_id: str, status: str = "pending") -> bool:
        """Record a payment transaction"""
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            
            created_at = datetime.now().isoformat()
            
            cur.execute("""
                INSERT INTO payments (user_id, amount, payment_method, transaction_id, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, amount, payment_method, transaction_id, status, created_at))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception:
            return False

# Global instance
user_limits = UserLimits()
