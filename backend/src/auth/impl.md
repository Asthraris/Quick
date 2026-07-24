# JWT (json web token) implementation notes

### jwt me multiple session ko kese handle karte hai like if user logs in twice?

1. install dep
pip install "python-jose[cryptography]" "passlib[bcrypt]"

2. Core Security & Utilities
utils.py
QUESTION how does server verify that the token prodived by the user is true or not random str
> 2.1 create hasher,verify , and create token util func.
> 2.1.5 encode the token 

3. create dependecies.py which verifies the header of the logged user to see if he is true user than returns him if yes 
