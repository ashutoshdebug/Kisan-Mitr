class PasswordHash:
    """Provide bcrypt password hashing and verification for Kisan Mitr accounts.

    ``dbHandler`` uses this helper for registration and login validation. It
    generates a fresh bcrypt salt for each password and checks later plaintext
    values against the stored database hash.
    """

    def userPassword(self, user_password: str) -> bytes:
        """Hash a plaintext password with a newly generated bcrypt salt.

        Args:
            user_password (str): Required plaintext password encoded as UTF-8
                before it is supplied to bcrypt.

        Returns:
            bytes: The bcrypt hash returned by ``bcrypt.hashpw``. The runtime
            implementation returns bytes, not the former stub's ``str`` type.
        """
        ...

    def checkPassword(self, password: str, return_pass: str | bytes) -> bool:
        """Check a plaintext password against a stored bcrypt hash.

        Args:
            password (str): Required plaintext password to encode as UTF-8.
            return_pass (str | bytes): Required stored hash; strings are UTF-8
                encoded before verification and bytes are used directly.

        Returns:
            bool: ``True`` when the password matches the hash; otherwise
            ``False``.
        """
        ...
