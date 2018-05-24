# -*- coding: utf-8 -*-

"""This module powers the DstSubjects class that is the workhorse to
obtain subjects and subjects from Statistics Denmark.
"""
from pandas import DataFrame, to_datetime
from pydst.utils import check_lang, bad_request_wrapper, desc_to_df
import requests


class Dst(object):
    """Retrieve subjects, metadata and data from Statistics Denmark.

    This class provides some simple functions to retrieve information
    from Statistics Denmark's API.

    Attributes:
        lang (str): Can take the values ``en`` for English or ``da``
            for Danish
    """

    def __init__(self, lang='en'):
        self.lang = check_lang(lang)

    def get_subjects(self, subjects=None, lang=None):
        """Retrieve subjects and subjects from Statistics Denmark

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
        if not lang:
            lang = self.lang
        else:
            lang = check_lang(lang)

        base_url = "https://api.statbank.dk/v1/subjects/"

        if not subjects:
            sub_url = base_url + "?lang={}&format=JSON".format(lang)
        elif isinstance(subjects, str):
            sub_url = base_url + "{}?lang={}&format=JSON".format(subjects, lang)
        elif isinstance(subjects, list):
            str_subjects = ','.join(subjects)
            sub_url = base_url + "{}?lang={}&format=JSON".format(str_subjects, lang)
        else:
            raise ValueError('Subjects must be a list or a string of subject ids')

        r = requests.get(sub_url)
        bad_request_wrapper(r)

        return desc_to_df(r.json())

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
                  active firstPeriod        id latestPeriod                                              text      unit
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

        if not lang:
            lang = self.lang
        else:
            lang = check_lang(lang)

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
        bad_request_wrapper(r)

        res = DataFrame(r.json())
        res['updated'] = to_datetime(res['updated'])
        return res
