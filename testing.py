# This file is created to create and test functions before implementing it in the actual code
import bcrypt

# Example password
password = 'Ashutoshkt@05'

# Converting password to array of bytes
bytes = password.encode('utf-8')

# Generating the salt
salt = bcrypt.gensalt()

# Hashing the password
hash = bcrypt.hashpw(bytes, salt)

# Password to check against the example password
userPassword = 'Ashutoshkt@05'

userBytes = userPassword.encode('utf-8')

result = bcrypt.checkpw(userBytes, hash)

print(result)

print(hash)