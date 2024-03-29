class TagSet:
    def __init__(self, tag_dictionary=None):
        if tag_dictionary:
            self._tags = tag_dictionary
        else:
            self._tags = {}

    @property
    def tags(self):
        return self._tags

    def add_tag(self, key, value):
        if not key.startswith("aws:"):
            self._tags[key] = value

    def get_tag(self, tag):
        if tag in self._tags:
            return self._tags[tag]
        else:
            return None

    def from_api_result(self, api_result):
        if "Tags" in api_result:
            api_result = api_result["Tags"]
        elif "tags" in api_result:
            api_result = api_result["tags"]

        for tag in api_result:
            if "Key" in tag:
                self.add_tag(tag["Key"], tag["Value"])
            elif "key" in tag:
                self.add_tag(tag["key"], tag["value"])
            else:
                self.add_tag(tag, api_result[tag])
