from pandas import DataFrame

def bad_request_wrapper(r):
    """Raises an error if http error

    A wrapper around httperror such that if there is an error message
    available from Statistics Denmark use this one because it is more
    descriptiveself.

    Args:
        r (requests.models.Response): Response from the requests library.
    """
    if not r.ok:
        if r.json().get('errorTypeCode', None) and \
           r.json().get('message', None):
           r.reason = r.json()['message']
           r.raise_for_status()
        else:
           r.raise_for_status()

def check_lang(lang):
    """Returns lang if lang is an available languages

    Args:
        lang (str): Can take the values ``en`` for English or ``da``
            for Danish
    """
    if lang not in ['da', 'en']:
        raise ValueError('lang is not specified correct. See the docs.')
    return lang

def desc_to_df(list_):
    """Flattens subject response from Statistics Denmark

    Args:
        list_ (list): Json response from the requests library.

    Returns:
        pandas.DataFrame: Returns a DataFrame of the flatten response.
    """
    def json_to_df_dict(list_):
        res = []
        for i in list_:
            if not i['subjects']:
                res.append({'id': i['id'], 'desc': i['description'], 'active': i['active'], 'hasSubjects': i['hasSubjects']})
            else:
                res.extend(json_to_df_dict(i['subjects']))
        return res
    return DataFrame(json_to_df_dict(list_))
