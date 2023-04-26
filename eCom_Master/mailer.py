import os
from store.models import *
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def sendMail(customer, items, transaction_id, total):
    text = "Thanks a lot for making this Presentation Successful!. Here are your Order Details:"
    text += "\n Order ID: " + str(transaction_id)
    text += "\n Order Total: " + str(total)
    text += "\n Order Items:"
    for i in items:
        product = Product.objects.get(id=i['id'])
        text += "\n" + product.name
        text += "\n Quantity: " + str(i['quantity'])
    message = Mail(
        from_email='abhishekmalik2903@gmail.com',
        to_emails=customer.email,
        subject='Sending with Twilio SendGrid is Fun',
        html_content=text)
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)