# the functions in this file should allow you to generate and confirm authentication tokens for confirming an email address. They
# can also be used to generate a one time password reset link that can be sent to the user's email address. The last function 
# should take our pre-configured Mail settings and send a message to that person. We can use different mail server configurations
# for different emails. We use a flask extension called flask_mail for this and more documentation can be found at
# https://pythonhosted.org/Flask-Mail/
from flask_mail import Message


def generate_confirmation_token(email, serializer):
    return serializer.dumps(email, salt='ughsecurity')

def confirm_email_token(token, serializer, expiration = 3600):
    try:
        email = serializer.loads(token, salt='ughsecurity', max_age = expiration)
    except:
        return False

    return email

def send_mail(to, subject, message, mail_server):
    msg = Message(subject, recipients=[to], sender='abmamo@reed.edu')
    msg.body = message
    mail_server.send(msg)


