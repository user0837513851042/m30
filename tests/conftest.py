import pytest
import asyncio
from fastapi.testclient import TestClient
from m30.src.app import create_app
import m30.src.models as models


@pytest.fixture
def app():
    _app = create_app(db_url="sqlite+aiosqlite:///./testing.db")

    # db init
    new_recipe = models.Recipe(
        id=1,
        title="test recipe",
        description="some description",
        ingredients="salt, water",
        cooking_time=60,
    )

    async def db_init():
        async with _app.db_engine.begin() as conn:
            await conn.run_sync(_app.Base.metadata.create_all)

        async with _app.db_session.begin():
            _app.db_session.add(new_recipe)

    async def shutdown():
        async with _app.db_engine.begin() as conn:
            await conn.run_sync(_app.Base.metadata.drop_all)
        await _app.db_session.close()
        await _app.db_engine.dispose()
    
    asyncio.run(db_init())

    yield _app

    asyncio.run(shutdown())


@pytest.fixture
def client(app):
    client = TestClient(app)
    yield client