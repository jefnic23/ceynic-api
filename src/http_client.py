import aiohttp


class HttpClient:
    async def delete_async(url: str, headers: dict[str, any] | None = None) -> dict[str, any]:
        async with aiohttp.ClientSession() as session, session.delete(url=url, headers=headers) as res:
            if not res.ok:
                await res.raise_for_status()
            return await res.json()

    async def get_async(
        url: str, headers: dict[str, any] | None = None, params: dict[str, any] | None = None
    ) -> dict[str, any]:
        async with aiohttp.ClientSession() as session, session.get(url=url, headers=headers, params=params) as res:
            if not res.ok:
                await res.raise_for_status()
            return await res.json()

    async def post_async(url: str, data: dict[str, any], headers: dict[str, any] | None = None) -> dict[str, any]:
        async with (
            aiohttp.ClientSession() as session,
            session.post(url=url, data=data, headers=headers) as res,
        ):
            if not res.ok:
                await res.raise_for_status()
            return await res.json()

    async def put_async(url: str, data: dict[str, any], headers: dict[str, any] | None = None) -> dict[str, any]:
        async with (
            aiohttp.ClientSession() as session,
            session.put(url=url, data=data, headers=headers) as res,
        ):
            if not res.ok:
                await res.raise_for_status()
            return await res.json()


def get_http_client():
    return HttpClient
