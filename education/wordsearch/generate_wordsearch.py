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
