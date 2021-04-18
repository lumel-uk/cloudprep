# TODO:
#  * Ensure that elements can't be processed multiple times.

class AwsEnvironment:
    def __init__(self):
        self.description = "AWS Environment generated by CloudPrep"
        self.resources = {}
        self.parameters = {}
        self.outputs = {}
        self.mappings = {}

        self._todo = []

    def find_by_physical_id(self, needle):
        if needle in self.resources:
            return self.resources[needle]
        return None

    def logicalFromPhysical(self, needle):
        return self.find_by_physical_id(needle).get_logical_id()

    def addToTodo(self, element):
        self._todo.append(element)

    def get_next_todo(self):
        if len(self._todo) > 0:
            candidate=self._todo[0]
            # Have we already done so? If so remove and revisit
            if self.find_by_physical_id(candidate.get_physical_id()) is not None:
                self.remove_from_todo(candidate)
                return self.get_next_todo()

            return candidate
        else:
            return None

    def remove_from_todo(self, task):
        self._todo.remove(task)

    def add_resource(self, resource):
        self.resources[resource.get_physical_id()] = resource

    def add_intermediate_resource(self, resource):
        self.resources.append(resource)
