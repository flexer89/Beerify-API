from fastapi import HTTPException


class BeerifyException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(status_code=status_code, detail=detail)


class NotFoundException(BeerifyException):
    def __init__(self, item_name: str):
        super().__init__(status_code=404, detail=item_name)


class BadValue(BeerifyException):
    def __init__(self, detail: str):
        detail = f"Invalid {detail} value"
        super().__init__(status_code=400, detail=detail)


class ValidationException(BeerifyException):
    def __init__(self, field_name: str, reason: str):
        detail = f"Validation failed for field '{field_name}': {reason}"
        super().__init__(status_code=422, detail=detail)


class UnauthorizedException(BeerifyException):
    def __init__(self):
        super().__init__(status_code=401, detail="Unauthorized")


class ForbiddenException(BeerifyException):
    def __init__(self):
        super().__init__(status_code=403, detail="Forbidden")
