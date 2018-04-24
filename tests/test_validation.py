import os
import sys
import pytest

from src.validation import AddressValidation


@pytest.mark.parametrize("user_input,fields,result", [
    ({"address": "demo"}, ["address"], ({}, {"address": "demo"}))
])

def test_address_validation(user_input, fields, result):
    assert AddressValidation.is_valid(user_input, fields) == result

def test_check_transaction():

    assert ""
