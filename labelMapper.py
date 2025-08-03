import json
import pandas as pd
import os

class LabelMapper:
    def __init__(self, label_hierarchy):
        self.label_hierarchy = label_hierarchy
        self._build_mapping_structures()
    
    def _build_mapping_structures(self):
        """Build efficient lookup structures from the hierarchy"""
        self.label_to_parent = {}
        self.exact_matches = {}
        self.patterns = {}
        self.keywords = {}
        
        for _, row in self.label_hierarchy.iterrows():
            label_name = row['Label']
            parent = row['Parent']
            
            if pd.notna(parent):
                self.label_to_parent[label_name] = parent
            
            if pd.notna(row.get('ExactMatches')):
                for exact in str(row['ExactMatches']).split(','):
                    self.exact_matches[exact.strip().lower()] = label_name
            
            if pd.notna(row.get('Patterns')):
                for pattern in str(row['Patterns']).split(','):
                    self.patterns[pattern.strip().lower()] = label_name
            
            if pd.notna(row.get('Keywords')):
                for keyword in str(row['Keywords']).split(','):
                    self.keywords[keyword.strip().lower()] = label_name
    
    def _find_root_parent(self, label_name):
        """Find the root parent (level 0) for a label"""
        if label_name not in self.label_to_parent:
            return label_name
        
        current = label_name
        while current in self.label_to_parent:
            current = self.label_to_parent[current]
        
        return current
    
    def _match_single_label(self, raw_label):
        """Match a single raw label string to its proper label"""
        if not raw_label or pd.isna(raw_label) or raw_label == "Unknown":
            return "Other"
        
        normalized = raw_label.lower().strip()
        
        # 1. Check exact matches first
        if normalized in self.exact_matches:
            matched_label = self.exact_matches[normalized]
            return self._find_root_parent(matched_label)
        
        # 2. Check patterns (partial matches)
        for pattern, label_name in self.patterns.items():
            if pattern in normalized:
                return self._find_root_parent(label_name)
        
        # 3. Check keywords (looser matches)
        for keyword, label_name in self.keywords.items():
            if keyword in normalized:
                return self._find_root_parent(label_name)
        
        # 4. Try to find the most specific label that matches
        parts = [p for p in normalized.split() if len(p) > 3]
        
        for part in parts:
            for label_name in self.label_to_parent:
                if part in label_name.lower():
                    return self._find_root_parent(label_name)
            
            for pattern, label_name in self.patterns.items():
                if part in pattern:
                    return self._find_root_parent(label_name)
        
        return "Other"
    
    def match_label(self, raw_label):
        """Match a raw label string to its proper label hierarchy, handles multiple labels"""
        if not raw_label or pd.isna(raw_label) or raw_label == "Unknown":
            return ["Other"]
        
        # Split the raw label by common separators
        separators = ["/", "&", " and ", "+"]
        label_parts = [raw_label]
        
        for separator in separators:
            new_parts = []
            for part in label_parts:
                new_parts.extend([p.strip() for p in part.split(separator) if p.strip()])
            label_parts = new_parts
        
        # Match each individual label
        matched_labels = [self._match_single_label(part) for part in label_parts]
        
        # Filter out "Other" if there's at least one major label
        non_other_labels = [label for label in matched_labels if label != "Other"]
        
        if non_other_labels:
            # Return unique non-other labels (remove duplicates)
            return list(set(non_other_labels))
        else:
            # If all labels mapped to "Other", return ["Other"]
            return ["Other"]

def process_labels(spotify_json, labels_csv, output_json):
    """Process data and map labels, preserving all original data while adding label mappings"""
    # Read the CSV file for label mapping
    print(f"Reading labels from CSV file: {labels_csv}")
    
    label_hierarchy = pd.read_csv(labels_csv)
    print(f"Successfully loaded label hierarchy with {len(label_hierarchy)} entries")
    
    # Initialize label mapper
    label_mapper = LabelMapper(label_hierarchy)
    
    # Load original data
    print(f"Loading data from: {spotify_json}")
    with open(spotify_json, 'r') as f:
        spotify_data = json.load(f)
    
    # Process each entry in the original data, adding mapped label information
    processed_data = []
    for entry in spotify_data:
        # Clone the original entry
        processed_entry = entry.copy()
        
        # Get the raw label and add the mapped major labels
        raw_label = entry.get("label", "")
        major_labels = label_mapper.match_label(raw_label)
        processed_entry["major_labels"] = major_labels  # Store as list of labels
        
        # Optionally add the artist genre as a field
        artist_genre = entry.get("artist_genre", "")
        processed_entry["artist_genre"] = artist_genre
        
        processed_data.append(processed_entry)
    
    # Create a separate metadata object with simple statistics
    metadata = {
        "total_entries": len(processed_data)
    }
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_json)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    # Save the processed data
    with open(output_json, 'w') as f:
        json.dump({
            "metadata": metadata,
            "data": processed_data
        }, f, indent=2)
    
    print(f"Processed {len(processed_data)} entries")
    print(f"Saved processed data to {output_json}")
    
    return processed_data, metadata

if __name__ == "__main__":
    # Process data and save to JSON
    process_labels(
        spotify_json='data/latest_albums_details.json',  # Input file
        labels_csv='labelshierarchystuffrelated/label_hierarchy.csv',  # Label hierarchy CSV file
        output_json='data/latest_albums_details_labels_normalized.json'  # Output file
    )
