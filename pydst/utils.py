from pandas import DataFrame
from pydst import validators
import os

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
    validators.lang_validator(lang, ['da', 'en'])
    return lang

def assign_lang(self, lang=None):
    if lang:
        return check_lang(lang)
    else:
        return check_lang(self.lang)

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

def construct_url(base, version, app, path, query):
    """
    Todo:
        * Test that url result expected url
    """
    url_without_query = ''.join([os.path.join(i, '') for i in \
                                [base, version, app, path]])
    query = flatten_list_to_string_in_dict_remove_none(query)
    query_str = '&'.join(['{}={}'.format(k, v) for k, v in query.items()])
    return url_without_query.replace("\\", "/").strip('/') + '?' + query_str

def flatten_list_to_string_in_dict_remove_none(dict):
    return {k: (v if isinstance(v, str) else ','.join(v)) for k,v \
                in dict.items() if v is not None}
