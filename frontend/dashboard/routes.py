from flask import Blueprint, render_template, url_for, flash, redirect, request, current_app
from frontend.users.forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm
from flask_login import login_user, current_user, logout_user, login_required
import requests
import json
from frontend.models import User
from frontend.dashboard.forms import RequestHelpForm

dash = Blueprint('dash', __name__)


@dash.route('/dashboard', methods=['POST', 'GET'])
@login_required
def dashboard():
    kids_data = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['KIDS_DATA_URL'],
                              json={
                                  'auth_token': current_user.auth_token
                              }).json()
    if kids_data['status'] == 0:
        flash(kids_data['error'], 'danger')
        logout_user()
        return redirect(url_for('common.login'))
    transactions_data = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['TRANSACTION_DATA_URL'],
                                      json={
                                          'auth_token': current_user.auth_token
                                      }).json()
    if transactions_data['status'] == 0:
        flash(transactions_data['error'], 'danger')
        logout_user()
        return redirect(url_for('common.login'))
    recent_transaction = transactions_data['transactions'][-1]['amount'] if len(transactions_data['transactions']) != 0\
        else 0
    balance_data = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['CURR_BALANCE_URL'],
                                      json={
                                          'auth_token': current_user.auth_token
                                      }).json()
    if balance_data['status'] == 0:
        flash(balance_data['error'], 'danger')
        logout_user()
        return redirect(url_for('common.login'))
    print(transactions_data)
    kid_transaction = [x for x in transactions_data['transactions'] if x['name'] != current_user.name][::-1]
    recent_kid_transaction = kid_transaction[0] if len(kid_transaction) >= 1 else None
    return render_template('master_dashboard.html', data={
        'num_account': len(kids_data['kids']),
        'num_transaction': len(transactions_data['transactions']),
        'most_recent_transaction': recent_transaction,
        'curr_balance': balance_data['balance'],
        'transactions': transactions_data['transactions'],
        'recent_kid_transaction': recent_kid_transaction
    })


@dash.route('/transactions', methods=['POST', 'GET'])
@login_required
def view_transactions():
    transactions_data = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['TRANSACTION_DATA_URL'],
                                      json={
                                          'auth_token': current_user.auth_token
                                      }).json()
    if transactions_data['status'] == 0:
        flash(transactions_data['error'], 'danger')
        logout_user()
        return redirect(url_for('common.login'))
    return render_template('master_sessions.html', transactions=transactions_data['transactions'])


@dash.route('/kids', methods=['POST', 'GET'])
@login_required
def view_kids():
    kids_data = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['KIDS_DATA_URL'],
                              json={
                                  'auth_token': current_user.auth_token
                              }).json()
    if kids_data['status'] == 0:
        flash(kids_data['error'], 'danger')
        logout_user()
        return redirect(url_for('common.login'))
    return render_template('kid_listing.html', kids=kids_data['kids'])


@dash.route('/kids/restriction/<kid_id>', methods=['POST', 'GET'])
@login_required
def edit_restrictions(kid_id):
    if request.method == 'GET':
        return render_template('restrictions.html')
    data = {
        'auth_token': current_user.auth_token,
        'kid_id': kid_id
    }
    amount = int(request.form.get('amount').strip()) if request.form.get('amount').strip() != '' else None
    transaction = int(request.form.get('num_tra').strip()) if request.form.get('num_tra').strip() != '' else None
    address = request.form.get('prim_location').strip() if request.form.get('prim_location').strip() != '' else None
    distance = int(request.form.get('radius').strip()) if request.form.get('radius').strip() != '' else 1
    cat_id = request.form.getlist('cat')
    if amount:
        data['amount'] = amount
    if transaction:
        data['transaction'] = transaction
    if address:
        data['address'] = address
        data['distance'] = distance
    if len(cat_id):
        data['cat_id'] = cat_id

    request_data = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['EDIT_RESTRICTIONS_URL'],
                                 json=data).json()
    if request_data['status'] == 0:
        flash(request_data['error'], 'danger')
    else:
        flash("Restrictions Updated Successfully!", 'success')
    return redirect(url_for('dash.dashboard'))


@dash.route('/kids/add_new', methods=['POST', 'GET'])
@login_required
def add_new_kid():
    if request.method == 'GET':
        return render_template('kid_new.html')
    data = {
        'auth_token': current_user.auth_token,
        'kid_name': request.form.get('name'),
        'kid_email': request.form.get('email'),
        'init_amount': int(request.form.get('amount'))
    }
    request_data = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['ADD_KID_URL'],
                                 json=data).json()
    if request_data['status'] == 0:
        flash(request_data['error'], 'danger')
    else:
        flash(f"Kid Account Created Successfully! Login Email: {request_data['email']}," +
              f" Login Password: {request_data['password']}", 'success')
    return redirect(url_for('dash.dashboard'))


@dash.route('/request/<topic>', methods=['POST', 'GET'])
@login_required
def request_help(topic):
    request_data = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['REQUEST_HELP_URL'],
                                 json={
                                     'auth_token': current_user.auth_token,
                                     'topic': topic
                                 })
    data = request_data.json()
    if data['status'] == 1:
        flash(f"Help request submitted. Please wait for your name to be called.", 'success')
        return redirect(url_for('dash.dashboard'))
    elif data['status'] == 2:
        flash(f"Help request already exists. Please wait for your name to be called.", 'danger')
        return redirect(url_for('dash.dashboard'))
    else:
        flash(f"Sorry, your session has expired. Kindly log in again.")
        return redirect(url_for('common.login'))


@dash.route('/helper/<int:helper_id>', methods=['POST', 'GET'])
@login_required
def get_helper_info(helper_id):
    request_data = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['HELPER_INFO_URL'],
                                 json={
                                     'auth_token': current_user.auth_token,
                                     'helper_id': helper_id
                                 })
    data = request_data.json()
    if data['status'] == 0:
        flash(data['error'], 'danger')
        return redirect(url_for('dash.dashboard'))
    return render_template('helper_profile.html',
                           name=data['name'],
                           email=data['email'],
                           gt_id=data['gt_id'],
                           total_sessions=data['total_sessions'],
                           total_check_ins=data['total_check_ins'],
                           avg_sessions=round((data['total_sessions'] / data['total_check_ins']), 2),
                           sessions_past_7_days=data['total_past_7_days_sessions'],
                           last_session_date=data['last_session_date'],
                           last_session_topic=data['last_session_topic'],
                           last_session_requester=data['last_session_requester']
                           )


@dash.route('/requester/<int:requester_id>', methods=['POST', 'GET'])
@login_required
def get_requester_info(requester_id):
    request_data = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['REQUESTER_INFO_URL'],
                                 json={
                                     'auth_token': current_user.auth_token,
                                     'requester_id': requester_id
                                 })
    data = request_data.json()
    if data['status'] == 0:
        flash(data['error'], 'danger')
        return redirect(url_for('dash.dashboard'))
    return render_template('requester_profile.html',
                           name=data['name'],
                           email=data['email'],
                           gt_id=data['gt_id'],
                           total_sessions=data['total_sessions'],
                           total_no_show=data['total_sessions'] - data['total_success'],
                           success_percent=round((data['total_success'] * 100 / data['total_sessions']), 2) if data[
                                                                                                                   'total_sessions'] != 0 else "N/A",
                           sessions_past_7_days=data['total_past_7_days_sessions'],
                           last_session_date=data['last_session_date'],
                           last_session_topic=data['last_session_topic'],
                           last_session_helper=data['last_session_helper']
                           )


@dash.route('/all/helpers', methods=['POST', 'GET'])
@login_required
def get_all_helpers():
    request_data = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['ALL_HELPERS_URL'],
                                 json={
                                     'auth_token': current_user.auth_token
                                 })
    data = request_data.json()
    if data['status'] == 0:
        flash(data['error'], 'danger')
        return redirect(url_for('dash.dashboard'))
    return render_template('helpers.html',
                           helpers=data['helper_data'])


@dash.route('/all/requesters', methods=['POST', 'GET'])
@login_required
def get_all_requesters():
    request_data = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['ALL_REQUESTERS_URL'],
                                 json={
                                     'auth_token': current_user.auth_token
                                 })
    data = request_data.json()
    if data['status'] == 0:
        flash(data['error'], 'danger')
        return redirect(url_for('dash.dashboard'))
    return render_template('requesters.html',
                           requesters=data['requester_data'])
