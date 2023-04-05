from datetime import datetime

def format_date(date):
    return datetime.strptime(date, "%d/%m/%Y")