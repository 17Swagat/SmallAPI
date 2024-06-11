from passlib.context import CryptContext # For: PswdHashing

# For pswd hasing:
# default hashing algo: 'bcrypt'
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto") 


# hash-string function:
def hash_str(pswd: str):
    hashed_pswd = pwd_context.hash(secret=pswd)
    return hashed_pswd