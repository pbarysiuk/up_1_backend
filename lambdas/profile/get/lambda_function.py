from src.users.profileBusiness import ProfileBusiness

def lambda_handler(event, context):
    return ProfileBusiness.getProfile(token=event.get('headers').get('auth'))
