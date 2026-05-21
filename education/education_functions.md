# Education Functions

This folder contains AI automation functions for educational purposes.

## Purpose

Reusable processes for teaching and learning various subjects.

## Function Structure

### `vowels-phonics/`
- **pull_research.py** - Pull research about vowels and phonics
- **store_data.py** - Store research data efficiently  
- **vowels.json** - Vowel sounds and spellings
- **phonics_rules.json** - Phonics rules and patterns
- **research_data.md** - Research data documentation

### Other folders to create:
- `spelling/` - Spelling research and helpers
- `math/` - Mathematics education functions
- `science/` - Science education functions
- `language/` - Language learning functions

## Data Efficiency

- Use JSON for structured data
- Store frequently accessed data in separate files
- Index by key for quick lookup
- Maintain research citations separately
- Use compression for large datasets

## First Function: Vowels and Phonics

This function pulls research about English vowels, specifically for teaching spelling and phonics. The information is stored in an efficient JSON format with:
- Vowel sounds and phonetic transcriptions
- Common spellings and patterns
- Example words
- Research sources
- Last update timestamps

## Usage

```bash
# Pull vowel research
python pull_research.py --topic vowel --source dictionary

# Pull phonics rules  
python pull_research.py --topic phonics --source curriculum

# Get constant patterns
python pull_research.py --topic constants
```
