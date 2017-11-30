# coding: utf-8
from datetime import datetime as dt
import logging
# from . import app


def string2bool(value, key=''):
    """
    A little helper function to convert the string 'true' or 'false' to the boolean True or False
    regardless of the case (works with True, TRUE, FaLsE, ...)
    If the input string is neither "True" nor "False", the function returns its value.
    """
    logger = logging.getLogger(__name__)
    try:
        v = value.upper()
    except AttributeError:  # if value is None or not a string
        logger.debug(f'msg="string2bool: value is None or not a string: {value}')
        return value
    else:
        logger.debug(f'msg="string2bool: original value of {key} is {value}"')
        if v == "TRUE":
            logger.debug(f'msg="string2bool: new value of {key} is True"')
            return True
        elif v == "FALSE":
            logger.debug(f'msg="string2bool: new value of {key} is False"')
            return False
        else:
            logger.debug(f'msg="string2bool: no change to {key}: {value}"')
            return value


#@app.template_filter()
def pretty_date(value, date_format='%d/%m/%Y'):
    """
    Function used to format dates to DD/MM/YYYY
    """
    logger = logging.getLogger(__name__)

    try:
        date_value = dt.strptime(value.replace(':', ''), '%Y-%m-%dT%H%M%S%z')
    except AttributeError as err:
        logger.error(f'msg="Error: invalid variable: {value}" err="{err}"')
        return value
    except ValueError as err:
        logger.error(f'msg="Error: invalid date format: {value}" err="{err}"')
        return value

    return date_value.strftime(date_format)


# Todo: use pytz module to build a 'Europe/Paris' date
#@app.context_processor
def inject_today():
    return {'today': dt.utcnow()}
