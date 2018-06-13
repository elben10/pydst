import cerberus

def lang_validator(lang, valid_langs):
    """Validates if language is correctly specified.

    This function validates that lang is contained in valid_langs,
    and that lang and valid_langs takes the correct types.

    Args:
        lang (str): Language that is contained in valid_langs.
            Language must be letters.

        valid_langs(list of str): A list of valid languages. Each
            element must be letters.

    Returns:
        None
    """
    v = cerberus.Validator()
    schema = {
        'lang': {
            'type': 'string',
            'regex': r'[a-zA-Z]+',
        },
        'valid_langs': {
            'type': 'list',
            'schema': {
                'type': 'string',
                'regex': r'[a-zA-Z]+',
            }
            }
        }
    validation_object = {
        'lang': lang,
        'valid_langs': valid_langs,
        }

    v.validate(validation_object, schema)

    if any(v.errors):
        raise ValueError(
            'The following arguments is not provided correctly: {}. '\
            'See the docs.'.format(dict_keys_to_comma_str(v.errors))
            )

    if not str_in_list(lang, valid_langs):
        raise ValueError('{} is not in {}'.format(lang, valid_langs))


def str_in_list(str, list):
    """Check if a string is contained in a list

    Args:
        str (str): Arbitrary string

        list (list of str): Arbitrary list of strings

    Returns:
        bool: Returns True (False) if (not) str contained in list 
    """
    if str in list:
        return True
    else:
        return False

def dict_keys_to_comma_str(dict):
    """ Comma seperates dict keys into string

    Args:
        dict (dict): A dictionary.

    Returns:
        str: Comma seperated string of keys.
    """
    return ', '.join([str(i) for i in dict.keys()])
