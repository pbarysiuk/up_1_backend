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


    #unauthorized 401
    invalidToken = '401-001'
    wrongEmailOrPassword = '401-002'
    oldPasswordNotMatch = '401-003' 
    forgetPasswordCodeNotMatch = '401-004'

    #forbidden 403
    expiredToken = '403-001'
    lackOfPrivileges = '403-002'

   
    
    #not found 404
    userNotFound = '404-001'
    forgetPasswordRequestNotFound = '404-002'

    #confolict 409
    duplicateEmail = '409-001'
    