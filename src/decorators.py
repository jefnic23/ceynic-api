def frontend(cls):
    """
    Marks a Pydantic model for frontend export.

    This decorator adds a `__frontend_export__ = True` attribute to the class,
    which can be detected during schema generation to selectively include only
    models intended for use in the frontend (e.g., to generate TypeScript interfaces).

    Usage:
        @frontend
        class MyModel(BaseModel):
            ...

    Returns:
        The class with the `__frontend_export__` attribute set.
    """
    cls.__frontend_export__ = True
    return cls
