import bcrypt

class PasswordHash:

    def userPassword(self, user_password: str) -> str:
        userPassword = user_password
        passwordBytes = userPassword.encode('utf-8')

        salt = bcrypt.gensalt()

        hashPassword = bcrypt.hashpw(passwordBytes, salt)

        return hashPassword