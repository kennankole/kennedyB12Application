import json
import hmac
import hashlib
import datetime
import requests
import os
import sys

def main():
    action_run_link = os.environ.get(
        "ACTION_RUN_LINK", 
        "https://github.com/kennankole/kennedyB12Application/actions"
    )
    
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    timestamp = now_utc.isoformat().replace('+00:00', 'Z')

    payload = {
        "action_run_link": action_run_link,
        "email": "kennankole@gmail.com",
        "name": "Kennedy Omondi Oduor",
        "repository_link": "https://github.com/kennankole/kennedyB12Application",
        "resume_link": "https://docs.google.com/document/d/1k3jgn7Ft4m2Zgk1loHBBXBov_RQ99JRW10k2n7LDbOU/edit?usp=sharing",
        "timestamp": timestamp
    }

    json_payload = json.dumps(payload, separators=(',', ':'), sort_keys=True).encode('utf-8')

    secret = os.environ.get("SIGNING_SECRET", "hello-there-from-b12").encode('utf-8')
    hex_digest = hmac.new(secret, json_payload, hashlib.sha256).hexdigest()

    headers = {
        "Content-Type": "application/json",
        "X-Signature-256": f"sha256={hex_digest}"
    }

    url = "https://b12.io/apply/submission"
    print("Sending payload to B12...")
    
    try:
        response = requests.post(url, data=json_payload, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                receipt = data.get('receipt')
                print("\n" + "="*50)
                print("SUCCESS! Here is your submission receipt:")
                print(receipt)
                print("="*50 + "\n")
            else:
                print(f"Submission failed: {data}")
                sys.exit(1)
        else:
            print("Submission failed. Please check the response above.")
            sys.exit(1)
            
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()