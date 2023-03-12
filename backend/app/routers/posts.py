from fastapi import APIRouter, Depends, HTTPException, Query
from elasticsearch import Elasticsearch

from app.config.es import es_auth, POSTS_INDEX_NAME
from app.models.posts import Post

router = APIRouter()


def get_es_client():
    """Get the dependency for ES client."""
    es_client = Elasticsearch(
        es_auth.host,
        basic_auth=(es_auth.user, es_auth.password.get_secret_value()),
    )

    try:
        yield es_client
    finally:
        es_client.close()


@router.get("/")
async def get_posts(
    query: str = Query(alias="q"),
    es_client: Elasticsearch = Depends(get_es_client),
) -> list[Post]:
    if len(query.strip()) == 0:
        raise HTTPException(
            status_code=400,
            detail="Please provide a valid query",
        )

    search_query = {
        "multi_match": {
            "query": query,
            "type": "most_fields",
            "operator": "and",
            "fields": [
                "title^3",
                "title.ngrams",
                "subtitle^2",
                "subtitle.ngrams",
            ],
        }
    }

    results = es_client.search(
        index=POSTS_INDEX_NAME,
        query=search_query,
    )

    posts_found: list[Post] = [
        Post(**hit["_source"]) for hit in results["hits"]["hits"]
    ]

    return posts_found
