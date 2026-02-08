import os

fulls_dir = os.path.join('images', 'fulls')
thumbs_dir = os.path.join('images', 'thumbs')

fulls_files = set(os.listdir(fulls_dir))
thumbs_files = set(os.listdir(thumbs_dir))

# Filter out hidden files (start with .)
fulls_files = {f for f in fulls_files if not f.startswith('.')}
thumbs_files = {f for f in thumbs_files if not f.startswith('.')}

print(f"Total full images: {len(fulls_files)}")
print(f"Total thumb images: {len(thumbs_files)}")

missing_thumbs = fulls_files - thumbs_files
missing_fulls = thumbs_files - fulls_files

if missing_thumbs:
    print("\nImages in 'fulls' but missing in 'thumbs' (exact filename match):")
    for f in sorted(missing_thumbs):
        print(f"  {f}")
else:
    print("\nAll full images have a corresponding thumbnail with the exact same name.")

if missing_fulls:
    print("\nImages in 'thumbs' but missing in 'fulls':")
    for f in sorted(missing_fulls):
        print(f"  {f}")
