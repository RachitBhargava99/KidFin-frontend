from flask import Blueprint, render_template, url_for, flash, redirect, current_app
from flask_login import current_user, login_required, logout_user
from frontend.master.forms import AddCompanyForm, AddCompanyAdminForm
import requests


master = Blueprint('master', __name__)


@login_required
@master.route('/master/dashboard', methods=['POST', 'GET'])
def dashboard():
    request_response = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['MASTER_DASH_INFO_URL'],
                                     json={
                                         'auth_token': current_user.auth_token
                                     })
    data = request_response.json()
    if data['status'] == 0:
        logout_user()
        flash(data['error'], 'danger')
        return redirect(url_for('common.login'))
    return render_template('master_dashboard.html',
                           data=data['output'])


@login_required
@master.route('/master/company/add', methods=['POST', 'GET'])
def add_new_company():
    form = AddCompanyForm()
    if form.validate_on_submit():
        request_response = requests.post(
            current_app.config['ENDPOINT_ROUTE'] + current_app.config['ADD_COMPANY_URL'],
            json={
                'auth_token': current_user.auth_token,
                'company_name': form.name.data,
                'rep_name': form.rep_name.data,
                'rep_email': form.rep_email.data,
                'num_reps': form.num_reps.data,
                'website': form.website.data
            })
        data = request_response.json()
        if data['status'] == 1:
            requests.post(
                current_app.config['ENDPOINT_ROUTE'] + current_app.config['ADD_COMPANY_ADMIN_URL'],
                json={
                    'auth_token': current_user.auth_token,
                    'company_id': data['company_id'],
                    'name': form.rep_name.data,
                    'email': form.rep_email.data,
                    'designation': "Recruiter"
                })
            flash("Company Added Successfully", 'success')
        else:
            flash(data['error'], 'danger')
        return redirect(url_for('master.add_new_company'))
    return render_template('add_company.html',
                           form=form)


@login_required
@master.route('/master/company/add_user', methods=['POST', 'GET'])
def add_company_admin():
    data1 = requests.post(
        current_app.config['ENDPOINT_ROUTE'] + current_app.config['GET_COMPANY_DATA_URL'],
        json={
            'auth_token': current_user.auth_token
        }
    ).json()
    if data1['status'] == 0:
        flash(data1['error'], 'danger')
        return redirect(url_for('dash.dashboard'))

    form = AddCompanyAdminForm(data1['choices'])

    if form.is_submitted():
        request_response = requests.post(
            current_app.config['ENDPOINT_ROUTE'] + current_app.config['ADD_COMPANY_ADMIN_URL'],
            json={
                'auth_token': current_user.auth_token,
                'company_id': form.company.data,
                'name': form.name.data,
                'email': form.email.data,
                'designation': form.designation.data
            })
        data = request_response.json()
        if data['status'] == 1:
            flash("Company Added Successfully", 'success')
        else:
            flash(data['error'], 'danger')
        return redirect(url_for('master.add_company_admin'))
    return render_template('add_company_admin.html',
                           form=form)


@master.route('/master/sessions', methods=['POST', 'GET'])
def get_session_info():
    request_response = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['SESSIONS_URL'],
                                     json={
                                         'auth_token': current_user.auth_token
                                     })
    data = request_response.json()
    if data['status'] == 0:
        flash(data['error'], 'danger')
        return redirect(url_for('dash.dashboard'))
    return render_template('master_sessions.html',
                           sessions=data['output'])


@master.route('/master/company', methods=['POST', 'GET'])
def get_company_list():
    request_response = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['LISTS_URL'],
                                     json={
                                         'auth_token': current_user.auth_token,
                                         'req': "company"
                                     })
    data = request_response.json()
    if data['status'] == 0:
        flash(data['error'], 'danger')
        return redirect(url_for('dash.dashboard'))
    return render_template('common_list.html',
                           req="Company",
                           sessions=data['output'])


@master.route('/master/recruiter', methods=['POST', 'GET'])
def get_recruiter_list():
    request_response = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['LISTS_URL'],
                                     json={
                                         'auth_token': current_user.auth_token,
                                         'req': "recruiter"
                                     })
    data = request_response.json()
    if data['status'] == 0:
        flash(data['error'], 'danger')
        return redirect(url_for('dash.dashboard'))
    return render_template('common_list.html',
                           req="Recruiter",
                           sessions=data['output'])


@master.route('/master/candidate', methods=['POST', 'GET'])
def get_candidate_list():
    request_response = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['LISTS_URL'],
                                     json={
                                         'auth_token': current_user.auth_token,
                                         'req': "candidate"
                                     })
    data = request_response.json()
    if data['status'] == 0:
        flash(data['error'], 'danger')
        return redirect(url_for('dash.dashboard'))
    return render_template('common_list.html',
                           req="Candidate",
                           sessions=data['output'])
