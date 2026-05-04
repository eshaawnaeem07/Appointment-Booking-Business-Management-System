# import os
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail
# from dotenv import load_dotenv
# from app.utils.constants import FROM_EMAIL
# from dotenv import load_dotenv
# import os

# load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))
# # load_dotenv()  

# class EmailService:
#     @staticmethod
#     def send_otp_email(email: str, otp: str):
#         message = Mail(
#             from_email=FROM_EMAIL,
#             to_emails=email,
#             subject='Your Password Reset OTP',
#             html_content=f'<strong>Your OTP is: {otp}</strong>. It expires in 15 minutes.')
#         try:
#             api_key = os.environ.get('SENDGRID_API_KEY')
#             sg = SendGridAPIClient(api_key)
#             response = sg.send(message)
           
#             print(f"Status Code: {response.status_code}") 
#             print(f"Response Body: {response.body}")
#         except Exception as e:
#             print(f"Error sending email: {e}")
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
from fastapi import HTTPException
from app.utils.constants import FROM_EMAIL

load_dotenv()

class EmailService:
    @staticmethod
    def send_otp_email(email: str, otp: str):
        try:
            api_key = os.getenv("SENDGRID_API_KEY")

            if not api_key:
                raise Exception("SENDGRID_API_KEY not found in environment")

            message = Mail(
                from_email=FROM_EMAIL,
                to_emails=email,
                subject='Your Password Reset OTP',
                html_content=f'<strong>Your OTP is: {otp}</strong>. It expires in 15 minutes.'
            )

            sg = SendGridAPIClient(api_key)
            response = sg.send(message)

            print("Status Code:", response.status_code)

            if response.status_code >= 400:
                raise Exception(f"SendGrid error: {response.body}")

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Email failed: {str(e)}")
