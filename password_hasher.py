# Function that takes password, token, and API key and sends back the final md5 hashed password

import requests
from hashlib import md5

def hash_md5(str):
	return md5(str.encode()).hexdigest()
