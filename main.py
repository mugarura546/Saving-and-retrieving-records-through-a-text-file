def save_records(vehicles, filename=DATA_FILE):
    temp = filename + ".tmp"
    with open(temp, "w", encoding="utf-8") as f:
        for v in vehicles:
            f.write(f"{v['registration']},{v['distance']:g},{v['fuel']:g}\n")
    os.replace(temp, filename)

def load_records(filename=DATA_FILE, reject_file=REJECT_FILE):
    vehicles, rejected = [], []
    if not os.path.exists(filename):
        return vehicles, rejected
    with open(filename, "r", encoding="utf-8") as f:
        for number, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            fields = [p.strip() for p in line.split(",")]
            if len(fields) != 3:
                rejected.append((number, line, f"expected 3 fields, found {len(fields)}"))
                continue
            ok, result = add_vehicle(vehicles, *fields)
            if not ok:
                rejected.append((number, line, result))
    if rejected:
        with open(reject_file, "a", encoding="utf-8") as log:
            for number, line, reason in rejected:
                log.write(f"line {number}: {line}  <-- {reason}\n")
    return vehicles, rejected
