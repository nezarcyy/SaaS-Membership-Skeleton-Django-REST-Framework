from djoser import email


class ActivationEmail(email.ActivationEmail):
    template_name = 'authentication/ActivationEmail.html'

class ConfirmationEmail(email.ConfirmationEmail):
    template_name = 'authentication/ConfirmationEmail.html'