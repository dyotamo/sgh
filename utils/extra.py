from typing import Dict
from flask_wtf import FlaskForm

from models import Company
from dao import get_all


def get_formdata(form: FlaskForm) -> Dict[str, str]:
    data = form.data
    data.pop('csrf_token')
    return data


def get_company_tuple():
    collection = [(str(company.id), company.name)
                  for company in get_all(Company)]
    collection.insert(0, ('', 'Nenhuma'))
    return collection
