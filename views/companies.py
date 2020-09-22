from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required
from playhouse.flask_utils import object_list

from models import Company
from dao import get_all, create, get, update
from forms.company import CompanyForm
from utils.security import allowed_profile
from utils.extra import get_formdata
from utils.validators import validate_company


companies = Blueprint('companies', __name__, url_prefix='/companies')


@companies.route('/', methods=['GET'])
@login_required
@allowed_profile(['receptionist', 'manager', 'admin'])
def company_index():
    return object_list('companies/index.html', query=get_all(Company),
                       context_variable='companies', paginate_by=7, check_bounds=False)


@companies.route('/new', methods=['GET', 'POST'])
@login_required
@allowed_profile(['receptionist', 'manager', 'admin'])
def company_new():
    company = Company()
    if request.method == 'POST':
        form = CompanyForm(request.form, obj=company)
        if form.validate():
            try:
                form.populate_obj(company)
                validate_company(company)
                company.save()
                flash('Yes, empresa cadastrada com sucesso.', 'success')
                return redirect(url_for('companies.company_index'))
            except AttributeError as e:
                flash(str(e), 'warning')
    else:
        form = CompanyForm(obj=company)
    return render_template('companies/new.html', form=form)


@companies.route('/<int:company_id>', methods=['GET'])
@login_required
@allowed_profile(['receptionist', 'manager', 'admin'])
def company_details(company_id: int):
    return render_template('companies/details.html', company=get(Company, company_id))


@companies.route('/<int:company_id>/edit', methods=['GET', 'POST'])
@login_required
@allowed_profile(['receptionist', 'manager', 'admin'])
def company_edit(company_id: int):
    company = get(Company, company_id)
    if request.method == 'POST':
        form = CompanyForm(request.form, obj=company)
        if form.validate():
            try:
                form.populate_obj(company)
                validate_company(company)
                company.save()
                flash('Yes, empresa alterada com sucesso.', 'success')
                return redirect(url_for('companies.company_index'))
            except AttributeError as e:
                flash(str(e), 'warning')
    else:
        form = CompanyForm(obj=company)
    return render_template('companies/edit.html', form=form)
