import subprocess, os, sys, random
from datetime import datetime, timedelta

TARGET_YEAR = int(sys.argv[1]) if len(sys.argv) > 1 else datetime.now().year

# Load pattern: 7 rows (Sun..Sat), each with up to 53 digits (0-9)
with open("pattern.txt") as f:
    rows = [line.strip() for line in f if line.strip()]

if len(rows) != 7:
    raise SystemExit("pattern.txt must have exactly 7 lines (Sun..Sat).")

# Find the grid's first Sunday covering TARGET_YEAR.
# GitHub shows the year ending on the last Saturday of the year.
# We'll start from the Sunday 52 weeks before the first Sunday on/after Jan 1.
jan1 = datetime(TARGET_YEAR, 1, 1)
first_sunday = jan1 + timedelta(days=(6 - jan1.weekday()) % 7)  # weekday(): Mon=0..Sun=6
grid_start = first_sunday - timedelta(weeks=52)

# Normalize row lengths to the longest (pad with zeros)
width = max(len(r) for r in rows)
rows = [r.ljust(width, "0") for r in rows]

def sh(cmd, env=None):
    subprocess.run(cmd, shell=True, check=True, env=env)

for week in range(width):
    for day in range(7):  # 0..6 (Sun..Sat)
        n = int(rows[day][week])
        if n <= 0:
            continue
        date = grid_start + timedelta(weeks=week, days=day)
        # Ensure the date is inside the chosen year window (optional guard)
        if date.year not in (TARGET_YEAR-1, TARGET_YEAR, TARGET_YEAR+1):
            continue
        for i in range(n):
            # Vary seconds so multiple commits on same day have unique timestamps
            ts = date + timedelta(seconds=random.randint(0, 86399))
            iso = ts.strftime("%Y-%m-%d %H:%M:%S")
            # Write something small so it's not an empty commit
            with open("pixel.txt", "a") as f:
                f.write(f"{iso} {week}:{day}:{i}\n")
            sh("git add pixel.txt")
            env = os.environ.copy()
            env["GIT_AUTHOR_DATE"] = iso
            env["GIT_COMMITTER_DATE"] = iso
            sh(f'git commit -m "pixel {week}:{day}:{i} on {iso}"', env=env)

print("Done creating local history. Now push: git push origin main")

