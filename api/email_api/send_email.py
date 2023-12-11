from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# ↓↓↓↓↓ prompt functions


class PromptEmail():
    def __init__(self, contact_data=None):
        self.contact_data = contact_data

    def send_prompt_email_purchase(self):
        """Mock email sending by printing to a file"""

        import random
        import string
        length = 12
        chars = string.digits

        customer_name = self.contact_data.get("name").title(
        ) + " " + self.contact_data.get("surname").title()

        order_number = ''.join(random.choice(chars) for i in range(length))

        PURCHASE_MAIL = f"""
        From: Napptilus Ecomm <no-reply@napptilus-ecomm.com>
        To: {self.contact_data.get("email")}
        Subject: f"Ecomm-Napptilus Order {order_number} 🎁🎁"

        Hello,
        {customer_name}
        We are preparing your purchases with great care 🥰.
        To track the status of your order {order_number}, please visit our website "https://napptilus.com/".
        Keep counting on us. ❤️❤️
        Ecomm-Napptilus Team  """

        return PURCHASE_MAIL

    def send_prompt_email_report(email):
        from datetime import datetime

        import pytz

        """Mock email sending by printing to a file"""

        REPORT_MAIL = f"""
        From: Napptilus Ecomm <tech@napptilus-ecomm.com>
        To: {email}
        Subject: f"Inventory accuracy report submission - {datetime.now(pytz.utc)}"

        Attached is the link to the inventory report of the products "https://napptilus.com/".
        Please do not unsubscribe from receiving this email
        If you have any questions or issues, please contact your supervisor
        """

        return REPORT_MAIL


# ↓↓↓↓↓ queue sendgrid backend functions


def purchase_email_sending(customer_data, SENDGRID_API_KEY):
    import random
    import string
    length = 12
    chars = string.digits
    order_number = ''.join(random.choice(chars) for i in range(length))

    customer_name = customer_data.get("name").title(
    ) + " " + customer_data.get("surname").title()

    html_message = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8">
                    <title>Order Status</title>
                </head>
                <body>
                    <p>Hello, </p>
                    <h4><p><strong>{customer_name}</strong>,</p></h4>
                    <p>We are preparing your purchases with great care &#129392;.</p>
                    <p>To track the status of your order <strong>{order_number}</strong>, please visit <a href="https://napptilus.com/">our website</a>.</p>
                    <p>Keep counting on us. ❤️❤️</p>
                    <p>Ecomm-Napptilus Team</p>
                </body>
                </html>
                """
    message = Mail(
        from_email=('bbereoff@gmail.com', 'Ecomm-Napptilus'),
        to_emails=[customer_data.get("email")],
        html_content=html_message,
        subject=f"Ecomm-Napptilus Order {order_number} 🎁🎁",
    )

    try:
        response = SendGridAPIClient(SENDGRID_API_KEY).send(message)
        return response.status_code
    except Exception as e:
        print(e)


def report_email_sending(email, SENDGRID_API_KEY):
    from datetime import datetime

    import pytz

    html_message = """
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8">
                    <title>Order Status</title>
                </head>
                <body>
                    <p>Attached is the link to the inventory report of the products <a href="https://napptilus.com/">our website</a>.</p>
                    <p>Please do not unsubscribe from receiving this email.</p>
                    <p>If you have any questions or issues, please contact your supervisor.</p>
                </body>
                </html>
                """
    message = Mail(
        from_email=('bbereoff@gmail.com', 'Ecomm-Napptilus'),
        to_emails=[email],
        html_content=html_message,
        subject=f"Inventory accuracy report submission - {datetime.now(pytz.utc)}",
    )

    try:
        response = SendGridAPIClient(SENDGRID_API_KEY).send(message)
        return response
    except Exception as e:
        print(e)
