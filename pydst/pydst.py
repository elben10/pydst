# -*- coding: utf-8 -*-

"""This module powers the DstSubjects class that is the workhorse to
obtain subjects and subjects from Statistics Denmark.
"""
from pandas import DataFrame, to_datetime, read_csv
from pydst import utils
from pydst import validators
import requests
from collections import OrderedDict
from io import StringIO
import os

class Dst(object):
    """Retrieve subjects, metadata and data from Statistics Denmark.

    This class provides some simple functions to retrieve information
    from Statistics Denmark's API.

    Attributes:
        lang (str): Can take the values ``en`` for English or ``da``
            for Danish
    """

    def __init__(self, lang='en'):
        self.lang = utils.check_lang(lang)
        self.base_url = 'https://api.statbank.dk'
        self.version = 'v1'

    def get_subjects(self, subjects=None, lang=None):
        """Retrieve subjects and sub subjects from Statistics Denmark.

        This function allows to retrieve the subjects and subsubjects
        Statistics Denmark uses to categorize their tables. These subjectsID
        can be used to only retrieve the tables that is classified with
        the respective SubjectsID using ``get_tables``.

        Args:
            subjects (str/list, optional): If a valid subjectsID is provided
                it will return the subject's subsubjects if available. subjects
                can either be a list of subjectsIDs in string format or a comma
                seperated string

            lang (str, optional): If lang is provided it uses this argument
                instead of the Dst's class attribute lang. Can take the values
                ``en`` for English or ``da`` for Danish

        Returns:
            pandas.DataFrame: Returns a DataFrame with subjects.

        Examples:
            The example beneath shows how ``get_subjects`` is used.

            >>> from pydst import Dst
            >>> Dst().get_subjects()
                active                               desc  hasSubjects  id
            0     True           Population and elections         True  02
            1     True                  Living conditions         True  05
            2     True            Education and knowledge         True  03
            ..     ...                                ...          ...  ..
            10    True                   Business sectors         True  11
            11    True  Geography, environment and energy         True  01
            12    True                              Other         True  19

            [13 rows x 4 columns]

        """
        lang = utils.assign_lang(self, lang)
        if not isinstance(subjects, (str, list, type(None))):
            raise ValueError('Subjects must be a list or a string of subject ids')

        if isinstance(subjects, (str, list)):
            validators.subject_validator(subjects)

        query_dict = {
            'lang': lang,
            'format': 'JSON'
            }

        url = utils.construct_url(self.base_url, 
                                  self.version,
                                  'subjects',
                                  '',
                                  query_dict)

        r = requests.get(url)
        utils.bad_request_wrapper(r)

        return utils.desc_to_df(r.json())

    def get_tables(self, subjects=None, inactive_tables=False, lang=None):
        """
        Args:
            inactive_tables (bool, optional): If True the DataFrame will
                contain tables that are no longer updated.

            subjects (str/list, optional): If a valid subjectsID is provided
                it will return the subject's subsubjects if available. subjects
                can either be a list of subjectsIDs in string format or a comma
                seperated string

            lang (str, optional): If lang is provided it uses this argument
                instead of the Dst's class attribute lang. Can take the values
                ``en`` for English or ``da`` for Danish

        Returns:
            pandas.DataFrame: Returns a DataFrame with subjects.

        Examples:
            The example beneath shows how ``get_tables`` is used.

            >>> from pydst import Dst
            >>> Dst().get_tables()
                  active firstPeriod        id latestPeriod
            0       True      2008Q1    FOLK1A       2018Q2
            1       True      2008Q1    FOLK1B       2018Q2
            2       True      2008Q1    FOLK1C       2018Q2
            ...      ...         ...       ...          ...
            1958    True        2005  SKOVRG01         2016
            1959    True        2005  SKOVRG02         2016
            1960    True        2005  SKOVRG03         2016
                                                        text      unit
            0     Population at the first day of the quarter    number
            1     Population at the first day of the quarter    number
            2     Population at the first day of the quarter    number
            ...                                          ...       ...
            1958            Growing stock (physical account)  1,000 m3
            1959            Growing stock (monetary account)  DKK mio.
            1960      Forest area (Kyoto) (physical account)       km2
                             updated                                          variables
            0    2018-05-08 08:00:00           [region, sex, age, marital status, time]
            1    2018-05-08 08:00:00              [region, sex, age, citizenship, time]
            2    2018-05-08 08:00:00  [region, sex, age, ancestry, country of origin...
            ...                  ...                                                ...
            1958 2017-11-28 08:00:00  [balance items, species of wood, county counci...
            1959 2017-11-28 08:00:00  [balance items, species of wood, county counci...
            1960 2017-11-28 08:00:00     [balance items, county council district, time]

            [1961 rows x 8 columns]

        """
        lang = utils.assign_lang(self, lang)

        base_url = "http://api.statbank.dk/v1/tables"

        if not subjects:
            tab_url = base_url + "?lang={}".format(lang)
        elif isinstance(subjects, str):
            tab_url = base_url + "?lang={}&subjects={}".format(lang, subjects)
        elif isinstance(subjects, list):
            sub_str = ",".join(subjects)
            tab_url = base_url + "?lang={}&subjects={}".format(lang, sub_str)
        else:
            raise ValueError('Subjects must be a list or a string of subject ids')

        if inactive_tables == True:
            tab_url += "&includeInactive=true"
        elif not isinstance(inactive_tables, bool):
            raise ValueError("include_inactive must be bool")

        r = requests.get(tab_url)
        utils.bad_request_wrapper(r)

        res = DataFrame(r.json())
        res['updated'] = to_datetime(res['updated'])
        return res

    def get_variables(self, table_id, lang=None):
        """ DataFrame with variables contained in `table_id`

        Args:
            table_id (str): Table ID for the the table you want to retrieve data
            from.

            lang (str, optional): If lang is provided it uses this argument
                instead of the Dst's class attribute lang. Can take the values
                ``en`` for English or ``da`` for Danish

        Returns:
            pandas.DataFrame: Returns a DataFrame with subjects.

        Todo:
            * Implement tests
        """
        lang = utils.assign_lang(self, lang)

        base_url = "http://api.statbank.dk/v1/tableinfo/{}?lang={}"\
        .format(table_id, lang)

        r = requests.get(base_url)
        utils.bad_request_wrapper(r)
        return DataFrame(r.json()['variables'])

    def get_metadata(self, table_id, lang=None):
        """ DataFrame with metadata about `table_id`

        Args:
            table_id (str): Table ID for the the table you want to retrieve data
            from.

            lang (str, optional): If lang is provided it uses this argument
                instead of the Dst's class attribute lang. Can take the values
                ``en`` for English or ``da`` for Danish

        Returns:
            dict: Returns a dictionary containing metadata about the
                specified data.

        Todo:
            * Implement tests
        """
        lang = utils.assign_lang(self, lang)

        base_url = "http://api.statbank.dk/v1/tableinfo/{}?lang={}"\
        .format(table_id, lang)

        r = requests.get(base_url)
        utils.bad_request_wrapper(r)
        json = r.json()
        json.pop('variables', None)
        return json

    def get_data(self, table_id, variables=None, lang=None):
        """ DataFrame with variables contained in `table_id`

        Args:
            table_id (str): Table ID for the the table you want to retrieve data
                from.

            lang (str, optional): If lang is provided it uses this argument
                instead of the Dst's class attribute lang. Can take the values
                ``en`` for English or ``da`` for Danish

            variables(dict, optional):

        Returns:
            pandas.DataFrame: Returns a DataFrame with data from table_id.

        Todo:
            *
                Implement tests
            *
                Ensure that variables (dict) can only take lists as inputs
                that is entirely filled with strings
            *
                Ensure that variables (dict) can take string as values
        """
        lang = utils.assign_lang(self, lang)

        vars = self.get_variables(table_id, lang).iterrows()

        if isinstance(variables, type(None)):
            args = {row[1]['id']:[row[1]['values'][0]['id']] for row in vars}
        elif isinstance(variables, dict):
            args = {row[1]['id']:[row[1]['values'][0]['id']] for row \
                    in vars if row[1]['id'] not in variables.keys()}
            args = {**variables, **args}
        else:
            raise ValueError("Variables must be either type None or Dict")

        base_url = 'http://api.statbank.dk/v1/data/{}/' \
                    'BULK?lang={}&delimiter=Semicolon&{}'
        arg_str = '&'.join([key + '=' + ','.join(value) \
                            for key, value in args.items()])
        url = base_url.format(table_id, lang, arg_str)
        r = requests.get(url)
        utils.bad_request_wrapper(r)
        return read_csv(StringIO(r.content.decode('utf-8')), sep=';')

    def get_csv(self, path, table_id, variables=None, lang=None):
        """ Save `table_id` as csv

        Args:
            path (str): Outputdirectory

            table_id (str): Table ID for the the table you want to retrieve data
                from.

            lang (str, optional): If lang is provided it uses this argument
                instead of the Dst's class attribute lang. Can take the values
                ``en`` for English or ``da`` for Danish

            variables(dict, optional):

        Returns:
            None: Doesn't return anything.

        Todo:
            *
                Implement tests
            *
                Ensure that variables (dict) can only take lists as inputs
                that is entirely filled with strings
            *
                Ensure that variables (dict) can take string as values
        """
        lang = utils.assign_lang(self, lang)

        if not os.path.exists(os.path.dirname(\
        os.path.abspath(os.path.expanduser(path)))):
            raise OSError('Directory does not exist')

        vars = self.get_variables(table_id, lang).iterrows()

        if isinstance(variables, type(None)):
            args = {row[1]['id']:[row[1]['values'][0]['id']] for row in vars}
        elif isinstance(variables, dict):
            args = {row[1]['id']:[row[1]['values'][0]['id']] for row \
                    in vars if row[1]['id'] not in variables.keys()}
            args = {**variables, **args}
        else:
            raise ValueError("Variables must be either type None or Dict")

        base_url = 'http://api.statbank.dk/v1/data/{}/' \
                    'BULK?lang={}&delimiter=Semicolon&{}'
        arg_str = '&'.join([key + '=' + ','.join(value) \
                            for key, value in args.items()])
        url = base_url.format(table_id, lang, arg_str)
        r = requests.get(url, stream=True)
        utils.bad_request_wrapper(r)
        with open(os.path.abspath(os.path.expanduser(path)), 'wb') as f:
            for line in r.iter_lines():
                f.write(line)
                f.write('\n'.encode())
