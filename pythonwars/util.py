#!/usr/bin/env python3
import sys

import inflection

__all__ = ["AttributesFromJson"]


class AttributesFromJson:
    attr_keys = []

    def __init__(self, json_data):
        for key in self.attr_keys:
            tree = key.split("/")
            leaf = tree.pop()
            look_in = json_data
            if ":" in leaf:
                leaf, class_name = leaf.split(":")
            else:
                class_name = None
            for inner_key in tree:
                look_in = look_in[inner_key]
            result = look_in[leaf]
            if class_name is not None:
                *module_name, class_name = class_name.split(".")
                module_name = ".".join(module_name)
                result = sys.modules[module_name].__dict__[class_name](result)
            setattr(self, inflection.underscore(leaf), result)
