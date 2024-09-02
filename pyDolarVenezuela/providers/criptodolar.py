from typing import Any, Dict, List
import json

from .. import network
from ..utils.time import get_formatted_date
from ..utils.common import _convert_specific_format, _convert_dollar_name_to_monitor_name
from ..utils.extras import list_monitors_images
from ._base import Base
from ..pages import CriptoDolar as CriptoDolarPage

class CriptoDolar(Base):
    PAGE = CriptoDolarPage

    @classmethod
    def _load(cls, **kwargs) -> List[Dict[str, Any]]:
        response = network.get(f'{cls.PAGE.provider}coins/latest', {'type': 'bolivar', 'base': kwargs.get('currency', 'usd')})
        json_response = json.loads(response)
        data = []

        for monitor in json_response:
            if monitor['type'] in ['bolivar', 'bancove']:
                image = next((image.image for image in list_monitors_images if image.provider == 'criptodolar' and image.title == _convert_specific_format(
                        _convert_dollar_name_to_monitor_name(monitor['name']))), None)
                key = _convert_specific_format(_convert_dollar_name_to_monitor_name(monitor['name']))
                title = _convert_dollar_name_to_monitor_name(monitor['name'])
                price = round(monitor['price'], 2)
                price_old   = monitor['priceOld']
                last_update = get_formatted_date(monitor['updatedAt'])

                data.append({
                    'key': key,
                    'title': title,
                    'price': price,
                    'price_old': price_old,
                    'last_update': last_update,
                    'image': image
                })

        return data