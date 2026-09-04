from pydantic import BaseModel, Field


class RecipeBase(BaseModel):
    title: str = Field(examples=["Tomato soup"], description="The name of the recipe")
    cooking_time: int = Field(
        ge=1, examples=[60], description="The cooking time of the recipe, in minutes"
    )


class RecipeCreate(RecipeBase):
    """
    Request model used to create a new recipe
    """

    description: str | None = Field(
        examples=["Some description"], description="The description of the recipe"
    )
    ingredients: str = Field(
        examples=["Salt, water"], description="The ingredients used in the recipe"
    )


class RecipeListResponse(RecipeBase):
    """
    Information returned when listing recipes
    """

    views: int = Field(description="How many times the recipe was viewed")

    class Config:
        from_attributes = True


class RecipeDetailResponse(RecipeBase):
    """
    Information returned about a single recipe
    """

    description: str | None = Field(
        examples=["Some description"], description="The description of the recipe"
    )
    ingredients: str = Field(
        examples=["Salt, water"], description="The ingredients used in the recipe"
    )

    class Config:
        from_attributes = True
