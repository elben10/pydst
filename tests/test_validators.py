#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pydst` package."""

import pytest

from pydst import validators
from pydst import utils

def test_ValueError_if_lang_wrong_type():
    with pytest.raises(ValueError):
        validators.lang_validator(2, ['da', 'en'])

def test_ValueError_if_valid_langs_wrong_type():
    with pytest.raises(ValueError):
        validators.lang_validator('da', 'da')

def test_ValueError_if_lang_not_in_valid_langs():
    with pytest.raises(ValueError):
        validators.lang_validator('da', ['en'])

def test_returns_None_if_correctly_specified():
    assert validators.lang_validator('da', ['da', 'en']) == None

def test_False_if_str_not_in_list():
    assert validators.str_in_list('da', ['en']) == False

def test_True_if_str_in_list():
    assert validators.str_in_list('da', ['da']) == True
