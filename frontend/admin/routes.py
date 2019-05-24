from flask import Blueprint, render_template, current_app, flash, redirect, url_for
from flask_login import current_user, login_required
import requests
from frontend.admin.forms import AddRecruiterForm


admin = Blueprint('admin', __name__)


@login_required
@admin.route('/admin/dashboard', methods=['POST', 'GET'])
def dashboard():
    request_data = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['ADMIN_DASHBOARD_INFO_URL'],
                         json={
                             'auth_token': current_user.auth_token
                         })
    data = request_data.json()
    return render_template('helper_dashboard.html', queue_length=data['queue_length'],
                           recruiters_active=data['helpers_active'],
                           estimated_wait_time=int(data['estimated_wait_time']) if
                           type(data['estimated_wait_time']) is not str else "N/A",
                           total_sessions=data['sessions_today'],
                           last_session_date=data['last_session_date'],
                           last_session_requester=data['last_session_requester'],
                           recs=data['online_recs'], curr_sessions=data['curr_sessions'])


@login_required
@admin.route('/admin/sessions', methods=['POST', 'GET'])
def get_session_info():
    request_response = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['SESSIONS_URL'],
                                     json={
                                         'auth_token': current_user.auth_token
                                     })
    data = request_response.json()
    if data['status'] == 0:
        flash(data['error'], 'danger')
        return redirect(url_for('dash.dashboard'))
    return render_template('helper_sessions.html',
                           sessions=data['output'])


@login_required
@admin.route('/admin/recruiter/add', methods=['POST', 'GET'])
def add_recruiter():
    form = AddRecruiterForm()
    if form.validate_on_submit():
        request_response = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['ADD_RECRUITER_URL'],
                                         json={
                                             'auth_token': current_user.auth_token,
                                             'name': form.name.data
                                         })
        data = request_response.json()
        if data['status'] == 1:
            flash("Recruiter Added Successfully", 'success')
        else:
            flash(data['error'], 'danger')
        return redirect(url_for('admin.add_recruiter'))
    return render_template('add_recruiter.html',
                           form=form)


@login_required
@admin.route('/admin/no_show/<int:session_id>', methods=['POST', 'GET'])
def mark_no_show(session_id):
    request_response = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['NO_SHOW_URL'],
                                     json={
                                         'auth_token': current_user.auth_token,
                                         'session_id': session_id
                                     })
    data = request_response.json()
    if data['status'] == 1:
        flash("User Marked No Show Successfully", 'success')
    else:
        flash(data['error'], 'danger')
    return redirect(url_for('admin.dashboard'))


@login_required
@admin.route('/admin/done/<int:session_id>', methods=['POST', 'GET'])
def mark_done(session_id):
    request_response = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['DONE_URL'],
                                     json={
                                         'auth_token': current_user.auth_token,
                                         'session_id': session_id
                                     })
    data = request_response.json()
    if data['status'] == 1:
        flash("Great job! You may continue.", 'success')
    else:
        flash(data['error'], 'danger')
    return redirect(url_for('admin.dashboard'))
