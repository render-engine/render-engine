from .page import Page
from elasticsearch.helpers import bulk
from dataclasses import dataclass
import elastic_app_search as app_search


import elasticsearch

from functools import wraps
import json
import logging
import typing
import hashlib


def _id_hash(page, *id_fields):
    """Generate a Hash from the provided fields"""
    raw_msg = ''.join([getattr(page,x,"") for x in id_fields]).encode('utf-8')
    return hashlib.sha1(raw_msg).hexdigest()


def _build_index(pages, id_field="_id", **search_params):
    """Build a page dict for the keys requested. There is a
    question if this should be replaced with a __dict__ overwrite on page."""

    for page in pages:
        page_dict = {}

        for key, key_params in search_params['fields'].items():

            if field_value := getattr(page, key, None):

                if key_params['type'] == "date":
                    page_dict[key] = field_value.to_rfc3339_string()

                else:
                    page_dict[key] = field_value

        page_dict[id_field] = _id_hash(page, *search_params["id_fields"])

        yield page_dict


def fuse(search: typing.Dict, filepath: str):
    """Build a JSON doc of your pages"""

    with open(filepath, "w") as jsonfile:
        return json.dump(
            [x for x in _build_index(search, id_field="id")],
            fp=jsonfile,
        )


def elasticsearch(
        _, # called inside a class
        search_client: elasticsearch.Elasticsearch,
        pages,
        **search_params,
        ):
    """Upload the pages to an elasticsearch index

    Parameters
    ----------
    search: Search-like object
        Search object from site to push to elasticsearch instance
    pages: list[Page]
        page-like objects to build_indexes out of

    Returns
    -------
    bulk operation
        the bulk command sent to your elasticsearch instance"""
    return bulk(
            client=search_client,
            index=search_params['index'],
            actions=(x for x in _build_index(pages=pages, **search_params)),
            )


def elastic_app_search(
    _,
    search_client, 
    pages,
    **search_params,
    ):
    """Upload the pages to an enterprise app search engine

    Parameters
    ----------
    host: str
        host for the enterprise app search instance.
    api_key: str
        **private** api_key for the app search instance
    engine: str
        name of the app search engine to add documents to
    pages: list[Page]
        page-like objects to build_indexes out of
    use_https: bool, default=False
        is the host using https
    fields: fields to iniclude in the build_index
    id_fields: the fields to use in generating the id (to prevent duplicate entries)
    """

    documents=[x for x in _build_index(pages=pages, id_field='id', **search_params)]
    return search_client.index_documents(
        engine_name=search_params['engine'],
        documents=documents,
    )
