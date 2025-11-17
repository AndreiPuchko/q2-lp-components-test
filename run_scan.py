import os
import json
from pathlib import Path

import sys
sys.stdout.reconfigure(encoding='utf-8')

def generate_folder_content(base_path: str):
    """
    Recursively walk through base_path and create folder_content.json in each folder.
    """
    base_path = Path(base_path).resolve()

    for root, dirs, files in os.walk(base_path):
        folder_path = Path(root)

        # Exclude the manifest itself
        if "folder_content.json" in files:
            files.remove("folder_content.json")

        # Prepare data
        data = {
            "folders": sorted(dirs),
            "files": sorted([x for x in files if x.endswith(".json")]),
        }

        json_path = folder_path / "folder_content.json"

        # Only update if changed
        if json_path.exists():
            try:
                old_data = json.loads(json_path.read_text(encoding="utf-8"))
                if old_data == data:
                    continue  # No changes
            except Exception:
                pass  # Overwrite if corrupted

        # Write JSON
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"✅ Created {json_path.relative_to(base_path)}")

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: run_scan.py <path>")
        sys.exit(1)

    target_dir = sys.argv[1]
    generate_folder_content(target_dir)
    print("All folder_content.json files created successfully.")
