import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class EmailService:
    @staticmethod
    def send_otp_email(email: str, otp: str):
        message = Mail(
            from_email='eshaanaeem07@gmail.com',
            to_emails=email,
            subject='Your Password Reset OTP',
            html_content=f'<strong>Your OTP is: {otp}</strong>. It expires in 15 minutes.')
        try:
            api_key = os.environ.get('SENDGRID_API_KEY')
            sg = SendGridAPIClient(api_key)
            response = sg.send(message)
           
            print(f"Status Code: {response.status_code}") 
            print(f"Response Body: {response.body}")
        except Exception as e:
            print(f"Error sending email: {e}")