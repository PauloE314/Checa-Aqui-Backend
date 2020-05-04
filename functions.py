from django.core.mail import send_mail, EmailMessage
from backend.settings import EMAIL_HOST_USER, BASE_DIR
from django.template.loader import render_to_string
from email.mime.image import MIMEImage

import os

def send_attendance_start_email(attendance):
    # print(attendance)

    subject = 'Atendimento solicitado - Checa Aqui'
    # message = f'Ativação de email, Token de ativação: {token}'
    html_message = render_to_string('attendance_start_email.html', {
        'attendant': attendance.attendant,
        'client': attendance.client,
        'product': attendance.product,
        'phone': attendance.client.profile.phone
    })

    image_path = os.path.join(BASE_DIR, os.path.join('templates', 'Ativo 1.png'))
    print(image_path)


    email = EmailMessage(subject, html_message, EMAIL_HOST_USER, [attendance.attendant.profile.email])

    email.content_subtype = "html"
    email.mixed_subtype = 'related'

    with open(image_path, mode='rb') as file:
        image = MIMEImage(file.read())
        email.attach(image)
        image.add_header('Content-ID', f"<Ativo_1>")

    email.send()



def send_validation(email, token):
    subject = 'Validação de email - Checa Aqui'
    # message = f'Ativação de email, Token de ativação: {token}'
    html_message = render_to_string('validation_email.html', {'token': token})
    image_path = os.path.join(BASE_DIR, os.path.join('templates', 'Ativo 1.png'))
    print(image_path)

    email = EmailMessage(subject, html_message, EMAIL_HOST_USER, [email])
    email.content_subtype = "html"
    email.mixed_subtype = 'related'

    with open(image_path, mode='rb') as file:
        image = MIMEImage(file.read())
        email.attach(image)
        image.add_header('Content-ID', f"<Ativo_1>")

    email.send()
    

    return False


def update_instance(instance, data, fields=None):
    change = False
    if not fields:
        fields = data

    for field in fields:
        if field in instance.__dict__ and field in data:
            setattr(instance, field, data[field])
            change = True

    if change:
        instance.save()

    return instance