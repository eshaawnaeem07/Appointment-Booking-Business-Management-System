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

    @staticmethod
    def send_payment_confirmation_email(email: str, service_name: str, appointment_time):
        try:
            api_key = os.getenv("SENDGRID_API_KEY", "").strip()
            from_email = os.getenv("FROM_EMAIL", "").strip()

            if not api_key or not from_email:
                raise Exception("Missing SendGrid configuration")

            message = Mail(
                from_email=from_email,
                to_emails=email,
                subject="Payment Confirmed - Appointment Booking",
                html_content=f"""
                <h2>Payment Confirmation</h2>
                <p>Your payment has been successfully received!</p>
                <p><strong>Service:</strong> {service_name}</p>
                <p><strong>Appointment Time:</strong> {appointment_time.strftime('%Y-%m-%d %H:%M')}</p>
                <p>Your appointment is now confirmed. Thank you for booking with us!</p>
                """
            )

            sg = SendGridAPIClient(api_key)
            response = sg.send(message)

            if response.status_code >= 400:
                raise Exception(f"SendGrid error: {response.status_code}")

        except Exception as e:
            print(f"Failed to send payment confirmation email: {str(e)}")

    @staticmethod
    def send_payment_failed_email(email: str, service_name: str):
        try:
            api_key = os.getenv("SENDGRID_API_KEY", "").strip()
            from_email = os.getenv("FROM_EMAIL", "").strip()

            if not api_key or not from_email:
                raise Exception("Missing SendGrid configuration")

            message = Mail(
                from_email=from_email,
                to_emails=email,
                subject="Payment Failed - Please Retry",
                html_content=f"""
                <h2>Payment Failed</h2>
                <p>Unfortunately, your payment could not be processed.</p>
                <p><strong>Service:</strong> {service_name}</p>
                <p>Please try again with a different payment method or contact support if the problem persists.</p>
                """
            )

            sg = SendGridAPIClient(api_key)
            response = sg.send(message)

            if response.status_code >= 400:
                raise Exception(f"SendGrid error: {response.status_code}")

        except Exception as e:
            print(f"Failed to send payment failed email: {str(e)}")
