from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from .forms import QuestionsForm
from .. import db
from ..models import User


def check_admin():
    """
    Prevent non-admins from accessing the page
    """

    if not current_user.is_admin:
        abort(403)
