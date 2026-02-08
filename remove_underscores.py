import os

directories = [
    os.path.join('images', 'fulls'),
    os.path.join('images', 'thumbs')
]

count = 0

for directory in directories:
    if not os.path.exists(directory):
        print(f"Directory not found: {directory}")
        continue
        
    print(f"Processing {directory}...")
    for filename in os.listdir(directory):
        if filename.startswith('_'):
            old_path = os.path.join(directory, filename)
            
            # Remove ONLY the leading underscore
            new_filename = filename[1:] 
            new_path = os.path.join(directory, new_filename)
            
            # Check if destination already exists to avoid overwriting (though unlikely given the context, good practice)
            if os.path.exists(new_path):
                print(f"Skipping {filename} -> {new_filename}: Target already exists.")
            else:
                os.rename(old_path, new_path)
                print(f"Renamed: {filename} -> {new_filename}")
                count += 1

print(f"Finished. Renamed {count} files.")
