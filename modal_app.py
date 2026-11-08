"""Public demo of Kedayam on Modal.

Deploy: modal deploy modal_app.py
URL:    https://applemacbook6sep2004--kedayam.us-east.modal.run

One small container (half a CPU, 512 MB) that scales to zero when idle, so the first
visit after a quiet spell takes a few seconds. KEDAYAM_HOSTED=1: messages and screenshots
are processed in memory and never saved or logged (as when installed), the family setup is
kept in memory per browser, and the server accepts its own host name. Tesseract uses the
same pinned tessdata_fast English, Tamil and Hindi models as `kedayam-ocr-setup`.
"""

from pathlib import Path

import modal

HERE = Path(__file__).resolve().parent
HOST = "applemacbook6sep2004--kedayam.us-east.modal.run"

image = (
    modal.Image.debian_slim(python_version="3.12")
    .apt_install("tesseract-ocr")
    .pip_install("fastapi==0.162.0", "jinja2==3.1.6", "python-multipart==0.0.33", "scikit-learn==1.9.1",
                 "joblib==1.6.0", "numpy==2.5.4", "scipy==1.18.1", "pillow==13.0.0")
    .env({"KEDAYAM_HOSTED": "1", "KEDAYAM_ALLOWED_HOSTS": HOST, "KEDAYAM_DATA_DIR": "/tmp/unused", "OMP_THREAD_LIMIT": "1"})
    .add_local_dir(str(HERE / "models"), "/root/kedayam/models")
    .add_local_dir(str(HERE / "vendor" / "tessdata"), "/root/kedayam/vendor/tessdata")
    .add_local_dir(str(HERE / "data"), "/root/kedayam/data")
    .add_local_dir(str(HERE / "src" / "kedayam"), "/root/kedayam/src/kedayam", ignore=["**/__pycache__"])
)

app = modal.App("kedayam")


@app.function(image=image, cpu=0.5, memory=512, min_containers=0, max_containers=1, scaledown_window=900)
@modal.concurrent(max_inputs=20)
@modal.asgi_app(label="kedayam")
def web():
    import sys

    sys.path.insert(0, "/root/kedayam/src")
    from kedayam.app import app as fastapi_app

    return fastapi_app
