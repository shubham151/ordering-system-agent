import os
from typing import Literal, Optional
from dotenv import load_dotenv

load_dotenv()

class Config:
    
    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    RELOAD: bool = os.getenv("RELOAD", "true").lower() == "true"
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # AI Provider settings
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "gemini").lower()
    
    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # AI Model settings
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")
    
    # CORS settings
    ALLOWED_ORIGINS: list = ["*"]
    
    # Order limits and validation
    MAX_ITEM_QUANTITY: int = int(os.getenv("MAX_ITEM_QUANTITY", "50"))
    MAX_MESSAGE_LENGTH: int = int(os.getenv("MAX_MESSAGE_LENGTH", "500"))
    MIN_MESSAGE_LENGTH: int = int(os.getenv("MIN_MESSAGE_LENGTH", "1"))
    
    # Request timeouts (in seconds)
    AI_REQUEST_TIMEOUT: int = int(os.getenv("AI_REQUEST_TIMEOUT", "30"))
    DEFAULT_REQUEST_TIMEOUT: int = int(os.getenv("DEFAULT_REQUEST_TIMEOUT", "60"))
    
    # Logging settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()
    LOG_FORMAT: str = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    # Rate limiting (requests per minute)
    RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    RATE_LIMIT_WINDOW: int = int(os.getenv("RATE_LIMIT_WINDOW", "60"))
    
    # Database settings (for future use)
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
    DATABASE_POOL_SIZE: int = int(os.getenv("DATABASE_POOL_SIZE", "10"))
    
    # Security settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "ai-food-ordering-system")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Feature flags
    ENABLE_LOGGING: bool = os.getenv("ENABLE_LOGGING", "true").lower() == "true"
    ENABLE_METRICS: bool = os.getenv("ENABLE_METRICS", "false").lower() == "true"
    ENABLE_RATE_LIMITING: bool = os.getenv("ENABLE_RATE_LIMITING", "false").lower() == "true"
    
    @classmethod
    def validate(cls) -> list[str]:
        errors = []
        
        if cls.AI_PROVIDER not in ["openai", "gemini"]:
            errors.append(f"Invalid AI_PROVIDER: {cls.AI_PROVIDER}. Must be 'openai' or 'gemini'")
        
        if cls.AI_PROVIDER == "openai" and not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY is required when using OpenAI provider")
        
        if cls.AI_PROVIDER == "gemini" and not cls.GEMINI_API_KEY:
            errors.append("GEMINI_API_KEY is required when using Gemini provider")
        
        if cls.PORT < 1 or cls.PORT > 65535:
            errors.append(f"Invalid PORT: {cls.PORT}. Must be between 1 and 65535")

        if cls.MAX_ITEM_QUANTITY <= 0:
            errors.append(f"Invalid MAX_ITEM_QUANTITY: {cls.MAX_ITEM_QUANTITY}. Must be positive")
        
        if cls.MAX_MESSAGE_LENGTH <= cls.MIN_MESSAGE_LENGTH:
            errors.append(f"MAX_MESSAGE_LENGTH ({cls.MAX_MESSAGE_LENGTH}) must be greater than MIN_MESSAGE_LENGTH ({cls.MIN_MESSAGE_LENGTH})")
 
        if cls.AI_REQUEST_TIMEOUT <= 0:
            errors.append(f"Invalid AI_REQUEST_TIMEOUT: {cls.AI_REQUEST_TIMEOUT}. Must be positive")
        
        valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if cls.LOG_LEVEL not in valid_log_levels:
            errors.append(f"Invalid LOG_LEVEL: {cls.LOG_LEVEL}. Must be one of {valid_log_levels}")
        
        if cls.RATE_LIMIT_REQUESTS <= 0:
            errors.append(f"Invalid RATE_LIMIT_REQUESTS: {cls.RATE_LIMIT_REQUESTS}. Must be positive")
        
        if cls.RATE_LIMIT_WINDOW <= 0:
            errors.append(f"Invalid RATE_LIMIT_WINDOW: {cls.RATE_LIMIT_WINDOW}. Must be positive")
        
        return errors
    
    @classmethod
    def get_summary(cls) -> dict:
        """Get configuration summary (without sensitive data)"""
        return {
            "environment": cls.ENVIRONMENT,
            "host": cls.HOST,
            "port": cls.PORT,
            "debug": cls.DEBUG,
            "ai_provider": cls.AI_PROVIDER,
            "ai_model": cls.GEMINI_MODEL if cls.AI_PROVIDER == "gemini" else cls.OPENAI_MODEL,
            "max_item_quantity": cls.MAX_ITEM_QUANTITY,
            "max_message_length": cls.MAX_MESSAGE_LENGTH,
            "log_level": cls.LOG_LEVEL,
            "features": {
                "logging": cls.ENABLE_LOGGING,
                "metrics": cls.ENABLE_METRICS,
                "rate_limiting": cls.ENABLE_RATE_LIMITING
            }
        }
    
    @classmethod
    def is_production(cls) -> bool:
        return cls.ENVIRONMENT.lower() == "production"
    
    @classmethod
    def is_development(cls) -> bool:
        """Check if running in development environment"""
        return cls.ENVIRONMENT.lower() in ["development", "dev"]