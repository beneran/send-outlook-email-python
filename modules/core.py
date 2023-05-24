from modules.msgraph import get_access_token
import requests

base_url = "https://graph.microsoft.com/v1.0/"


def send_text_email(to: str, subject: str, content: str = "content"):
    endpoint = base_url + "me/sendMail"
    access_token = get_access_token()
    headers = {"Authorization": "Bearer " + access_token}
    request_body = {
        "message": {
            "toRecipients": [{"emailAddress": {"address": to}}],
            "subject": subject,
            "body": {
                "contentType": "text",  # or html
                "content": content,
            },
            "importance": "normal",
        }
    }
    response = requests.post(endpoint, headers=headers, json=request_body)
    return response.status_code
