# pylint: disable=W0621

import json

import pytest
from flask import current_app

import example


JSON_CONTENT = {"Content-Type": "application/json"}


@pytest.fixture
def client():
    test_client = example.app.test_client()
    with example.app.app_context():
        current_app.config["DATABASE"] = example.Database({"network": {}})

    yield test_client


def get_json(resp):
    return json.loads(resp.data.decode())


def test_get(client):
    resp = client.get("/config/network")
    assert resp.headers["ETag"] == '"bf21a9e8fbc5a3846fb05b4fa0859e0917b2202f"'
    assert get_json(resp) == {}


def test_get_with_meta(client):
    resp = client.get("/config/network?require_meta=yes")
    resp_json = get_json(resp)
    assert "meta" in resp_json
    assert "etag" in resp_json["meta"]
    assert '"' + resp_json["meta"]["etag"] + '"' == resp.headers["ETag"]
    assert resp_json == {
        "body": {},
        "meta": {"etag": "bf21a9e8fbc5a3846fb05b4fa0859e0917b2202f", "pointer": "network"},
    }


def test_get_404(client):
    resp = client.get("/config/foo")
    assert resp.status_code == 404

    resp_json = get_json(resp)

    assert resp_json == {"error": "member 'foo' not found in {'network': {}}", "meta": {"pointer": "foo"}}


def test_put(client):
    resp = client.get("/config/network")
    etag = resp.headers["ETag"]

    data_json = {"meta": {"etag": etag}, "body": []}
    resp = client.put("/config/network", headers=JSON_CONTENT, data=json.dumps(data_json))
    assert resp.status_code == 200
    assert get_json(resp) == []

    resp = client.get("/config/network")
    assert get_json(resp) == []


def test_put_invalid_etag(client):
    data_json = {"meta": {"etag": "deadbeef"}, "body": []}
    resp = client.put("/config/network", headers=JSON_CONTENT, data=json.dumps(data_json))
    assert resp.status_code == 400
    assert get_json(resp) == {"error": "Etag mismatch"}

    resp = client.get("/config/network")
    assert get_json(resp) == {}


def test_put_etag_missing(client):
    data_json = {"body": []}
    resp = client.put("/config/network", headers=JSON_CONTENT, data=json.dumps(data_json))
    assert resp.status_code == 400
    assert get_json(resp) == {"error": "Etag missing from request"}


def test_put_invalid_json(client):
    resp = client.put("/config/network", headers=JSON_CONTENT, data="invalid-json")
    assert resp.status_code == 400
    assert get_json(resp) == {
        "error": "The browser (or proxy) sent a request that this server could not understand."
    }


def test_post(client):
    resp = client.post("/config/network/interfaces", headers=JSON_CONTENT, data='{"addresses": []}')
    assert get_json(resp) == {"addresses": []}
    assert resp.status_code == 200

    resp = client.get("/config/network/interfaces")
    assert get_json(resp) == {"addresses": []}
    assert resp.headers["ETag"] == '"5568e6bf737d11fedd1e624b7b7245c41f05f20e"'


def test_post_no_parent(client):
    resp = client.post("/config/network/foo/bar/baz", headers=JSON_CONTENT, data='{"addresses": []}')
    assert resp.status_code == 400
    assert get_json(resp) == {
        "error": "member 'foo' not found in {}",
        "meta": {"pointer": "network/foo/bar/baz"},
    }
