import functools

from flask import session, url_for, redirect


def needs_auth(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if "api_key" not in session:
            return redirect(url_for("root.root"))
        return f(*args, **kwargs)

    return wrapper


def allowed_file(filename, extensions):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in extensions
