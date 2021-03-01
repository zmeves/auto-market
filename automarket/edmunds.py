"""
Get car values from Edmunds.com

URL pattern: https://www.edmunds.com/MAKE/MODEL/YYYY/appraisal-value/
"""

import requests
import bs4
import logging
import pandas as pd

# URL query base for getting data for cars
_base_url = "https://www.edmunds.com/{make}/{model}/{year}/appraisal-value/"

# Headers to send with GET request
_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/56.0.2924.76 Safari/537.36',
            "Upgrade-Insecure-Requests": "1",
            "DNT": "1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate"}


def get_values(make, model, year, timeout=10):
    """
    Get market values for a make, model, and year.

    Parameters
    ----------
    make : str
        Auto maker
    model : str
        Model of car
    year : str or int
        Year in 4-number format.
    timeout : float or int, optional
        Timeout (in seconds) for GET request. Defaults to 10 seconds.

    Returns
    -------

    Raises
    ------
    ValueError
        If unable to retrieve information.
    """

    year = str(year)
    if len(year) != 4:
        raise TypeError(f"Year must be given in YYYY format")

    logging.info(f"Make={make}, Model={model}, Year={year}")

    url = _base_url.format(make=make, model=model, year=year)
    logging.info(f"URL={url}")

    response = requests.request("GET", url, headers=_headers, timeout=timeout)
    logging.info(f"Response code={response.status_code}")

    if response.status_code != 200:
        raise ValueError(f"Unable to retrieve information: HTTP code {response.status_code}")

    soup = bs4.BeautifulSoup(response.content.decode())
    tables = list(soup.find_all(class_="estimated-values-table"))

    trim_values = {}

    # Iterate over tables on page
    for table in tables:
        # Get trim for this table
        identifier = ''.join(table.caption.contents)

        # Get column names for this table
        columns = [x.text for x in table.thead.contents[0].contents]

        tbody = table.tbody  # Table body content

        # Iterate over rows of table
        data = []
        for row in tbody.contents:
            data.append([x.text for x in row.contents])

        # Table format (as of 2/28/2021), field names NOT hard-coded:

        # Condition    Trade-in   Private Party   Dealer Retail
        # Outstanding    $              $              $
        # Clean          $              $              $
        # Average        $              $              $
        # Rough          $              $              $

        # Create a DataFrame
        data = pd.DataFrame(data, columns=columns).set_index(columns[0])
        # Store values for this trim level
        trim_values[identifier] = data

    return trim_values




