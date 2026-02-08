import os
from PIL import Image

thumbs_dir = os.path.join('images', 'thumbs')
quality = 50  # Compression quality (0-100)

success_count = 0
skip_count = 0
error_count = 0

print(f"Compressing images in {thumbs_dir} with quality={quality}...")

for filename in os.listdir(thumbs_dir):
    full_path = os.path.join(thumbs_dir, filename)
    
    if not os.path.isfile(full_path):
        continue
        
    lower_name = filename.lower()
    if lower_name.endswith(('.jpg', '.jpeg', '.png')):
        try:
            with Image.open(full_path) as img:
                # Extract EXIF data to preserve metadata/rotation
                exif_data = img.info.get("exif")

                original_size = os.path.getsize(full_path)
                
                save_kwargs = {'optimize': True, 'quality': quality}
                if exif_data:
                    save_kwargs['exif'] = exif_data

                
                img.save(full_path, **save_kwargs)

                new_size = os.path.getsize(full_path)
                reduction = original_size - new_size
                reduction_pct = (reduction / original_size) * 100 if original_size > 0 else 0

                print(f"Compressed: {filename} | "
                      f"Original: {original_size / 1024:.2f} KB | "
                      f"New: {new_size / 1024:.2f} KB | "
                      f"Reduction: {reduction / 1024:.2f} KB ({reduction_pct:.2f}%)")
                success_count += 1
        except Exception as e:
            print(f"Error compressing {filename}: {e}")
            error_count += 1
    else:
        print(f"Skipping (unsupported format): {filename}")
        skip_count += 1

print("-" * 30)
print(f"Finished.")
print(f"Compressed: {success_count}")
print(f"Skipped: {skip_count}")
print(f"Errors: {error_count}")
