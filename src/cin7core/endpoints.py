from .api import ApiEndpoint, ListMixin, GetMixin, CreateMixin, UpdateMixin, DeleteMixin


class Sale(ListMixin, GetMixin, CreateMixin, UpdateMixin, DeleteMixin, ApiEndpoint):
    def __init__(self, client):
        super().__init__(client=client, resource="sale")

        self._list = self.SaleList(client=client)
        self.order = self.SaleOrder(client=client)

    class SaleList(ListMixin, ApiEndpoint):
        def __init__(self, client):
            super().__init__(client=client, resource="saleList")

    class SaleOrder(GetMixin, CreateMixin, ApiEndpoint):
        def __init__(self, client):
            super().__init__(client=client, resource="sale/order")

        def get(self, pk, **kwargs):
            return super().get(pk, SaleId=pk, **kwargs)

    def all(self, **kwargs):
        return self._list.all(**kwargs)

    def filter(self, **kwargs):
        return self._list.filter(**kwargs)


class Webhook(ListMixin, CreateMixin, UpdateMixin, DeleteMixin, ApiEndpoint):
    def __init__(self, client):
        super().__init__(client=client, resource="webhooks")

    def get(self, pk):
        page = 1
        while True:
            webhooks = self.all(page=page)
            for webhook in webhooks:
                if webhook["ID"] == pk:
                    return webhook

            if webhooks.has_more:
                page += 1
            else:
                break
