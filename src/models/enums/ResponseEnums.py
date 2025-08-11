from enum import Enum

class ResponseSignal(Enum):
    FILE_VALIDATE_SUCCESS = "File validates successfully"
    FILE_TYPE_NOT_SUPPORTED= "File type refused"
    FILE_SIZE_EXCEEDED= "File size exceeded"
    FILE_UPLOAD_SUCCESS= "File upload success"
    FILE_UPLOAD_FAILED = "File upload failed"