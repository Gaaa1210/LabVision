from datetime import date, datetime

def parse_date_string(date_str: str, date_format: str = "%d/%m/%Y") -> date | None:
    """
    Converte uma string de data para um objeto date.
    Retorna o objeto date ou None se a string não puder ser convertida.
    Ex: parse_date_string("15/06/1990")
    """
    try:
        return datetime.strptime(date_str, date_format).date()
    except ValueError:
        return None

def format_date_to_string(date_obj: date, date_format: str = "%d/%m/%Y") -> str:
    """
    Converte um objeto date para uma string formatada.
    Ex: format_date_to_string(date(1990, 6, 15)) -> "15/06/1990"
    """
    return date_obj.strftime(date_format)