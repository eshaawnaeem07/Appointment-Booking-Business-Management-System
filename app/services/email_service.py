# import os
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail
# from dotenv import load_dotenv
# from fastapi import HTTPException
# from app.utils.constants import FROM_EMAIL

# load_dotenv()

# class EmailService:
#     @staticmethod
#     def send_otp_email(email: str, otp: str):
#         try:
#             api_key = "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"

#             if not api_key:
#                 raise Exception("SENDGRID_API_KEY not found in environment")

#             message = Mail(
#                 from_email=FROM_EMAIL,
#                 to_emails=email,
#                 subject='Your Password Reset OTP',
#                 html_content=f'<strong>Your OTP is: {otp}</strong>. It expires in 15 minutes.'
#             )

#             sg = SendGridAPIClient(api_key)
#             print("sendgrid client ", sg)

#             # response = sg.send(message)
#             try:
#                     response = sg.send(message)
#             except Exception as e:
#                     print(f"Error response email.......: {e}")
#                     raise HTTPException(status_code=500, detail=f"Email failed: {str(e)}")
#             print("sendgrid response", response)

#             print("Status Code:", response.status_code)

#             if response.status_code >= 400:
#                 raise Exception(f"SendGrid error: {response.body}")

#         except Exception as e:
#             raise HTTPException(status_code=500, detail=f"Email failed: {str(e)}")
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import HTTPException
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env", override=True)


class EmailService:
    @staticmethod
    def send_otp_email(email: str, otp: str):
        try:
            api_key = os.getenv("SENDGRID_API_KEY", "").strip()
            from_email = os.getenv("FROM_EMAIL", "").strip()

            if not api_key:
                raise Exception("Missing SENDGRID_API_KEY")

            if not from_email:
                raise Exception("Missing FROM_EMAIL")

            print(f"SendGrid API Key loaded: {api_key[:6]}...{api_key[-4:]}")

            message = Mail(
                from_email=from_email,
                to_emails=email,
                subject="Your Password Reset OTP",
                html_content=f"<strong>Your OTP is: {otp}</strong>. It expires in 15 minutes."
            )

            sg = SendGridAPIClient(api_key)
            response = sg.send(message)

            print("SendGrid status:", response.status_code)

            if response.status_code >= 400:
                raise Exception(f"SendGrid error: {response.status_code} - {response.body}")

        except Exception as e:
            print("EMAIL ERROR:", str(e))
            raise HTTPException(status_code=500, detail=f"Email failed: {str(e)}")
