from flask import render_template
from datetime import date


def render_template_with_today_date(template, context):
    return render_template(template, today=date.today(), **context)
