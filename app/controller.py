import flask_login

from app.app import app_utm_sugarcrm_report
from app.helpers import render_template_with_today_date


@app_utm_sugarcrm_report.route('/')
@flask_login.login_required
def index():
    return render_template_with_today_date(
        'index.html', {'current_user': flask_login.current_user}
    )
