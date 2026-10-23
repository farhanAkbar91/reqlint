import re
from typing import List, Dict, Any, Optional

class StoryParser:
    @staticmethod
    def split_stories(raw_text: str) -> List[Dict[str, Any]]:
        """
        Split a document or draft into individual user stories.
        Supports blank lines, numbered lists (1. ...), or bullet points (*, -).
        Preserves global character offsets so highlights map back accurately.
        """
        text = raw_text.strip()
        if not text:
            return []

        # Find line breaks or pattern splits
        # First check if there are numbered/bulleted stories or multiple paragraphs
        lines = raw_text.splitlines(keepends=True)
        stories: List[Dict[str, Any]] = []
        current_chunk = []
        current_start_offset = 0
        current_offset = 0

        for line in lines:
            line_len = len(line)
            stripped = line.strip()

            # Check if line indicates a new story:
            # 1. Numbered list: "1. As a...", "2. Sebagai..."
            # 2. Bullet list: "- As a...", "* Sebagai..."
            # 3. Explicit "Sebagai " or "As a " when already holding a chunk
            is_new_story_indicator = (
                bool(re.match(r'^\s*(\d+[\.\)]|[\*\-])\s+(sebagai|as\s+an?)', stripped, re.IGNORECASE)) or
                (bool(re.match(r'^\s*(sebagai|as\s+an?)\s+', stripped, re.IGNORECASE)) and len(current_chunk) > 0 and any(c.strip() for c in current_chunk))
            )

            # Check if blank line separating blocks
            is_blank = not stripped

            if (is_new_story_indicator or (is_blank and current_chunk)) and any(c.strip() for c in current_chunk):
                full_story_text = "".join(current_chunk).strip()
                if full_story_text:
                    # Find actual start index of non-whitespace
                    raw_block = "".join(current_chunk)
                    leading_spaces = len(raw_block) - len(raw_block.lstrip())
                    actual_start = current_start_offset + leading_spaces
                    stories.append({
                        "story_index": len(stories),
                        "text": full_story_text,
                        "start_offset": actual_start,
                        "end_offset": actual_start + len(full_story_text)
                    })
                current_chunk = []
                current_start_offset = current_offset

            current_chunk.append(line)
            current_offset += line_len

        if any(c.strip() for c in current_chunk):
            full_story_text = "".join(current_chunk).strip()
            if full_story_text:
                raw_block = "".join(current_chunk)
                leading_spaces = len(raw_block) - len(raw_block.lstrip())
                actual_start = current_start_offset + leading_spaces
                stories.append({
                    "story_index": len(stories),
                    "text": full_story_text,
                    "start_offset": actual_start,
                    "end_offset": actual_start + len(full_story_text)
                })

        # If nothing split, return the whole text as single story
        if not stories:
            stories.append({
                "story_index": 0,
                "text": text,
                "start_offset": raw_text.find(text),
                "end_offset": raw_text.find(text) + len(text)
            })

        return stories

    @staticmethod
    def parse_structure(story_text: str) -> Dict[str, Any]:
        """
        Parses Role, Means, and End in Indonesian and English.
        """
        # Patterns for Indonesian
        id_role = re.search(r'\bsebagai\s+([^,]+?)(?=,\s*saya|\s+saya|\s+agar|\s+sehingga|\s*$)', story_text, re.IGNORECASE)
        id_means = re.search(r'\b(?:saya\s+(?:ingin|mau|butuh|perlu))\s+([^,]+?)(?=,\s*(?:agar|sehingga|supaya|untuk)|\s+(?:agar|sehingga|supaya|untuk)|\s*$)', story_text, re.IGNORECASE)
        id_end = re.search(r'\b(?:agar|sehingga|supaya)\s+(.+)$', story_text, re.IGNORECASE)

        # Patterns for English
        en_role = re.search(r'\bas\s+(?:an?|the)\s+([^,]+?)(?=,\s*i|\s+i\s+want|\s+so\s+that|\s*$)', story_text, re.IGNORECASE)
        en_means = re.search(r'\bi\s+(?:want|need|wish)(?:\s+to)?\s+([^,]+?)(?=,\s*so\s+that|\s+so\s+that|\s*$)', story_text, re.IGNORECASE)
        en_end = re.search(r'\bso\s+that\s+(.+)$', story_text, re.IGNORECASE)

        role = None
        means = None
        end = None
        detected_lang = "en"

        # Check which language matches better
        if id_role or id_means or id_end:
            detected_lang = "id"
            role = id_role.group(1).strip() if id_role else None
            means = id_means.group(1).strip() if id_means else None
            end = id_end.group(1).strip() if id_end else None
        elif en_role or en_means or en_end:
            detected_lang = "en"
            role = en_role.group(1).strip() if en_role else None
            means = en_means.group(1).strip() if en_means else None
            end = en_end.group(1).strip() if en_end else None

        missing = []
        if not role:
            missing.append("Role")
        if not means:
            missing.append("Means")
        if not end:
            missing.append("End")

        return {
            "lang": detected_lang,
            "role": role,
            "means": means,
            "end": end,
            "missing_elements": missing
        }
