from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
import os

class UserManager(object):
    def __init__(self):
        pass
    def parse_user(self,request):
        if  os.environ.get('APP_ENV') == 'dev':
            return {
                'userid'        : 1,
                'username'      : 'admin',
                'email'         : 'admin@genopedia',
                'logout_link'   : ''
            }
        else :
            import jwt
            encoded = request.COOKIES.get('_gpadmin_jwt')
            if encoded:
                user = jwt.decode(encoded, settings.OAUTH_CLIENT_EK, algorithms=['HS256'])
                if user:
                    return user
            return False
    