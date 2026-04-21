#!/usr/bin/env python3
import base64
import io
import subprocess
from pathlib import Path

import qrcode

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "scripts" / "kit-template.html"
OUTPUT_HTML = ROOT / "scripts" / "kit-rendered.html"
OUTPUT_PDF = ROOT / "assets" / "kit" / "nidosync-profesionales-kit.pdf"

QR_URL = "https://nidosync.app"


def qr_data_uri(data: str) -> str:
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=14,
        border=2,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#2e2a26", back_color="#fef8f3")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"data:image/png;base64,{b64}"


def main() -> None:
    html = TEMPLATE.read_text(encoding="utf-8")
    html = html.replace("{{QR_DATA_URI}}", qr_data_uri(QR_URL))
    OUTPUT_HTML.write_text(html, encoding="utf-8")

    cmd = [
        "google-chrome",
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        "--virtual-time-budget=10000",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={OUTPUT_PDF}",
        f"file://{OUTPUT_HTML}",
    ]
    subprocess.run(cmd, check=True)
    print(f"PDF generado: {OUTPUT_PDF} ({OUTPUT_PDF.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
