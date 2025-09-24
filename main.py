import os
from pathlib import Path
from file_checks import basic_file_check, save_as_done
from data_quality import quality_check

IN_DIR = "./input_files"
OUT_DIR = "./output_files"
BAD_DIR = "./invalid_files"

def ensure_dirs():
    for d in (IN_DIR, OUT_DIR, BAD_DIR):
        Path(d).mkdir(exist_ok=True)

if __name__ == "__main__":
    ensure_dirs()
    files = sorted(os.listdir(IN_DIR))
    if not files:
        print("> nothing in input_files/")
    for f in files:
        fpath = os.path.join(IN_DIR, f)
        if not os.path.isfile(fpath):
            continue
        if basic_file_check(fpath, BAD_DIR):
            result = quality_check(fpath, OUT_DIR)
            save_as_done(f)
            print(f"> summary: {result}")
            