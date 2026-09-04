from typing import Annotated, List

from fastapi import FastAPI, HTTPException, Path
from sqlalchemy.future import select

import m30.src.models as models
import m30.src.schemas as schemas
from m30.src.database import Base, create_connection


def create_app(db_url: str = "sqlite+aiosqlite:///./app.py.db"):
    app = FastAPI()
    app.db_engine, app.db_session = create_connection(db_url)
    app.Base = Base

    @app.on_event("startup")
    async def startup():
        async with app.db_engine.begin() as conn:
            await conn.run_sync(app.Base.metadata.create_all)

    @app.on_event("shutdown")
    async def shutdown():
        await app.db_session.close()
        await app.db_engine.dispose()

    @app.get("/recipes/{recipe_id}", response_model=schemas.RecipeDetailResponse)
    async def recipe(
        recipe_id: int = Annotated[..., Path(..., title="ID of a recipe.")]
    ) -> models.Recipe:
        """
        Shows detailed information about a recipe.
        """

        recipe = await app.db_session.get(models.Recipe, recipe_id)

        if recipe is None:
            raise HTTPException(status_code=404, detail="Recipe not found")

        recipe.views += 1
        await app.db_session.commit()

        return recipe

    @app.get("/recipes/", response_model=list[schemas.RecipeListResponse])
    async def recipes() -> List[models.Recipe]:
        """
        Lists all recipes.
        """
        res = await app.db_session.execute(
            select(models.Recipe).order_by(models.Recipe.views)
        )
        return res.scalars().all()

    @app.post("/recipes", response_model=schemas.RecipeDetailResponse)
    async def create_recipe(recipe: schemas.RecipeCreate) -> models.Recipe:
        """
        Creates a new recipe.
        """
        new_recipe = models.Recipe(
            title=recipe.title,
            description=recipe.description,
            ingredients=recipe.ingredients,
            cooking_time=recipe.cooking_time,
        )

        async with app.db_session.begin():
            app.db_session.add(new_recipe)

        return new_recipe

    return app
