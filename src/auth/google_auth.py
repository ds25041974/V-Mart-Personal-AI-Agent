"""
Handles Google Authentication for V-Mart Personal AI Agent.
"""

from authlib.integrations.flask_client import OAuth
from flask import Blueprint, redirect, session, url_for

# Allowed domains for authentication
ALLOWED_DOMAINS = ["www.vmart.co.in", "www.vmartretail.com", "www.limeroad.com"]

oauth = OAuth()
auth_bp = Blueprint("auth", __name__)


def init_app(app):
    oauth.init_app(app)
    oauth.register(
        name="google",
        client_id=app.config["GOOGLE_CLIENT_ID"],
        client_secret=app.config["GOOGLE_CLIENT_SECRET"],
        access_token_url="https://accounts.google.com/o/oauth2/token",
        access_token_params=None,
        authorize_url="https://accounts.google.com/o/oauth2/auth",
        authorize_params=None,
        api_base_url="https://www.googleapis.com/oauth2/v1/",
        userinfo_endpoint="https://openidconnect.googleapis.com/v1/userinfo",
        client_kwargs={"scope": "openid email profile"},
    )
    app.register_blueprint(auth_bp)


@auth_bp.route("/login")
def login():
    redirect_uri = url_for("auth.authorize", _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@auth_bp.route("/authorize")
def authorize():
    token = oauth.google.authorize_access_token()
    user_info = oauth.google.parse_id_token(token)

    # Check if user's domain is allowed
    if user_info["hd"] not in ALLOWED_DOMAINS:
        return "Access denied. Your domain is not authorized.", 403

    session["user"] = user_info
    return redirect("/")


@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")
