#!/usr/bin/env python3
import inflection

__all__ = ["JsonDict"]


class JsonDict:
    def __init__(self, json_data):
        self._data = json_data

    def __getitem__(self, key):
        value = self._data[inflection.camelize(key, False)]
        # We only want to convert "real" dicts
        if value.__class__ is dict:
            value = self.__class__(value)
        return value

    def __setitem__(self, key, value):
        self._data[inflection.camelize(key, False)] = value

    def __getattr__(self, key):
        try:
            return self.__getitem__(key)
        except KeyError:
            # The lengths I go to for PEP8.
            clsname = self.__class__.__name__
            errmsg = "{!r} object has no attribute {!r}".format(clsname,
                                                                key)
            raise AttributeError(errmsg) from None

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self._data)
