from pydantic import BaseSettings, Field, SecretStr


class ESAuth(BaseSettings):
    """Settings for Elasticsearch."""

    host: str = Field(env="ES_HOST", default="http://localhost:9200")
    user: str = Field(env="ES_USER", default="elastic")
    password: SecretStr = Field(env="ES_PASSWORD", default="elastic")


es_auth = ESAuth()

POSTS_INDEX_NAME = "posts"

POSTS_INDEX_SYNONYMS = [
    "es, elasticsearch",
    "js, javascript",
    "ts, typescript",
    "k8s, k9s, Kubernetes",
]

POSTS_INDEX_SETTINGS = {
    "analysis": {
        "analyzer": {
            "post_index_analyzer": {
                "type": "custom",
                "tokenizer": "standard",
                "filter": [
                    "lowercase",
                    "autocomplete_filter",
                ],
            },
            "post_search_analyzer": {
                "type": "custom",
                "tokenizer": "standard",
                "filter": [
                    "lowercase",
                    "synonym_filter",
                ],
            },
        },
        "filter": {
            "synonym_filter": {
                "type": "synonym_graph",
                "expand": True,
                "lenient": True,
                "synonyms": POSTS_INDEX_SYNONYMS,
            },
            "autocomplete_filter": {
                "type": "edge_ngram",
                "min_gram": 1,
                "max_gram": 20,
            },
        },
    },
}


POSTS_INDEX_MAPPINGS = {
    "properties": {
        "display_tag": {"type": "text"},
        "id": {"type": "keyword"},
        "image_url": {"type": "keyword"},
        "published_at": {"type": "date", "format": "yyyy-MM-dd"},
        "reading_time": {"type": "float"},
        "subtitle": {
            "type": "text",
            "search_analyzer": "post_search_analyzer",
            "fields": {
                "ngrams": {
                    "type": "text",
                    "analyzer": "post_index_analyzer",
                    "search_analyzer": "post_search_analyzer",
                },
            },
        },
        "tags": {"type": "text"},
        "title": {
            "type": "text",
            "search_analyzer": "post_search_analyzer",
            "fields": {
                "ngrams": {
                    "type": "text",
                    "analyzer": "post_index_analyzer",
                    "search_analyzer": "post_search_analyzer",
                },
            },
        },
        "url": {"type": "keyword"},
    }
}
