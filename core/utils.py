import threading

# Thread-local storage
_current_company = threading.local()

def get_current_company():
    return getattr(_current_company, 'value', None)

def set_current_company(company):
    _current_company.value = company