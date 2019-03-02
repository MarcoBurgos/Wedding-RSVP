from flask import Blueprint,render_template
from flask_dance.contrib.google import make_google_blueprint, google

error_pages = Blueprint('error_pages',__name__)

@error_pages.app_errorhandler(404)
def error_404(error):
    return render_template('error_pages/404.html'), 404

@error_pages.app_errorhandler(403)
def error_403(error):
    if not google.authorized:
        return redirect(url_for("google.login"))

    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    email=resp.json()["email"]
    return render_template('error_pages/403.html', email=email), 403
