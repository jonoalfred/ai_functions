#!/usr/bin/env python3
"""
WordSearch Generator for Vowel-Based Spelling Practice
Creates word search puzzles for specific vowel sounds and age ranges.
"""

import argparse
import json
import os
import random
import string
from pathlib import Path
from typing import Dict, List, Tuple


def setup_argument_parser() -> argparse.Namespace:
    """Configure and parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate word search puzzles for vowel sounds and age groups."
    )
    
    parser.add_argument(
        "--vowel",
        type=str,
        required=True,
        choices=["a", "e", "i", "o", "u", "long_a", "short_a", 
                 "long_e", "short_e", "long_i", "long_o", "short_o",
                 "long_u", "short_u", "ai", "ay", "oy", "au", "aw",
                 "ea", "ee", "ie", "oa", "oo", "ow", "er", "ir", "or"],
        help="Vowel sound to focus on (e.g., 'long_o', 'short_e', 'ai')"
    )
    
    parser.add_argument(
        "--age",
        type=int,
        default=7,
        help="Target age for word selection (default: 7)"
    )
    
    parser.add_argument(
        "--age-range",
        type=str,
        default="6-8",
        help="Age range in format 'min-max' (e.g., '6-8', '7-9')"
    )
    
    parser.add_argument(
        "--words",
        type=int,
        default=20,
        help="Number of words to include (default: 20)"
    )
    
    parser.add_argument(
        "--output-dir",
        type=str,
        default="./output",
        help="Output directory for generated puzzles"
    )
    
    parser.add_argument(
        "--grid-size",
        type=int,
        default=15,
        help="Grid size (default: 15)"
    )
    
    return parser.parse_args()


# ============ DATABASE SCHEMA (Job 1) ============
# Efficient persistent word database - builds on execution

from datetime import datetime

DB_FILE = Path(__file__).parent / "words.json"

def get_db() -> Dict:
    """Load or create word database."""
    if not DB_FILE.exists():
        # Create empty schema with all vowel categories
        schema = {
            "long_a": [], "short_a": [],
            "long_e": [], "short_e": [],
            "long_i": [], "long_o": [], "short_o": [],
            "long_u": [], "short_u": [],
            "ai": [], "ay": [], "oy": [], "au": [], "aw": [],
            "ea": [], "ee": [], "ie": [], "oa": [], "oo": [],
            "ow": [], "ou": [], "er": [], "ir": [], "or": [],
        }
        return schema
    
    with open(DB_FILE) as f:
        return json.load(f)

def save_db(db: Dict) -> None:
    """Persist database to file."""
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=2)

def get_words_for_vowel(vowel: str) -> List:
    """Get words for a specific vowel sound."""
    db = get_db()
    return db.get(vowel, [])

def add_word(vowel: str, word: str) -> None:
    """Add a single word to the database."""
    db = get_db()
    if vowel not in db:
        db[vowel] = []
    db[vowel].append({"word": word, "timestamp": datetime.now().isoformat()})
    save_db(db)

def get_word_count(vowel: str) -> int:
    """Get count of words for a vowel."""
    return len(get_words_for_vowel(vowel))


# ============ WORD FILTERING (Job 2) ============
# Efficient word filtering - lightweight string matching

def filter_words_by_vowel(words: List[str], vowel: str) -> List[str]:
    """Filter words containing the vowel sound."""
    return [w for w in words if vowel in w.lower()]

def filter_by_age(words: List[str], age: int) -> List[str]:
    """Filter words by age difficulty (simplified) - keep all for now."""
    return words  # Can add age logic later if needed

def get_20_words(vowel: str, age: int = 7) -> List[str]:
    """Get up to 20 words for a vowel and age."""
    raw_words = get_words_for_vowel(vowel)
    filtered = filter_words_by_vowel(raw_words, vowel)
    age_filtered = filter_by_age(filtered, age)
    return age_filtered[:20]  # Limit to 20 words

def ensure_minimum_words(vowel: str, target: int = 20) -> Tuple[List[str], bool]:
    """Ensure minimum word count, return words and success flag."""
    words = get_20_words(vowel)
    return words, len(words) >= target

def get_fallback_words(vowel: str, count: int = 5) -> List[str]:
    """Return simple fallback words if database empty."""
    fallbacks = {
        "a": ["aardvark", "ant", "ago", "apt", "axe"],
        "e": ["elephant", "egg", "end", "ear", "eat"],
        "i": ["igloo", "ink", "ivy", "ice", "ill"],
        "o": ["owl", "oar", "odd", "on", "ox"],
        "u": ["umbrella", "up", "use", "urn", "url"],
    }
    default = ["apple", "book", "cat", "dog", "fish"]
    return fallbacks.get(vowel, default)[:count]

def select_best_words(vowel: str, target: int = 20) -> List[str]:
    """Select best 20 words for grid generation."""
    words, has_enough = ensure_minimum_words(vowel, target)
    if has_enough:
        return words
    # If not enough, use first available + fallbacks
    available = get_words_for_vowel(vowel)
    fallback = get_fallback_words(vowel)
    combined = available + fallback
    return combined[:target]


# ============ MAIN EXECUTION ============
def main():
    """Main entry point."""
    args = setup_argument_parser()
    
    # Get words for this vowel
    words = select_best_words(args.vowel, args.words)
    
    if not words:
        print(f"No words found for vowel: {args.vowel}")
        print("Run first to build database, or add words manually.")
        return
    
    print(f"Generated wordsearch for vowel: {args.vowel}")
    print(f"Found {len(words)} words (target: {args.words})")
    
    # TODO: Call grid generation here
    # grid, placed_words = generate_grid(words, args.grid_size)
    # TODO: Save output
    # save_wordsearch(grid, words, args.output_dir)

if __name__ == "__main__":
    main()


# ============ FILE OUTPUT (Job 4) ============
# Save grid and word list to files - lightweight, no heavy deps

def save_wordlist(words: List[str], filepath: str) -> None:
    """Save word list to JSON file."""
    data = {"words": words}
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def save_grid_ascii(grid: List[List[str]], filepath: str) -> None:
    """Save grid as ASCII text file."""
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w') as f:
        for row in grid:
            f.write(' '.join(row) + '\n')

def save_solution(words: List[str], filepath: str) -> None:
    """Save solution file with word list."""
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w') as f:
        f.write('SOLUTION\n')
        f.write('=' * 20 + '\n')
        for word in words:
            f.write(word + ' \n')


def main():
    """Main entry point - full execution."""
    args = setup_argument_parser()
    
    # Get words for this vowel
    words = select_best_words(args.vowel, args.words)
    
    if not words:
        print(f"No words found for vowel: {args.vowel}")
        print("Run first to build database, or add words manually.")
        return
    
    print(f"Generated wordsearch for vowel: {args.vowel}")
    print(f"Found {len(words)} words (target: {args.words})")
    
    # Create grid
    grid, placed_words = generate_grid(words, args.grid_size)
    print(f"Placed {len(placed_words)} words in {args.grid_size}x{args.grid_size} grid")
    
    # Save all outputs
    puzzle_id = f"{args.vowel}_{len(words)}w"
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save word list
    wordlist_path = output_dir / f"{puzzle_id}_words.json"
    save_wordlist(placed_words, str(wordlist_path))
    
    # Save grid
    grid_path = output_dir / f"{puzzle_id}_grid.txt"
    save_grid_ascii(grid, str(grid_path))
    
    # Save solution
    solution_path = output_dir / f"{puzzle_id}_solution.txt"
    save_solution(placed_words, str(solution_path))
    
    print(f"Saved to: {output_dir}")

if __name__ == "__main__":
    main()



