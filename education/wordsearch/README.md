# WordSearch Functions

This folder contains functions for generating word search puzzles, specifically for teaching spelling and phonics.

## Purpose

Create word search puzzles based on vowel sounds (e.g., long vowel O as in "bone") with curated words for specific age ranges.

## Structure

### `generate_wordsearch.py`
- Main function to generate word search puzzles
- Accepts vowel sound as input (e.g., "long_o", "short_e", "ai", "oa")
- Configurable word count (default 20)
- Age-based word filtering
- Output folder organization by vowel and age

## Usage

```bash
# Generate wordsearch for long O vowel
python generate_wordsearch.py --vowel long_o --age_range 6-8 --words 20

# Generate wordsearch for short E vowel
python generate_wordsearch.py --vowel short_e --age_range 6-9 --words 20

# Generate for specific vowels
python generate_wordsearch.py --vowel ai --age_range 6-8
```

## Wordsearch Format

Each generated wordsearch includes:
- Grid with embedded words
- Word list with phonetic pronunciations
- Age-appropriate vocabulary
- Difficulty level indicator
- Solution key (separate file)

## Output Organization

Generated files are saved in folders named by vowel sound:
```
education/wordsearch/
└── long_o/
    ├── age_6_8/
    │   ├── wordsearch_001.png
    │   ├── words_list.json
    │   └── solution.pdf
    └── ...
```
