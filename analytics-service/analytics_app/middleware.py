"""JSON logging middleware for analytics service."""
import json
import logging
import time
from datetime import datetime, timezone
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class JsonLoggingMiddleware(MiddlewareMixin):
    """Middleware to log requests in structured JSON format."""
    
    def process_request(self, request):
        request._start_time = time.time()
        return None
    
    def process_response(self, request, response):
        if hasattr(request, '_start_time'):
            duration_ms = round((time.time() - request._start_time) * 1000, 2)
            
            log_data = {
                "method": request.method,
                "path": request.path,
                "status": response.status_code,
                "duration_ms": duration_ms,
                "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
            }
            
            logger.info(json.dumps(log_data))
        
        return response