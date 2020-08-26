from bs4 import BeautifulSoup
from decimal import Decimal


def convert(amount, cur_from, cur_to, date, requests):
    import re
    url = f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={date}'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'xml')

    def find_value(coin, soup):
        from_ = soup.find('CharCode', text=coin)
        nominal = Decimal(from_.find_next_sibling('Nominal').string)
        val = Decimal(re.sub(',', '.', from_.find_next_sibling('Value').string))
        return val / nominal

    if cur_from == cur_to:
        return amount

    if cur_from == 'RUR':
        from_ = 1
    else:
        from_ = find_value(cur_from, soup)

    rel = from_ * 1 / find_value(cur_to, soup)
    return (amount * rel).quantize(Decimal('1.0000'))