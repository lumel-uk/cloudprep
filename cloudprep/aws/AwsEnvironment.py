class AwsEnvironment:
    def __init__(self):
        self.description = "AWS Environment generated by CloudPrep"
        self.resources = {}
        self.parameters = {}
        self.outputs = {}
        self.mappings = {}

        self._todo = []
        self._warnings = []

    def find_by_physical_id(self, needle):
        # First, look through the existing resources; then scan those still to do.
        if needle in self.resources:
            return self.resources[needle]
        #
        # for task in self._todo:
        #     if task.get_physical_id() == needle:
        #         return task

        return None

    def find_by_logical_id(self, needle):
        for physical_id, candidate in self.resources.items():
            if candidate.logical_id == needle:
                return candidate
        return None

    def logical_from_physical(self, needle):
        return self.find_by_physical_id(needle).logical_id

    def add_to_todo(self, element):
        self._todo.append(element)

    def get_next_todo(self):
        if len(self._todo) > 0:
            candidate = self._todo[0]
            # Have we already done so? If so remove and revisit
            if self.find_by_physical_id(candidate.physical_id) is not None:
                self.remove_from_todo(candidate)
                return self.get_next_todo()

            return candidate
        else:
            return None

    def remove_from_todo(self, task):
        self._todo.remove(task)

    def add_resource(self, resource):
        self.resources[resource.physical_id] = resource

    def add_intermediate_resource(self, resource):
        self.resources[resource.physical_id] = resource

    def add_parameter(self, **kwargs):
        """ Parameters:
         * Name: The parameter name (mandatory)
         * Description: The parameter description (mandatory)
         * Type: Parameter type (optional, default: "String")
         * Default: The default value (optional)
         * AllowedValues: A set of optional values to constrain input (optional)
         """
        name = kwargs["Name"]
        del kwargs["Name"]

        if "Type" not in kwargs:
            kwargs["Type"] = "String"

        self.parameters[name] = kwargs

    def add_warning(self, message, resource_physical_id):
        self._warnings.append("Warning: {0} on {1}".format(message, resource_physical_id))