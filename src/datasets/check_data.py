import torch
import os

# Use one of the files from your 'ls' output
file_path = "/home/kluitel/HEPT/data/tracking/raw/tracking-acts/data15_s0.pt"

data = torch.load(file_path, map_location='cpu')

print("--- Data Object Structure ---")
print(data)

print("\n--- Tensor Shapes ---")
if hasattr(data, 'x'):
    print(f"Node features (x) shape: {data.x.shape}")
if hasattr(data, 'y'):
    print(f"Label (y): {data.y}")
if hasattr(data, 'particle_id'):
    print(f"Particle IDs shape: {data.particle_id.shape}")

# Look at the first hit to see the scale of the values
print("\n--- First Hit Features (x[0]) ---")
print(data.x[0])