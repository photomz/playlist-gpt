from typing import List, Dict, Any, Optional
import asyncio
import aiohttp
import logging
from aiohttp.client_exceptions import ClientResponseError


async def fetch(
    session: aiohttp.ClientSession,
    url: str,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, str]] = None,
    max_retries: Optional[int] = 5,
) -> Optional[str]:
    """
    Fetch a URL using aiohttp, handling errors and retries.
    """
    retry = 0
    while retry < max_retries: # type: ignore
        try:
            async with session.get(url, headers=headers, params=params) as response:
                # log_request(response.request_info)
                if response.status == 429:  # HTTP status code for Too Many Requests
                    retry += 1
                    await asyncio.sleep(retry * 2)  # exponential backoff
                    continue
                response.raise_for_status()  # raises error for non-200 status codes
                return await response.json()
        except ClientResponseError as e:
            logging.error(
                f"Async Fetch Error \n Url: {url} \n Headers: {headers} \n Params: {params}"
            )
            raise e
    return None


async def fetch_all(
    urls: List[str],
    headers: List[Dict[str, str]] = [],
    params: List[Dict[str, str]] = [],
    max_retries: int = 5,
    batch_size: int = 10,
) -> List[Any]:
    """
    Fetch all URLs in parallel using asyncio and aiohttp, handling errors and retries.
    """
    try:
        async with aiohttp.ClientSession() as session:
            # For zip() to work, all lists must be of the same length
            headers = [{}] * len(urls) if not len(headers) else headers
            params = [{}] * len(urls) if not len(params) else params

            request_kwargs = [
                {
                    "url": url,
                    "headers": header,
                    "params": param,
                    "max_retries": max_retries,
                }
                for (url, header, param) in zip(urls, headers, params)
            ]

            # Fetch Unsplash URLs in smaller batches to respect rate limits
            results = []
            for i in range(0, len(urls), batch_size):  # Adjust batch size as needed
                batch = request_kwargs[i: i + batch_size]
                results.extend(
                    await asyncio.gather(
                        *(fetch(session, **kwargs) for kwargs in batch)
                    )
                )

            return results
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return []
