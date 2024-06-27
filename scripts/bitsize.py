import torch

# Load the file containing PyTorch tensors
file_path = "assets\cache\MetaTestset_1/blur-2\ViT.pt"
tensors = torch.load(file_path)

# Assuming the file contains a single tensor
tensor = tensors[0]

# Get the data type of the tensor
data_type = tensor.dtype

# Get the number of bits for the data type
num_bits = torch.finfo(data_type).bits

# Get the size of the tensor in bits
tensor_size_bits = tensor.numel() * num_bits

print("Number of bits per element:", num_bits)
print("Number of bits for the entire tensor:", tensor_size_bits)