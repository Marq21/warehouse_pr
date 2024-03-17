from datetime import date, datetime, timedelta
from expiration_dates.models import ExpirationDateEntity


def validate_dates(expired_date_entity: ExpirationDateEntity) -> bool:
    if expired_date_entity.date_of_manufacture > expired_date_entity.date_of_expiration:
        expired_date_entity.date_of_manufacture = date.today()
        expired_date_entity.date_of_expiration = date.today() + timedelta(days=20)
        return True
    else:
        return False
