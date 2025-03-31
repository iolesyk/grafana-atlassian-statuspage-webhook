from flask import Flask, request
import json
import requests  # Import requests for making HTTP requests
import os  # Import os for environment variables

app = Flask(__name__)

# Load environment variables
STATUSPAGE_API_URL = os.getenv("STATUSPAGE_API_URL", "https://api.statuspage.io")
STATUSPAGE_API_BEARER_TOKEN = os.getenv("STATUSPAGE_API_BEARER_TOKEN")

# Ensure the mandatory environment variable is set
if not STATUSPAGE_API_BEARER_TOKEN:
    raise EnvironmentError("The environment variable 'STATUSPAGE_API_BEARER_TOKEN' must be set.")

@app.route("/webhook", methods=["POST", "PUT"])
def webhook():
    payload = request.json  # Parse the JSON payload

    # Extract the required fields
    status = payload.get("status")
    description = json.loads(payload.get("commonAnnotations", {}).get("description", "{}"))
    page = description.get("page")
    component = description.get("component")
    instance = description.get("instance")

    # Log the extracted values
    print("Status:", status, flush=True)
    print("Instance:", instance, flush=True)
    print("Description Page:", page, flush=True)
    print("Description Component:", component, flush=True)

    # Map incoming statuses to Statuspage statuses
    status_mapping = {
        "firing": "major_outage",
        "resolved": "operational",
        "no_data": "under_maintenance",
        "paused": "under_maintenance"
    }
    mapped_status = status_mapping.get(status, "operational")  # Default to "operational" if status is unknown

    # Prepare the data to resend
    resend_payload = {
        "component": {
            "status": mapped_status
        }
    }

    # Resend the payload using a PUT request to the Statuspage API
    url = f"{STATUSPAGE_API_URL}/v1/pages/{page}/components/{component}"
    headers = {
        "Authorization": f"Bearer {STATUSPAGE_API_BEARER_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.put(url, headers=headers, json=resend_payload)

    # Log the response from the forwarded request
    print("Resend Response Status Code:", response.status_code, flush=True)
    print("Resend Response Body:", response.text, flush=True)

    return {"message": "Received and resent"}, 200  # Respond OK

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)