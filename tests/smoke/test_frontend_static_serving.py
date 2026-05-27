from pathlib import Path

from fastapi.testclient import TestClient

from farmer_helper import main


class _FakeSettings:
    def __init__(self, frontend_dist_dir: Path) -> None:
        self.app_log_level = "INFO"
        self.app_env = "test"
        self.sentry_dsn = None
        self.sentry_traces_sample_rate = 0.0
        self.sentry_environment = None
        self.frontend_serve_enabled = True
        self.frontend_dist_dir = str(frontend_dist_dir)


def test_backend_serves_frontend_index_and_spa_fallback(
    tmp_path: Path,
    monkeypatch,
) -> None:
    dist_dir = tmp_path / "dist"
    assets_dir = dist_dir / "assets"
    assets_dir.mkdir(parents=True)
    (dist_dir / "index.html").write_text(
        "<!doctype html><html><body><div id='root'></div></body></html>",
        encoding="utf-8",
    )
    (assets_dir / "app.js").write_text("console.log('ok');", encoding="utf-8")

    monkeypatch.setattr(main, "get_settings", lambda: _FakeSettings(dist_dir))
    monkeypatch.setattr(main, "configure_logging", lambda _level: None)
    monkeypatch.setattr(main, "configure_sentry", lambda _settings: False)

    app = main.create_app()
    client = TestClient(app)

    root = client.get("/")
    assert root.status_code == 200
    assert "text/html" in root.headers["content-type"]
    assert "id='root'" in root.text

    fallback = client.get("/user/chat")
    assert fallback.status_code == 200
    assert "text/html" in fallback.headers["content-type"]

    static_asset = client.get("/assets/app.js")
    assert static_asset.status_code == 200
    assert "console.log('ok');" in static_asset.text
