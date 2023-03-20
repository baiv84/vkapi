class VKException(Exception):
    """Determine custom exception type for VK API errors handling"""
    def __init__(self, error_code, error_msg, exception_point):
        self.args = (error_code, error_msg, exception_point)
        self.error_code = error_code
        self.error_msg = error_msg
        self.exception_point = exception_point
