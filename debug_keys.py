
import os
import requests

# The key provided by user, which contains 'POd'
ORIGINAL_KEY = 'FzwNPAouDqT7Epue7lPOd_2_kEpIb5ONVMc-ZrKOCSk'

# Variation: Replace 'O' with '0'
VAR_1 = ORIGINAL_KEY.replace('POd', 'P0d')

# Variation: Replace '0' with 'O' (unlikely as 0 is distinct)
VAR_2 = ORIGINAL_KEY.replace('0', 'O') # Replace ALL 0s

keys_to_test = [
    ("Original", ORIGINAL_KEY),
    ("Var 1 (O->0)", VAR_1),
    ("Var 2 (0->O)", VAR_2)
]

print("--- Unsplash Key Brute Force Check ---")

for name, key in keys_to_test:
    print(f"\nTesting {name}: {key}")
    url = "https://api.unsplash.com/search/photos"
    headers = {
        "Authorization": f"Client-ID {key}",
        "Accept-Version": "v1"
    }
    params = {"query": "test", "per_page": 1}
    
    try:
        resp = requests.get(url, headers=headers, params=params)
        print(f"Status: {resp.status_code}")
        if resp.status_code == 200:
            print(">>> SUCCESS! THIS IS THE VALID KEY <<<")
            print(f"Valid Key: {key}")
            break
        else:
            print(f"Failed: {resp.text}")
    except Exception as e:
        print(f"Error: {e}")
