import pytest


@pytest.fixture(autouse=True)
def isolated_family_store(tmp_path, monkeypatch):
    """Every test gets an empty family store, never the real one."""
    monkeypatch.setenv("KEDAYAM_DATA_DIR", str(tmp_path / "instance"))
