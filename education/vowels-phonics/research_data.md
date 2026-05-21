# Vowels and Phonics Research Data

## Purpose

Efficient storage for vowel and phonics research data used in spelling education.

## Structure

- `/vowels/` - Vowel sounds and spellings
- `/phonics/` - Phonics rules and patterns
- `/constants/` - Common constant patterns
- `/research/` - Research findings and data

## Data Format

```json
{
  "vowel": "a",
  "phonetic": "/eɪ/|/æ/|/ɑː/",
  "spellings": ["a", "ai", "ay", "ae", "al", "au"],
  "word_examples": ["cat", "bait", "day", "face"],
  "exceptions": ["all", "ball", "hall"],
  "research_sources": ["source1", "source2"],
  "last_updated": "2026-05-21"
}
```

## Efficiency Notes

- Use JSON for structured data
- Store frequently accessed data in separate files
- Index by vowel/phoneme for quick lookup
- Maintain research citations separately
