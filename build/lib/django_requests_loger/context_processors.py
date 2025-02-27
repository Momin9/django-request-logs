from django.conf import settings


def dynamic_login_settings(request):
    """
    Returns dynamic settings for the login page (logo, heading, etc.)
    These can be overridden in settings.py as needed.
    """
    return {
        # Fallback to a default if not found in settings
        "LOGIN_PAGE_LOGO": getattr(settings, "LOGIN_PAGE_LOGO", "images/FamilyTime Logo-1200 x 1200.png"),
        "LOGIN_PAGE_HEADING": getattr(settings, "LOGIN_PAGE_HEADING", "WELCOME TO FAMILYTIME <br>(MDM REQUESTS)"),
    }


def ui_settings(request):
    """
    Injects dynamic UI settings into templates, e.g., brand logo, project name, and sidebar links.
    """
    config = getattr(settings, "DJANGO_REQUESTS_LOGER_UI", {})
    return {
        "BRAND_LOGO": config.get("BRAND_LOGO", "images/default_logo.png"),
        "PROJECT_NAME": config.get("PROJECT_NAME", "My Project"),
        "SIDEBAR_LINKS": config.get("SIDEBAR_LINKS", []),
    }
