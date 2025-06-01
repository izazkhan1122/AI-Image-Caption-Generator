from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import requests
import torch

print("Starting...")

try:
    print("Loading processor and model...")
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
except Exception as e:
    print("Error loading model:", e)
    exit()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
print(f"Using device: {device}")

try:
    img_url = "https://storage.googleapis.com/sfr-vision-language-research/BLIP/demo.jpg"
    print(f"Downloading image from {img_url} ...")
    image = Image.open(requests.get(img_url, stream=True).raw).convert('RGB')
except Exception as e:
    print("Error loading image:", e)
    exit()

try:
    print("Processing image...")
    inputs = processor(image, return_tensors="pt").to(device)

    print("Generating caption...")
    out = model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)

    print("📷 Caption:", caption)
except Exception as e:
    print("Error during caption generation:", e)
