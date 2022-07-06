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
        ResponseCodes.emptyOrInvalidName : "Empty or invalid name",
        ResponseCodes.duplicateEmail : "Duplicated email",
        ResponseCodes.userNotFound : "User not found",
        ResponseCodes.oldPasswordNotMatch : "Old password doesn't match",
        ResponseCodes.invalidPageNumber : 'Invalid page number',
        ResponseCodes.invalidPageSize : 'Invalid page size',
        ResponseCodes.emptyOrInvalidForgetPasswordRequestId : "Empty or invalid forget password request id",
        ResponseCodes.forgetPasswordRequestNotFound : "Forget password request not found",
        ResponseCodes.emptyOrInvalidForgetPasswordCode : "Empty or invalid forget password code",
        ResponseCodes.forgetPasswordCodeNotMatch : "Forget password code doesn't match",
        ResponseCodes.emptyXdlName : "Empty or invalid name",
        ResponseCodes.emptyXdlUrl : "Empty or invalid url",
        ResponseCodes.emptyXdlFilePath : "Empty or invalid file path",
        ResponseCodes.emptyXdlXml : "Empty or invalid xml",
        ResponseCodes.emptyXdlText : "Empty or invalid synthesis",
        ResponseCodes.emptyXdlId : "Empty or invalid id",
        ResponseCodes.emptyXdlSearchQuery : "Empty or invalid search query",
        ResponseCodes.xdlNotFound : "Xdl not found",
        ResponseCodes.fileNotFound : "file not found",
        ResponseCodes.badXdlRequest : "Length of drugs names not equals length of texts or xmls",
        ResponseCodes.emptyXdlTitle : "Empty xdl title",
        ResponseCodes.emptyVerificationCode : "Empty verification code",
        ResponseCodes.verificationCodeNotMatch : "Verification code not match",
        ResponseCodes.notVerifiedUser : "User not verified",
        ResponseCodes.alreadyVerifiedUser : "User already verified",
        ResponseCodes.alreadyResettedPasswordFirstTime : "User already reseted password"
        
        
        
        



    }