def response_wrapper(data, status_code=200, message="Success"):
    return {
        "status_code": status_code,
        "message": message,
        "data": data
    }

