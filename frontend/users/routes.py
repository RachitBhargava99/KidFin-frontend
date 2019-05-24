from flask import Blueprint, render_template, url_for, flash, redirect, request, current_app
from frontend.users.forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm
from flask_login import login_user, current_user, logout_user, login_required
import requests
import json
from frontend.models import User
from frontend import db


users = Blueprint('users', __name__)

@users.route('/logout')
@login_required
def logout():
    logout_user()
    flash(f"You have logged out successfully.", 'success')
    return redirect(url_for('common.login'))

@users.route('/reset_password', methods = ['GET', 'POST'])
def request_reset():
    if current_user.is_authenticated:
        return redirect(url_for('dash.dashboard'))
    form = RequestResetForm()
    if form.validate_on_submit():
        request_response = requests.post(current_app.config['ENDPOINT_URL'] + url_for('backend.users.request_reset_password'),
                                          json = {
                                              'email': form.email.data
                                          })
        response = json.loads(request_response)
        if response['status'] == 1:
            flash(f"Please check your inbox for an email with instructions to reset the password.")
        else:
            flash(response['error'])
        return redirect(url_for('common.login'))
    return render_template('request_reset.html', title = "Request Reset Password", form = form)

@users.route('/reset/<token>', methods = ['GET', 'POST'])
def reset(token):
    if current_user.is_authenticated:
        return redirect(url_for('dash.dashboard'))
    request_response = requests.post(current_app.config['ENDPOINT_URL'] + url_for('backend.users.verify_reset_token'),
                                     json = {
                                         'token': token
                                     })
    response = json.loads(request_response)
    if response['status'] == 0:
        flash(response['error'], 'warning')
        return redirect(url_for('frontend.users.request_reset'))
    else:
        form = ResetPasswordForm()
        request_response = request.posts(current_app.config['ENDPOINT_URL'] + url_for('backend.users.reset_password'),
                                         json = {
                                             'token': token,
                                             'password': form.password.data
                                         })
        response = json.loads(request_response)
        if response['status'] == 1:
            flash(f'Your password has been reset.', 'success')
            return redirect(url_for('common.login'))
    return render_template('reset.html', title = "Reset Password", form = form)

@users.route('/check_in', methods = ['GET', 'POST'])
@login_required
def helper_check_in():
    request_data = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['HELPER_CHECK_IN_URL'],
                                 json={
                                     'auth_token': current_user.auth_token,
                                     'type': 1
                                 })
    data = request_data.json()
    if data['status'] == 0:
        flash(data['error'], 'danger')
        logout_user()
        return redirect(url_for('common.login'))
    elif data['status'] == 1:
        flash("Checked In Successfully!", 'success')
        return redirect(url_for('dash.dashboard'))

@users.route('/check_in/<int:user_id>', methods = ['GET', 'POST'])
@login_required
def helper_check_in_i(user_id):
    request_data = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['HELPER_CHECK_IN_URL'],
                                 json={
                                     'auth_token': current_user.auth_token,
                                     'type': 2,
                                     'user_id': user_id
                                 })
    data = request_data.json()
    if data['status'] == 0:
        flash(data['error'], 'danger')
        logout_user()
        return redirect(url_for('common.login'))
    elif data['status'] == 1:
        flash("Checked In Successfully!", 'success')
        return redirect(url_for('dash.dashboard'))

@users.route('/check_out', methods = ['GET', 'POST'])
@login_required
def helper_check_out():
    request_data = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['HELPER_CHECK_OUT_URL'],
                                 json={
                                     'auth_token': current_user.auth_token,
                                     'type': 1
                                 })
    data = request_data.json()
    if data['status'] == 0:
        flash(data['error'], 'danger')
        logout_user()
        return redirect(url_for('common.login'))
    elif data['status'] == 1:
        flash("Checked In Successfully!", 'success')
        return redirect(url_for('dash.dashboard'))

@users.route('/check_out/<int:user_id>', methods = ['GET', 'POST'])
@login_required
def helper_check_out_i(user_id):
    request_data = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['HELPER_CHECK_OUT_URL'],
                                 json={
                                     'auth_token': current_user.auth_token,
                                     'type': 2,
                                     'user_id': user_id
                                 })
    data = request_data.json()
    if data['status'] == 0:
        flash(data['error'], 'danger')
        logout_user()
        return redirect(url_for('common.login'))
    elif data['status'] == 1:
        flash("Checked In Successfully!", 'success')
        return redirect(url_for('dash.dashboard'))

@users.route('/no_show', methods = ['GET', 'POST'])
@login_required
def helper_user_no_show():
    request_data = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['HELPER_NOT_FOUND_URL'],
                                 json={
                                     'auth_token': current_user.auth_token
                                 })
    data = request_data.json()
    if data['status'] == 0:
        flash(data['error'], 'danger')
        logout_user()
        return redirect(url_for('common.login'))
    elif data['status'] == 1:
        flash("User marked 'No Show'. You may now continue.", 'success')
        return redirect(url_for('dash.dashboard'))

@users.route('/helped', methods = ['GET', 'POST'])
@login_required
def helper_user_helped():
    request_data = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['HELPER_HELPED_URL'],
                                 json={
                                     'auth_token': current_user.auth_token
                                 })
    data = request_data.json()
    if data['status'] == 0:
        flash(data['error'], 'danger')
        logout_user()
        return redirect(url_for('common.login'))
    elif data['status'] == 1:
        flash("Awesome Job! You may now continue.", 'success')
        return redirect(url_for('dash.dashboard'))

@users.route('/users/sessions', methods = ['GET', 'POST'])
@login_required
def get_session_data_u():
    request_data = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['USER_SESSIONS_URL'],
                                 json={
                                     'auth_token': current_user.auth_token
                                 })
    data = request_data.json()
    if data['status'] == 0:
        flash(data['error'], 'danger')
        logout_user()
        return redirect(url_for('common.login'))
    elif data['status'] == 1:
        return render_template('user_sessions.html', title="Sessions | Helpify", sessions=data['data'])


@users.route('/helpers', methods = ['GET', 'POST'])
@login_required
def get_helpers_info():
    request_data = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['HELPERS_ONLINE_URL'],
                                 json={
                                     'auth_token': current_user.auth_token
                                 })
    data = request_data.json()
    if data['status'] == 0:
        flash(data['error'], 'danger')
        logout_user()
        return redirect(url_for('common.login'))
    elif data['status'] == 1:
        if data['user_type'] == "Admin":
            return render_template('helpers_online_a.html', title="Helpers | Helpify", helpers=data['data'])
        elif data['user_type'] == "Normal":
            return render_template('helpers_online_u.html', title="Helpers | Helpify", helpers=data['data'])
