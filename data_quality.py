import os
import re
import json
import pandas as pd

def tidy_phone(val):
    # clean phone, return up to 2 numbers
    if pd.isna(val):
        return None, None
    cleaned = re.sub(r"[^\d,]", "", str(val))
    parts = [p for p in cleaned.split(",") if p]
    p1 = parts[0] if len(parts) > 0 and len(parts[0]) >= 10 else None
    p2 = parts[1] if len(parts) > 1 and len(parts[1]) >= 10 else None
    return p1, p2

def scrub_text(val):
    # strip junk chars
    if pd.isna(val):
        return None
    return re.sub(r"[^a-zA-Z0-9\s,.]", "", str(val))

def quality_check(path: str, out_dir: str) -> dict:
    fname = os.path.basename(path)
    try:
        df = pd.read_csv(path)
    except Exception as e:
        print(f"> can't read {fname}: {e}")
        return {"file": fname, "error": str(e)}

    # phone split
    df[["phone_1", "phone_2"]] = df.apply(
        lambda r: pd.Series(tidy_phone(r.get("phone"))), axis=1
    )

    # clean a couple text cols
    for col in ("address", "reviews_list"):
        if col in df.columns:
            df[col] = df[col].apply(scrub_text)

    # required fields
    req = ["name", "phone_1", "location"]
    for c in req:
        if c not in df.columns:
            df[c] = None
    bad_mask = df[req].isnull().any(axis=1)

    good = df[~bad_mask]
    bad = df[bad_mask]

    base = os.path.splitext(fname)[0]
    out_ok = os.path.join(out_dir, f"{base}.out")
    out_bad = os.path.join(out_dir, f"{base}.bad")
    out_meta = os.path.join(out_dir, f"{base}.json")

    good.to_csv(out_ok, index=False)
    bad.to_csv(out_bad, index=False)

    problems = {}
    if not bad.empty:
        for c in req:
            rows = bad.index[bad[c].isnull()].tolist()
            if rows:
                problems[f"{c}_null"] = rows
        if problems:
            with open(out_meta, "w") as f:
                json.dump(problems, f, indent=2)
    else:
        out_meta = None

    print(f"> {fname}: {len(good)} good, {len(bad)} bad")

    return {
        "file": fname,
        "good_count": len(good),
        "bad_count": len(bad),
        "out_file": out_ok,
        "bad_file": out_bad,
        "meta_file": out_meta,
    }
