"""
Custom exception handlers for REST API responses.
"""

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Custom exception handler that formats error responses consistently.
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    if response is not None:
        # Customize the response data
        custom_response_data = {
            'success': False,
            'error': {
                'message': get_error_message(response.data),
                'details': response.data if isinstance(response.data, dict) else {'detail': response.data},
                'status_code': response.status_code
            }
        }
        
        response.data = custom_response_data

    return response


def get_error_message(data):
    """
    Extract a user-friendly error message from the error data.
    """
    if isinstance(data, dict):
        # Try to get detail field
        if 'detail' in data:
            return str(data['detail'])
        
        # Try to get first error message from validation errors
        for key, value in data.items():
            if isinstance(value, list) and len(value) > 0:
                return f"{key}: {value[0]}"
            elif isinstance(value, str):
                return f"{key}: {value}"
        
        return "An error occurred"
    
    elif isinstance(data, list) and len(data) > 0:
        return str(data[0])
    
    return str(data)
