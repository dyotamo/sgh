from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required

from models import Company
from dao import get_all, create, get, update
from forms.company import CompanyForm
from utils.security import allowed_profile
from utils.extra import get_formdata
from utils.validators import validate_company


companies = Blueprint('companies', __name__, url_prefix='/companies')


@companies.route('/', methods=['GET'])
@login_required
@allowed_profile(['receptionist', 'manager'])
def company_index():
    return render_template('companies/index.html', companies=get_all(Company))


@companies.route('/new', methods=['GET', 'POST'])
@login_required
@allowed_profile(['receptionist', 'manager'])
def company_new():
    form = CompanyForm()

    if form.validate_on_submit():
        try:
            data = get_formdata(form)
            validate_company(data)
            create(Company, **data)

            flash('Quarto cadastrado.', 'success')
            return redirect(url_for('companies.company_index'))
        except AttributeError as e:
            flash(str(e), 'danger')
    return render_template('companies/new.html', form=form)


@companies.route('/<int:company_id>/edit', methods=['GET', 'POST'])
@login_required
@allowed_profile(['receptionist', 'manager'])
def company_edit(company_id):
    form = CompanyForm(obj=get(Company, company_id))

    if form.validate_on_submit():
        try:
            data = get_formdata(form)
            validate_company(data)
            update(Company, company_id, **data)

            flash('Quarto alterado.', 'success')
            return redirect(url_for('companies.company_index'))
        except AttributeError as e:
            flash(str(e), 'danger')
    return render_template('companies/edit.html', form=form)
