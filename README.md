# GitHub Contribution Art

This repository generates contribution-grid art by creating back-dated commits.

## What's Inside

- **pattern.txt** - A 7x53 grid pattern (Sun-Sat rows, 53 weeks) where each digit (0-4) represents commit intensity
- **paint.py** - Python script that creates commits with back-dated timestamps to paint the pattern on your GitHub contribution graph
- **pixel.txt** - The file that gets modified with each commit

## Design

The pattern creates two smiley faces side by side - one lighter (2s) and one darker (4s) - with decorative elements.

## Usage

Run the painter for 2025:
```bash
python3 paint.py 2025
git push origin main
```

## Note

This is purely cosmetic and for fun. The commits are clearly labeled and this README makes the purpose transparent.
