"""
Verify Google reCAPTCHA responses in a Django login view.

Demonstrates backend verification of client-side reCAPTCHA tokens.
Get keys at: https://www.google.com/recaptcha/admin/create

Note: reCAPTCHA does not work with localhost.

HTML form snippet:
    <div class="g-recaptcha" data-sitekey="YOUR_CLIENT_KEY"></div>
    <script src="https://www.google.com/recaptcha/api.js" async defer></script>
"""

import requests

RECAPTCHA_VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"

try:
    from django.contrib.auth import authenticate, login
    from django.shortcuts import redirect, render
except ImportError:
    authenticate = login = render = redirect = print  # type: ignore[assignment]


def verify_recaptcha(secret_key: str, client_response: str) -> bool:
    """
    Post the reCAPTCHA response to Google and return True if valid.

    >>> verify_recaptcha("bad_key", "bad_response")  # doctest: +SKIP
    False
    """
    response = requests.post(
        RECAPTCHA_VERIFY_URL,
        data={"secret": secret_key, "response": client_response},
        timeout=10,
    )
    return response.json().get("success", False)


def login_using_recaptcha(request):
    """
    Django view: authenticate user only if reCAPTCHA verification passes.

    When method is not POST, render the login page.
    """
    secret_key = "YOUR_SECRET_KEY"  # noqa: S105
    if request.method != "POST":
        return render(request, "login.html")
    username = request.POST.get("username")
    password = request.POST.get("password")
    client_key = request.POST.get("g-recaptcha-response")
    if verify_recaptcha(secret_key, client_key):
        user_in_database = authenticate(request, username=username, password=password)
        if user_in_database:
            login(request, user_in_database)
            return redirect("/your-webpage")
    return render(request, "login.html")


if __name__ == "__main__":
    print("This module is designed to be used as a Django view.")
    print("Import login_using_recaptcha and wire it to a URL pattern.")
