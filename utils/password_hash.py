import bcrypt
# from database.db_handler import dbHandler

class PasswordHash:

    def userPassword(self, user_password: str) -> str:
        userPassword = user_password
        passwordBytes = userPassword.encode('utf-8')

        salt = bcrypt.gensalt()

        hashPassword = bcrypt.hashpw(passwordBytes, salt)

        return hashPassword

    def checkPassword(self, password, return_pass):
        returnPass = return_pass
        if isinstance(returnPass, str):
            returnPass = returnPass.encode("utf-8")

        is_match = bcrypt.checkpw(password.encode("utf-8"), returnPass)

        return is_match