from . import errors


class ApiEndpoint(object):
    def __init__(self, client, resource):
        self.client = client
        self.resource = resource

    def _request(self, method, data=None, params=None):
        return self.client._request(method, self.resource, data, params)

    def all(self, page=1, limit=100):
        raise errors.InvalidMethodError(
            message=f"API resource {self.resource} does not support listing"
        )

    def filter(self, **kwargs):
        raise errors.InvalidMethodError(
            message=f"API resource {self.resource} does not support filtering"
        )

    def get(self, pk, **kwargs):
        raise errors.InvalidMethodError(
            message=f"API resource {self.resource} does not support getting"
        )

    def create(self, data=None):
        raise errors.InvalidMethodError(
            message=f"API resource {self.resource} does not support creating"
        )

    def update(self, data=None):
        raise errors.InvalidMethodError(
            message=f"API resource {self.resource} does not support updating"
        )

    def delete(self, pk):
        raise errors.InvalidMethodError(
            message=f"API resource {self.resource} does not support deleting"
        )


class ListMixin:
    class ApiList(list):
        # TODO: Implement auto-pagination
        page = 1
        total = 0
        has_more = False

        def __new__(self, *args, **kwargs):
            return super().__new__(self, args, kwargs)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.__dict__.update(kwargs)

        def __call__(self, **kwargs):
            self.__dict__.update(kwargs)
            return self

    def all(self, page=1, limit=100):
        return self.filter(page=page, limit=limit)

    def filter(self, **kwargs):
        response = self._request("GET", params=kwargs)
        if response.status_code == 200:
            raw = response.json()

            api_list = self.ApiList(raw[self.resource[0].upper() + self.resource[1:]])
            try:
                api_list.page = raw["Page"]
                api_list.total = raw["Total"]
                api_list.has_more = api_list.total > api_list.page * kwargs.get(
                    "limit", kwargs.get("Limit", 100)
                )
            except KeyError:
                api_list.total = len(api_list)

            return api_list
        raise errors.ListObjectsError(
            message=f"List {self.resource} failed", response=response
        )


class GetMixin:
    def get(self, pk, **kwargs):
        response = self._request("GET", params={"ID": pk} | kwargs)
        if response.status_code == 200:
            return response.json()
        raise errors.GetObjectError(
            message=f"Get {self.resource} failed", response=response
        )


class CreateMixin:
    def create(self, data):
        response = self._request("POST", data=data)
        if response.status_code in (200, 201):
            return response.json()
        raise errors.CreateObjectError(
            message=f"Create {self.resource} failed", response=response
        )


class UpdateMixin:
    def update(self, data):
        response = self._request("PUT", data=data)
        if response.status_code in (200, 201, 204):
            return response.json()
        raise errors.UpdateObjectError(
            message=f"Update {self.resource} failed", response=response
        )


class DeleteMixin:
    def delete(self, pk):
        response = self._request("DELETE", params={"ID": pk})
        if response.status_code in (200, 204):
            return True
        raise errors.DeleteObjectError(
            message=f"Delete {self.resource} failed", response=response
        )
