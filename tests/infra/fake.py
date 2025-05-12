import httpx


class FakeResponse:
    def __init__(self, json_data, status_code=200):
        self._json = json_data
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise httpx.HTTPStatusError(
                "Error", request=None, response=self  # minimal stub
            )

    def json(self):
        return self._json


class FakeHttpClient:
    """
    Maps request URL → JSON payload.
    """
    def __init__(self, url_map):
        self.url_map = url_map

    async def get(self, url: str):
        if url not in self.url_map:
            return FakeResponse({"detail": "not found"}, status_code=404)
        return FakeResponse(self.url_map[url], status_code=200)
