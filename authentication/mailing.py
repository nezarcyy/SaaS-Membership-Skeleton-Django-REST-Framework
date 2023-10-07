from djoser import email


class ActivationEmail(email.ActivationEmail):
    template_name = 'authentication/ActivationEmail.html'


class ConfirmationEmail(email.ConfirmationEmail):
    template_name = 'authentication/ConfirmationEmail.html'


class PasswordResetEmail(email.PasswordResetEmail):
    template_name = "authentication/PasswordResetEmail.html"

class PasswordChangedConfirmationEmail(email.PasswordChangedConfirmationEmail):
    template_name = "authentication/PasswordChangedConfirmation.html"


class UsernameChangedConfirmationEmail(email.UsernameChangedConfirmationEmail):
    template_name = "authentication/UsernameChangedConfirmation.html"


class UsernameResetEmail(email.UsernameResetEmail):
    template_name = "authentication/UsernameResetEmail.html"