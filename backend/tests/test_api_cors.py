from app.main import app


def test_local_frontend_origin_is_configured() -> None:
    cors_middleware = next(
        middleware
        for middleware in app.user_middleware
        if middleware.cls.__name__ == "CORSMiddleware"
    )

    assert "http://127.0.0.1:5173" in cors_middleware.kwargs["allow_origins"]
    assert "http://localhost:5173" in cors_middleware.kwargs["allow_origins"]


def test_cors_origins_come_from_settings() -> None:
    cors_middleware = next(
        middleware
        for middleware in app.user_middleware
        if middleware.cls.__name__ == "CORSMiddleware"
    )

    assert cors_middleware.kwargs["allow_origins"]
