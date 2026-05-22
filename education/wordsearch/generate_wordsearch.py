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
