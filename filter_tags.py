import os
import yaml
from pathlib import Path
from collections import defaultdict

# List of allowed tags
ALLOWED_TAGS = {
    "accents",
    "anchors",
    "appearance",
    "glyph set",
    "clipboard",
    "components",
    "contours",
    "designspace",
    "diacritics",
    "drawing",
    "tools",
    "extension management",
    "ezui",
    "figures",
    "font dimensions",
    "font generation",
    "font lib",
    "font overview",
    "fractions",
    "glyph generator",
    "glyph editor",
    "glyphs",
    "groups",
    "font info",
    "guidelines",
    "inspector",
    "interpolation",
    "italics",
    "hinting",
    "images",
    "kerning",
    "layers",
    "menu",
    "measuring",
    "merz",
    "mojo",
    "notes",
    "notifications",
    "observers",
    "pens",
    "points",
    "safe mode",
    "saving",
    "scripting",
    "selection",
    "space center",
    "spacing",
    "subscriber",
    "tabular figures",
    "text",
    "transform",
    "unicode",
    "user interface",
    "vanilla",
    "versioning",
    "QA",
    "mastering",
    "variable fonts",
    "graphics",
    "features",
    "rtl",
    "bidirectional",
    "masters",
    "similarity",
    "workspace",
    "design helpers",
    "unicodes",
    "font info"
}

convert = {
    "debugging": "scripting",
    "glyph names": "glyphs",
    "glyphconstruction": "components",
    "character set": "glyph set",
    "interface": "user interface",
    "workflow": "font generation",
    "consistency": "QA",
    "revisions": "versioning",
    "scale": "transform",
    "encoding": "unicode",
    "alignment": "guidelines",
    "generating fonts": "font generation",
    "paste": "clipboard",
    "copy": "clipboard",
    "windows": "user interface",
    "mark": "points",
    "effects": "appearance",
    "TrueType": "hinting",
    "pangrams": "text",
    "dimensions": "font dimensions",
    "guideline": "guidelines",
    "guides": "guidelines",
    "languages": "unicode",
    "proofing": "text",
    "margins": "spacing",
    "extreme points": "points",
    "interpolated nudge": "interpolation",
    "mutatormath": "interpolation",
    "drawingtool": "drawing",
    "interface workflow workspace": "user interface",
    "contours drawing": "contours",
    "code": "scripting",
    "glyph cells": "font overview",
    "mark positioning": "anchors",
    "anchor": "anchors",
    "accent": "accents",
    "unicode glyph names": "unicodes",
    "OpenType features": "features",
    "glyph": "glyphs",
    "window": "user interface",
    "bidrectional": "bidirectional",
    "variablefont": "variable fonts",
    "preview": "glyph editor",
    "glyph view": "glyph editor",
    "debugging": "QA",
    "fontgadgets": "tools",
}


def read_yaml_file(file_path):
    encodings = ['utf-8', 'latin-1', 'ascii']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return yaml.safe_load(f)
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"Error reading {file_path} with {encoding}: {str(e)}")
            return None
    print(f"Could not read {file_path} with any of the attempted encodings")
    return None

def process_tags(original_tags):
    # Step 1: Remove tags in the remove set
    tags_after_removal = [tag for tag in original_tags if tag.strip() not in remove]
    if tags_after_removal != original_tags:
        # print("\nAfter removing tags:")
        removed = set(original_tags) - set(tags_after_removal)
        # for tag in removed:
        #     print(f"  - Removed: {tag}")
    
    # Step 2: Convert tags according to the convert dictionary
    tags_after_conversion = []
    converted = []
    for tag in tags_after_removal:
        clean_tag = tag.strip()
        if clean_tag in convert:
            new_tag = convert[clean_tag]
            tags_after_conversion.append(new_tag)
            converted.append((tag, new_tag))
        else:
            tags_after_conversion.append(tag)
    
    # if converted:
    #     print("\nAfter converting tags:")
    #     for old, new in converted:
    #         print(f"  - Converted: {old} → {new}")
    #     print(f"After conversion: {tags_after_conversion}")
    
    # Step 3: Remove tags not in ALLOWED_TAGS
    final_tags = [tag for tag in tags_after_conversion if tag in ALLOWED_TAGS]
    if final_tags != tags_after_conversion:
        # print("\nAfter filtering to allowed tags:")
        removed = set(tags_after_conversion) - set(final_tags)
        # for tag in removed:
        #     print(f"  - Removed (not allowed): {tag}")
        # print(f"After filtering: {final_tags}")
    
    # Step 4: Remove duplicates while preserving order
    seen = set()
    deduped_tags = []
    for tag in final_tags:
        if tag not in seen:
            seen.add(tag)
            deduped_tags.append(tag)
    
    if len(deduped_tags) != len(final_tags):
        # print("\nAfter removing duplicates:")
        removed = set(final_tags) - set(deduped_tags)
        # for tag in removed:
        #     print(f"  - Removed duplicate: {tag}")
        # print(f"Final deduped tags: {deduped_tags}")

    if original_tags != deduped_tags:
        print(f"Original tags: {original_tags}")
        print(f"Processed tags: {deduped_tags}")
    if not deduped_tags:
        print("⚠️⚠️⚠️⚠️⚠️")
    
    return deduped_tags

def analyze_tags(yaml_file):
    try:
        data = read_yaml_file(yaml_file)
        if data is None:
            return False
            
        if 'tags' in data:
            original_tags = data['tags']
            if not original_tags:  # Skip empty tag lists
                return False
                
            print(f"\n{'='*50}")
            print(f"Processing file: {yaml_file.name}")
            final_tags = process_tags(original_tags)
            
            if set(original_tags) != set(final_tags):
                # Write changes back to file
                with open(yaml_file, 'w', encoding='utf-8') as file:
                    data['tags'] = final_tags
                    yaml.dump(data, file, default_flow_style=False, sort_keys=False, allow_unicode=True)
                print(f"Changes written back to {yaml_file.name}")
                return True
                
    except Exception as e:
        print(f"Error processing {yaml_file}: {str(e)}")
    return False

def main():
    data_dir = Path('_data')
    modified_count = 0
    
    # Process all YAML files in the _data directory
    for yaml_file in data_dir.glob('*.yml'):
        if analyze_tags(yaml_file):
            modified_count += 1
    
    print(f"\nAnalyzed {modified_count} files with modified tags")

if __name__ == "__main__":
    main() 
    main() 