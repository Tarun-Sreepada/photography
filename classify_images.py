import os
import json
import torch
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

def generate_labels():
    thumbs_dir = os.path.join('images', 'thumbs')
    output_file = 'image_labels.json'
    
    if not os.path.exists(thumbs_dir):
        print(f"Directory not found: {thumbs_dir}")
        return

    print("Loading image captioning model (Salesforce/blip-image-captioning-large)...")
    print("This might take a moment to download dependencies on the first run.")
    
    try:
        model_name = "Salesforce/blip-image-captioning-large"
        processor = BlipProcessor.from_pretrained(model_name)
        model = BlipForConditionalGeneration.from_pretrained(model_name)
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    # Use GPU if available (MPS for Mac, CUDA for Nvidia, CPU otherwise)
    if torch.backends.mps.is_available():
        device = torch.device("mps")
    elif torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")
        
    model.to(device)
    print(f"Model loaded. Using device: {device}")

    # Helper function for prediction
    def predict_caption(image_path):
        try:
            i_image = Image.open(image_path)
            if i_image.mode != "RGB":
                i_image = i_image.convert(mode="RGB")

            inputs = processor(images=i_image, return_tensors="pt").to(device)

            out = model.generate(**inputs, max_new_tokens=50) # Increased token limit for better descriptions
            caption = processor.decode(out[0], skip_special_tokens=True)
            return caption
        except Exception as e:
            # print(f"Error predicting for {image_path}: {e}")
            return None

    results = {}
    
    files = [f for f in os.listdir(thumbs_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.heic'))]
    files.sort()
    
    print(f"Found {len(files)} images to process in {thumbs_dir}")
    print("Starting classification...")
    
    for i, filename in enumerate(files):
        file_path = os.path.join(thumbs_dir, filename)
        
        if filename.lower().endswith('.heic'):
            print(f"[{i+1}/{len(files)}] Skipping HEIC: {filename}")
            continue

        caption = predict_caption(file_path)
        if caption:
            print(f"[{i+1}/{len(files)}] {filename} -> {caption}")
            results[filename] = caption
        else:
            print(f"[{i+1}/{len(files)}] Failed to caption: {filename}")
            
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
        
    print(f"\nProcessing complete. Labels saved to {output_file}")

if __name__ == "__main__":
    generate_labels()
