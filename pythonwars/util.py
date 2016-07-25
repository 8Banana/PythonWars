#!/usr/bin/env python3
import inflection


class _AttributesFromJson(object):
    attr_keys = [

    ]

    def __init__(self, json_data):
        for key in self.attr_keys:
            *tree, leaf = key.split("/")
            look_in = json_data
            for inner_key in tree:
                look_in = look_in[inner_key]
            setattr(self, inflection.underscore(leaf), look_in[leaf])
