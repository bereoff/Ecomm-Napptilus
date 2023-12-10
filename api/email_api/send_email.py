from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_mail(customer_data, api_key):
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
        response = SendGridAPIClient(api_key).send(message)
        return response.status_code
    except Exception as e:
        print(e)
