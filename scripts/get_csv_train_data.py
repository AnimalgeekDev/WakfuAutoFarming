import os
import csv
import glob
from collections import defaultdict

try:
    from tensorflow.compat.v1.train import summary_iterator
except Exception:
    summary_iterator = None


TAGS = [
    "lr/pg0",
    "lr/pg1",
    "lr/pg2",
    "metrics/mAP50",
    "metrics/mAP50-95",
    "metrics/precision",
    "metrics/recall",
    "train/box_loss",
    "train/cls_loss",
    "train/dfl_loss",
    "val/box_loss",
    "val/cls_loss",
    "val/dfl_loss",
]


def find_event_files(runs_root="runs/detect/wakfu"):
    """Return list of (run_label, event_path) tuples found under runs_root."""
    out = []
    if not os.path.isdir(runs_root):
        return out
    for entry in sorted(os.listdir(runs_root)):
        folder = os.path.join(runs_root, entry)
        if not os.path.isdir(folder):
            continue
        # find event files recursively in the folder
        files = glob.glob(os.path.join(folder, "**", "events.out.tfevents.*"), recursive=True)
        for f in sorted(files):
            out.append((entry, f))
    return out


def extract_scalars_from_event(event_path, wanted_tags):
    """Yield (tag, step, wall_time, value) from a TF event file.

    Uses tensorflow.compat.v1.train.summary_iterator when available.
    """
    if summary_iterator is None:
        raise RuntimeError("tensorflow not available; please install tensorflow or tensorboard")
    for e in summary_iterator(event_path):
        if not hasattr(e, 'summary') or e.summary is None:
            continue
        for v in e.summary.value:
            tag = v.tag
            if tag in wanted_tags:
                # prefer simple_value
                val = None
                if hasattr(v, 'simple_value'):
                    val = v.simple_value
                else:
                    # other kinds not expected
                    continue
                yield tag, int(e.step), float(e.wall_time), float(val)


def aggregate_and_write_csv(runs_root="runs/detect/wakfu", out_dir="runs/csv_exports", training_configs=None):
    os.makedirs(out_dir, exist_ok=True)
    events = find_event_files(runs_root)
    if not events:
        print(f"No event files found in {runs_root}")
        return

    # Prepare CSV writers for each tag
    writers = {}
    files = {}
    for tag in TAGS:
        path = os.path.join(out_dir, f"{tag.replace('/', '_')}.csv")
        f = open(path, "w", newline='')
        files[tag] = f
        w = csv.writer(f)
        w.writerow(["run_label", "event_file", "step", "wall_time", "value"])
        writers[tag] = w

    # Process each event file
    for run_label, ev in events:
        try:
            for tag, step, wall_time, value in extract_scalars_from_event(ev, set(TAGS)):
                writers[tag].writerow([run_label, ev, step, wall_time, value])
        except Exception as e:
            print(f"Failed to read {ev}: {e}")

    for f in files.values():
        f.close()

    print(f"Exported CSVs to {out_dir}")


if __name__ == "__main__":
    # Default behavior: scan runs/detect/wakfu and export CSVs to runs/csv_exports
    aggregate_and_write_csv()
