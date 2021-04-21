import hashlib
import sys
from typing import final

from ..AwsEnvironment import AwsEnvironment


class AwsElement:
    def __init__(self, aws_type, environment: AwsEnvironment, physical_id, source_json=None):
        self._environment = environment

        self._element = {}
        self._dependencies = []
        self._awsType = aws_type
        self._logical_id = self.calculate_logical_id(physical_id)
        self._defaults = {}
        self._tags = None
        self._valid = False
        self._physical_id = physical_id
        self._source_json = source_json

    def get_logical_id(self):
        return self._logical_id

    def get_physical_id(self):
        return self._physical_id

    def get_type(self):
        return self._awsType

    def get_properties(self):
        return self._element

    def set_source_json(self, json):
        self._source_json = json

    def make_valid(self, validity=True):
        self._valid = validity

    def get_dependencies(self):
        return self._dependencies

    def add_dependency(self, new_dependency):
        if new_dependency not in self._dependencies:
            self._dependencies.append(new_dependency)

    def is_valid(self):
        return self._valid

    def get_tags(self):
        if self._tags:
            return self._tags.get_tags()
        else:
            return None

    def set_defaults(self, defaults):
        self._defaults = defaults

    def is_default(self, key, value=None):
        if key not in self._defaults:
            return False
        if value is None:
            value = self._element[key]
        return value == self._defaults[key]

    def copy_if_exists(self, key, source_json):
        """ If a key exists, copy it directly"""
        if key in source_json:
            self._element[key] = source_json[key]

    def refer_if_exists(self, key, source_json):
        """" If a key exists, turn it into a reference and copy it here """
        if key in source_json:
            self._element[key] = self.make_reference(physical_id=source_json[key])

    def array_refer_if_exists(self, key, source_json):
        """ If a key exists, and is an array, iterate through it and make references. """
        if key in source_json and isinstance(source_json[key], list):
            self._element[key] = []
            for entry in source_json[key]:
                self._element[key].append(self.make_reference(physical_id=entry))

    def make_reference(self, logical_id=None, physical_id=None):
        """ Construct a reference for either this object or from a logical or physical id."""
        if logical_id is None:
            if physical_id is None:
                logical_id = self.get_logical_id()
            else:
                logical_id = self.calculate_logical_id(physical_id)

        return {"Ref": logical_id}

    def make_getatt(self, attribute):
        return {"Fn::GetAtt": [self.get_logical_id(), attribute]}

    @final
    def capture(self):
        print("Capturing %s %s as %s" % (self._awsType, self._physical_id, self._logical_id), file=sys.stderr)
        return self.local_capture()

    def local_capture(self):
        raise NotImplementedError("capture is not implemented in this class.")

    @final
    def finalise(self):
        print("Finalising %s %s" % (self._awsType, self._physical_id), file=sys.stderr)
        return self.local_finalise()

    def local_finalise(self):
        return False

    @staticmethod
    def calculate_logical_id(physical_id):
        return physical_id.replace("-","")
        # md5 = hashlib.md5()
        # md5.update(physical_id.encode("utf-8"))
        # new_pid = md5.hexdigest()[0:16].upper()
        # return aws_type[aws_type.rfind(":") + 1:].lower() + str(new_pid)
