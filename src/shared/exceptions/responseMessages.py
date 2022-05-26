from src.shared.exceptions.responseCodes import ResponseCodes

class ResponseMessages:
    english = {
        ResponseCodes.success : "Success !!",
        ResponseCodes.generalError : "Unexpected error occured",
        ResponseCodes.invalidEmailFormat : 'Invalid email format',
        ResponseCodes.emptyOrInvalidEmail : 'Empty or invalid email',
        ResponseCodes.emptyOrInvalidPassword : 'Empty or invalid password',
        ResponseCodes.invalidToken : 'Invalid token',
        ResponseCodes.wrongEmailOrPassword : 'Wrong email or password',
        ResponseCodes.expiredToken : 'Expired token',
        ResponseCodes.lackOfPrivileges : "You Don't have privilege to do this action",
        ResponseCodes.emptyOrInvalidRole : "Empty or invalid role",
        ResponseCodes.emptyOrInvalidName : "Empty or invalid role",
        ResponseCodes.duplicateEmail : "Duplicated email",
        ResponseCodes.userNotFound : "User not found",
        ResponseCodes.oldPasswordNotMatch : "Old password doesn't match",
        ResponseCodes.invalidPageNumber : 'Invalid page number',
        ResponseCodes.invalidPageSize : 'Invalid page size',
        ResponseCodes.emptyOrInvalidForgetPasswordRequestId : "Empty or invalid forget password request id",
        ResponseCodes.forgetPasswordRequestNotFound : "Forget password request not found",
        ResponseCodes.emptyOrInvalidForgetPasswordCode : "Empty or invalid forget password code",
        ResponseCodes.forgetPasswordCodeNotMatch : "Forget password code doesn't match"
    }