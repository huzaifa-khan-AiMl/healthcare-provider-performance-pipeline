import os
import sys
import zipfile
import argparse
import requests
from pathlib import Path

CMS_DATASET_URLS = {
    "2022": "https://data.cms.gov/data-api/v1/dataset/e650987d-01b7-4f09-b75e-b0b075afbf98/data-viewer?_format=csv"
}

def stream_download(url: str, dest_path: Path):
    """Streams data from CMS in 1 MB chunks to prevent RAM overflow."""
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    print(f"Connecting to: {url}")
    with requests.get(url, headers=headers, stream=True, timeout=120) as response:
        response.raise_for_status()
        total_size = int(response.headers.get("content-length", 0))
        downloaded = 0
        chunk_size = 1024 * 1024  # 1 MB

        print(f"Downloading archive to: {dest_path}")
        with open(dest_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        mb_down = downloaded / (1024 * 1024)
                        mb_total = total_size / (1024 * 1024)
                        sys.stdout.write(f"\rProgress: {mb_down:.1f} MB / {mb_total:.1f} MB ({percent:.1f}%)")
                    else:
                        mb_down = downloaded / (1024 * 1024)
                        sys.stdout.write(f"\rDownloaded: {mb_down:.1f} MB")
                    sys.stdout.flush()
    print("\nDownload complete.")

def main():
    parser = argparse.ArgumentParser(description="Acquire CMS Medicare Part B dataset.")
    parser.add_argument("--year", default="2022", choices=["2022"], help="Publication year to download")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent.parent
    raw_dir = project_root / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    # Check if uncompressed CSV already exists (Idempotency)
    existing_csvs = list(raw_dir.glob("*.csv"))
    if existing_csvs and existing_csvs[0].stat().st_size > 100 * 1024 * 1024:
        print(f"Found existing raw dataset: {existing_csvs[0].name} ({existing_csvs[0].stat().st_size / (1024*1024):.1f} MB). Skipping download.")
        return

    url = CMS_DATASET_URLS.get(args.year)
    zip_path = raw_dir / f"medicare_part_b_{args.year}.zip"

    try:
        stream_download(url, zip_path)
        print(f"Extracting archive into {raw_dir}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(raw_dir)
        print("Extraction complete.")
        
        # Remove the downloaded .zip to save disk space
        zip_path.unlink()
        print("Cleaned up temporary archive.")
        
    except requests.exceptions.RequestException as e:
        print(f"\n[ERROR] Download failed: {e}")
        print("\nManual Fallback:")
        print(f"1. Download via browser: {url}")
        print(f"2. Unzip and place the CSV into: {raw_dir}/")
        sys.exit(1)
    except zipfile.BadZipFile as e:
        print(f"\n[ERROR] Corrupted ZIP file: {e}")
        if zip_path.exists():
            zip_path.unlink()
        sys.exit(1)

if __name__ == "__main__":
    main()
