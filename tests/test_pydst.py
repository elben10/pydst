#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pydst` package."""

import pytest

from pandas import DataFrame
from pydst import pydst
import pydst.utils as utils

# Check that utils.check_lang raises a value error if not 'da' or 'en'
def test_nonexistence_lang_error():
    with pytest.raises(ValueError):
        utils.check_lang('es')

# Check that 'da' is returned if provided as lang arg in utils.check_lang
def test_existence_lang_return():
    assert 'da' == utils.check_lang('da')

# Check that Dst class raises an valueerror if 'es' is provided
# because it is not an availble langauge at the moment.
def test_nonexistence_lang_error_dst():
    with pytest.raises(ValueError):
        pydst.Dst(lang='es')

# Check that Dst class has an attribute lang='da' if initialized with 'da'
def test_existence_lang_attribute():
    assert 'da' == pydst.Dst('da').lang

# Check that Dst class has an attribute lang='en' if initialized with
# no lang argument provided
def test_existence_lang_attribute_default():
    assert 'en' == pydst.Dst().lang

# Check that Dst.get_subjects() returns a pandas.DataFrame
def test_subjects_returns_df():
    assert isinstance(pydst.Dst().get_subjects(), DataFrame)

# Check that the first subject has an subsubject
def test_subject_has_subsubjects():
    id =  pydst.Dst().get_subjects()['id'][0]
    assert isinstance(pydst.Dst().get_subjects(subjects=id), DataFrame)

# Check that get_subjects returns df when str is provided as subjects arg
def test_str_subject():
    assert isinstance(pydst.Dst().get_subjects(subjects='02'), DataFrame)

# Check that get_subjects returns df when list is provided as subjects arg
# Only one element is provided
def test_list_single_element_subject():
    assert isinstance(pydst.Dst().get_subjects(subjects=['02']), DataFrame)

# Check that get_subjects returns df when list is provided as subjects arg
# Multiple elements is provided
def test_list_multiple_elements_subject():
    assert isinstance(pydst.Dst().get_subjects(subjects=['02', '05']), DataFrame)

# Check that if get_subjects get int as subjects arg it raises an ValueError
def test_int_subject():
        with pytest.raises(ValueError):
            pydst.Dst().get_subjects(subjects=2)

# Check that error is raised if lang == fi
def test_lang_error_subject():
        with pytest.raises(ValueError):
            pydst.Dst().get_subjects(lang='fi')


# Check that get_tables returns df when str is provided as subjects arg
def test_str_tables():
    assert isinstance(pydst.Dst().get_tables(subjects='02'), DataFrame)

# Check that get_tables returns df when list is provided as subjects arg
# Only one element is provided
def test_list_single_element_tables():
    assert isinstance(pydst.Dst().get_tables(subjects=['02']), DataFrame)

# Check that get_tables returns df when list is provided as subjects arg
# Multiple elements is provided
def test_list_multiple_elements_tables():
    assert isinstance(pydst.Dst().get_tables(subjects=['02', '05']), DataFrame)

# Check that if get_tables get int as subjects arg it raises an ValueError
def test_int_tables():
        with pytest.raises(ValueError):
            pydst.Dst().get_tables(subjects=2)

# Check that ValueError is raised when dst_tables arg include_inactive is int
def test_int_include_inactive_get_tables():
            with pytest.raises(ValueError):
                pydst.Dst().get_tables(inactive_tables=2)

# Check that error is raised if lang == fi
def test_lang_error_tables():
        with pytest.raises(ValueError):
            pydst.Dst().get_tables(lang='fi')

def check_no_inactive_tables_if_false():
    assert pydst.Dst().get_tables().active.all()

def check_inactive_tables_if_true():
    assert pydst.Dst().get_tables(inactive_tables=True).active.all() == False
