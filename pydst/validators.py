import cerberus

def lang_validator(lang, valid_langs):
    v = cerberus.Validator()
    schema = {
        'lang': {'type': 'string'},
        'valid_langs': {
            'type': 'list',
            'schema': {'type': 'string'}
            }
        }
    validation_object = {
        'lang': lang,
        'valid_langs': valid_langs
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
    if str in list:
        return True
    else:
        return False

def dict_keys_to_comma_str(dict):
    return ', '.join([str(i) for i in dict.keys()])
