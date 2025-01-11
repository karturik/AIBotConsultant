import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Request logging
        logger.info(f"Request: {request.method} {request.url}")
        
        # Process request
        response = await call_next(request)
        
        # Response logging
        process_time = time.time() - start_time
        logger.info(
            f"Response: status={response.status_code} "
            f"process_time={process_time:.3f}s"
        )
        
        return response
