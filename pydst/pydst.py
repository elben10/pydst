# -*- coding: utf-8 -*-

"""This module powers the DstSubjects class that is the workhorse to
obtain subjects and subjects from Statistics Denmark.
"""

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
            https://api.statbank.dk/v1/subjects/?lang=en&format=JSON
                active                                       desc  hasSubjects  id
            0     True                   Population and elections         True  02
            1     True                          Living conditions         True  05
            2     True                    Education and knowledge         True  03
            3     True                Culture and National Church         True  18
            4     True                  Labour, income and wealth         True  04
            5     True                     Prices and consumption         True  06
            6     True  National accounts and government finances         True  14
            7     True                    Money and credit market         True  16
            8     True                           External economy         True  13
            9     True                 Business sector in general         True  07
            10    True                           Business sectors         True  11
            11    True          Geography, environment and energy         True  01
            12    True                                      Other         True  19

        """
        if not lang:
            lang = self.lang

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
