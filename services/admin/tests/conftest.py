# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 The HuggingFace Authors.

from collections.abc import Iterator

from libcommon.queue import _clean_queue_database
from libcommon.resources import CacheMongoResource, QueueMongoResource
from libcommon.simple_cache import _clean_cache_database
from pytest import MonkeyPatch, TempPathFactory, fixture

from admin.config import AppConfig

# Import fixture modules as plugins
pytest_plugins = ["tests.fixtures.hub"]


# see https://github.com/pytest-dev/pytest/issues/363#issuecomment-406536200
@fixture(scope="session")
def monkeypatch_session(hf_endpoint: str, hf_token: str, tmp_path_factory: TempPathFactory) -> Iterator[MonkeyPatch]:
    monkeypatch_session = MonkeyPatch()
    assets_root = str(tmp_path_factory.mktemp("assets_root"))
    monkeypatch_session.setenv("CACHED_ASSETS_STORAGE_ROOT", assets_root)
    monkeypatch_session.setenv("ASSETS_STORAGE_ROOT", assets_root)
    monkeypatch_session.setenv("CACHE_MONGO_DATABASE", "dataset_viewer_cache_test")
    monkeypatch_session.setenv("QUEUE_MONGO_DATABASE", "dataset_viewer_queue_test")
    monkeypatch_session.setenv("COMMON_HF_ENDPOINT", hf_endpoint)
    monkeypatch_session.setenv("COMMON_HF_TOKEN", hf_token)
    monkeypatch_session.setenv("ADMIN_HF_TIMEOUT_SECONDS", "10")
    yield monkeypatch_session
    monkeypatch_session.undo()


@fixture(scope="session")
def app_config(monkeypatch_session: MonkeyPatch) -> AppConfig:
    app_config = AppConfig.from_env()
    if "test" not in app_config.cache.mongo_database or "test" not in app_config.queue.mongo_database:
        raise ValueError("Test must be launched on a test mongo database")
    return app_config


@fixture(autouse=True)
def cache_mongo_resource(app_config: AppConfig) -> Iterator[CacheMongoResource]:
    with CacheMongoResource(database=app_config.cache.mongo_database, host=app_config.cache.mongo_url) as resource:
        yield resource
        _clean_cache_database()


@fixture(autouse=True)
def queue_mongo_resource(app_config: AppConfig) -> Iterator[QueueMongoResource]:
    with QueueMongoResource(database=app_config.queue.mongo_database, host=app_config.queue.mongo_url) as resource:
        yield resource
        _clean_queue_database()


@fixture
def anyio_backend() -> str:
    return "asyncio"
