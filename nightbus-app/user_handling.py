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


