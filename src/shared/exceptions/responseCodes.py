class ResponseCodes:
    #ok 200
    success = '200'

    #internal server error 500
    generalError = '500'

    #bad request 400
    invalidEmailFormat = '400-001'
    emptyOrInvalidEmail = '400-002'
    emptyOrInvalidPassword = '400-003'
    emptyOrInvalidRole = '400-004'
    emptyOrInvalidName = '400-005'
    invalidPageNumber = '400-006'
    invalidPageSize = '400-007'
    emptyOrInvalidForgetPasswordRequestId = '400-008'
    emptyOrInvalidForgetPasswordCode = '400-009'
    emptyXdlName = '400-010'
    emptyXdlUrl = '400-011'
    emptyXdlFilePath = '400-012'
    emptyXdlXml = '400-013'
    emptyXdlText = '400-014'
    emptyXdlId = '400-015'
    emptyXdlSearchQuery = '400-016'
    badXdlRequest = '400-17'
    emptyXdlTitle = '400-18'
    emptyVerificationCode = '400-19'



    #unauthorized 401
    invalidToken = '401-001'
    wrongEmailOrPassword = '401-002'
    oldPasswordNotMatch = '401-003' 
    forgetPasswordCodeNotMatch = '401-004'
    verificationCodeNotMatch = '401-005'

    #forbidden 403
    expiredToken = '403-001'
    lackOfPrivileges = '403-002'
    notVerifiedUser = '403-003'

   
    
    #not found 404
    userNotFound = '404-001'
    forgetPasswordRequestNotFound = '404-002'
    xdlNotFound =  '404-003'
    fileNotFound = '404-004'

    #confolict 409
    duplicateEmail = '409-001'
    alreadyVerifiedUser = '409-002'
    
