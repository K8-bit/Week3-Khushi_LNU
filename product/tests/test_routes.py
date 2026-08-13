from product.main import app


def test_print_registered_routes() -> None:
    paths = app.openapi().get("paths", {})

    for path, operations in paths.items():
        methods = [
            method.upper()
            for method in operations
            if method.lower() in {"get", "post", "put", "patch", "delete"}
        ]
        print(f"{methods} {path}")

    assert paths, "No API routes are registered"
