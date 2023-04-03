from ansible.errors import AnsibleFilterError

import gi.repository.GLib as glib


def replace_array_str(input_str, value, key=None):
    try:
        input_variant = glib.variant_parse(glib.VariantType('as'), input_str)
    except:
        raise AnsibleFilterError("Expected VariantType('as') for: %s" %
                                 input_str)

    def replace(in_variant):
        for s in in_variant.unpack():
            k, v = s.split(':')
            if key is None or key == k:
                v = value
            yield f'{k}:{v}'

    output = [_ for _ in replace(input_variant)]
    output = glib.Variant(input_variant.get_type_string(), output)
    return output


class FilterModule(object):
    def filters(self):
        return {
            'cinnamon_array_str_value': replace_array_str
        }
