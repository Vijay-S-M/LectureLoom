"""Polite downloader: python tools/download.py urls.txt.

urls.txt: one URL per line (lines starting with # are skipped).
Saves files to data/raw/ and logs every file to data/manifest.csv.
"""

import csv
import hashlib
import os
import sys
import time
from datetime import date
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

RAW = "data/raw"
MANIFEST = "data/manifest.csv"
HEADERS = {
    "User-Agent": (
        "ExamateStudentProject/1.0 (learning project; contact:"
        " your-email@example.com)"
    )
}
DELAY = 2  # seconds between requests: be polite to government servers

robots = {}


def allowed(url):
    root = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
    if root not in robots:
        rp = RobotFileParser(f"{root}/robots.txt")
        try:
            rp.read()
        except Exception:
            rp = None  # robots.txt unreachable: proceed carefully
        robots[root] = rp

    rp = robots[root]
    return rp is None or rp.can_fetch(HEADERS["User-Agent"], url)


def name_for(url):
    name = os.path.basename(urlparse(url).path) or "index.html"
    return name.replace(" ", "_")


def main(list_file):
    os.makedirs(RAW, exist_ok=True)

    new_manifest = not os.path.exists(MANIFEST)

    with open(MANIFEST, "a", newline="") as mf:
        log = csv.writer(mf)

        if new_manifest:
            log.writerow([
                "file",
                "source_url",
                "downloaded_on",
                "bytes",
                "sha256"
            ])

        with open(list_file) as fh:
            urls = [u.strip() for u in fh]

        for url in urls:
            if not url or url.startswith("#"):
                continue

            path = os.path.join(RAW, name_for(url))

            if os.path.exists(path):
                print("skip (already have)", path)
                continue

            if not allowed(url):
                print("BLOCKED by robots.txt, not downloading:", url)
                continue

            request = Request(url, headers=HEADERS)
            try:
                with urlopen(request, timeout=30) as response:
                    status = response.status
                    content = response.read()
            except HTTPError as error:
                status = error.code
                content = b""

            if status != 200:
                print("failed", status, url)
                continue

            with open(path, "wb") as f:
                f.write(content)

            digest = hashlib.sha256(content).hexdigest()[:16]

            log.writerow([
                path,
                url,
                date.today().isoformat(),
                len(content),
                digest
            ])

            print("saved", path, len(content), "bytes")

            time.sleep(DELAY)


if __name__ == "__main__":
    main(sys.argv[1])