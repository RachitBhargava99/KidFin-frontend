from flask import Blueprint, render_template, url_for, flash, redirect, current_app
from flask_login import current_user, login_required
import requests


normal = Blueprint('normal', __name__)

@login_required
@normal.route('/normal/dashboard', methods = ['POST', 'GET'])
def dashboard():
    request_response = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['ALL_ACTIVE_COMPANY_URL'],
                                     json={
                                         'auth_token': current_user.auth_token
                                     })
    data = request_response.json()
    return render_template('user_dashboard.html',
                           activity_status=data['activity_status'],
                           basics=data['basics'],
                           data=data['output'])


@login_required
@normal.route('/normal/enter/<int:company_id>', methods=['POST', 'GET'])
def enter_company_queue(company_id):
    request_response = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['ENTER_COMPANY_QUEUE_URL'],
                                     json={
                                         'auth_token': current_user.auth_token,
                                         'company_id': company_id
                                     })
    data = request_response.json()
    flash("Entered Successfully!" if data['status'] == 1 else data['error'], 'success' if data['status'] == 1 else 'danger')
    return redirect(url_for('normal.dashboard'))


@login_required
@normal.route('/normal/sessions', methods=['POST', 'GET'])
def get_session_info():
    request_response = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['SESSIONS_URL'],
                                     json={
                                         'auth_token': current_user.auth_token
                                     })
    data = request_response.json()
    if data['status'] == 0:
        flash(data['error'], 'danger')
        return redirect(url_for('dash.dashboard'))
    return render_template('user_sessions.html',
                           sessions=data['output'])


@login_required
@normal.route('/normal/opt_out', methods=['POST', 'GET'])
def exit_queue():
    request_response = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['QUEUE_EXIT_URL'],
                                     json={
                                         'auth_token': current_user.auth_token
                                     })
    data = request_response.json()
    if data['status'] == 0:
        flash(data['error'], 'danger')
    else:
        flash("Queue Exited Successfully!", 'success')
    return redirect(url_for('dash.dashboard'))
