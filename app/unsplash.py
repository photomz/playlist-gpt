import asyncio, os
from typing import List
import logging
from arequests import fetch_all

def batch_search_unsplash(
    queries: List[str], counts: List[int], page=1, size="small", return_raw=False
):
    """Batch fetch images from Unsplash based on a query with asyncio.

    Args:
        queries (List[str]): Search queries.
        counts (List[int]): Number of items per query.
        page (int, optional): Page number to retrieve. Defaults to 1.
        size (str, optional): Size of the image. Defaults to "regular".

    Returns:
        List[str]: List of image URLs.
    """
    UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
    
    params = [
        {
            "query": query,
            "content_filter": "high",
            "client_id": UNSPLASH_ACCESS_KEY,
            "per_page": str(count),
            "page": str(page),
        }
        for query, count in zip(queries, counts)
    ]
    base_urls = ["https://api.unsplash.com/search/photos"] * len(queries)

    batch_responses = asyncio.run(fetch_all(base_urls, params=params))

    try:
        urls = []
        for data, query in zip(batch_responses, queries):
            try:
                if return_raw:
                    urls.append(data)
                else:
                    urls.append([r["urls"][size] for r in data["results"]])
            except KeyError:
                logging.error(
                    f"Can't find images for query={query} the returned data=", data)
                urls.append([query])  # Silent fallback
        return urls
    except Exception as e:
        logging.error(f"Error in Unsplash: {e}")
        # Silent fallback: append original query
        # Behaviour on web client: broken images, but design layout preserved
        return queries

# Test "fish" query
if __name__ == "__main__":
    import dotenv, os, time
    dotenv.load_dotenv()

    queries = ["fish", "beaver"]
    counts = [1] * 2

    start = time.time()
    urls = batch_search_unsplash(queries, counts)
    print(f"Time taken: {time.time() - start:.2f} seconds")
    print(urls)