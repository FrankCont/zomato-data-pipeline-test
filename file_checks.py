import os

PROCESSED_LOG = "processed_files.txt"

def seen_before(fname: str) -> bool:
    # check if we processed this file already
    if not os.path.exists(PROCESSED_LOG):
        return False
    with open(PROCESSED_LOG, "r") as f:
        done = f.read().splitlines()
    return fname in done

def save_as_done(fname: str) -> None:
    # add file to processed log
    with open(PROCESSED_LOG, "a") as f:
        f.write(fname + "\n")

def basic_file_check(path: str, bad_dir: str) -> bool:
    """quick sanity checks on a file"""
    fname = os.path.basename(path)

    if seen_before(fname):
        print(f"> skip {fname}, done already")
        return False

    if not fname.lower().endswith(".csv"):
        print(f"> wrong ext: {fname}")
        os.rename(path, os.path.join(bad_dir, fname))
        return False

    if os.path.getsize(path) == 0:
        print(f"> empty file: {fname}")
        os.rename(path, os.path.join(bad_dir, fname))
        return False

    return True
