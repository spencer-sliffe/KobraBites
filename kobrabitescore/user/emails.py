"""
FOR THE FUTURE:

@register_template('forgot-password', 'Password reset', example_context=_FORGOT_PASSWORD)
def forgot_password(user: CustomUser, host=None) -> dict:
    uid = user.get_uid()
    host = settings.ADMIN_HOST if host and host in (settings.ADMIN_HOST or '') else settings.APP_HOST
    return {
        'subject': 'Password Reset',
        'reset_href': f'{host}/reset-password/{uid}/{user.reset_token}',
    }


"""