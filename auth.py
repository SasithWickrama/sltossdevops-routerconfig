import hashlib

class Authentication:
    def login(self):
        if not self or not self.username or not self.password:
            # return make_response({'success': 'false', 'message': 'Authentication Required'}, 401,
            #                      {'WWW-Authenticate': 'Basic realm="Login required!"'})
            return 'Authentication Required'
        hashpwd = hashlib.md5(self.password.encode())

        try:
            if self.username == 'clarity':
                if hashpwd.hexdigest() == '518f8a60369d3a0b78b22b88af75b2a6':
                    return 'success'

                return 'Invalid Credentials'
            return 'Invalid Credentials'
        except TypeError:

            return 'Unauthorized User'
