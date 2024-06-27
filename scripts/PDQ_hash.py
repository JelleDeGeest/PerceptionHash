import numpy as np
from scipy.fftpack import dct
from scipy.ndimage import convolve
from PIL import Image
import base64

def rgb_to_luminance(image):
    """Convert an RGB image to a luminance image."""
    r, g, b = image[:,:,0], image[:,:,1], image[:,:,2]
    return 0.299 * r + 0.587 * g + 0.114 * b

def jarosz_filter(image, radius=1):
    """Apply Jarosz filter with given radius using efficient convolution."""
    kernel = np.ones((radius * 2 + 1,)) / (radius * 2 + 1)
    smoothed = convolve(image, kernel[:, None], mode='mirror')
    smoothed = convolve(smoothed, kernel[None, :], mode='mirror')
    return smoothed

def downsample(image, size=(64, 64)):
    """Downsample the image to the given size using efficient resizing."""
    return np.array(Image.fromarray(image).resize(size, Image.Resampling.LANCZOS))

def apply_dct(image):
    """Apply 2D DCT to the image."""
    return dct(dct(image.T, norm='ortho').T, norm='ortho')

def extract_low_mid_frequencies(dct_coeffs, size=8):
    """Extract the low to mid frequency components."""
    return dct_coeffs[:size, :size]

def generate_hash(dct_coeffs):
    """Generate the hash by comparing to the median value."""
    median_value = np.median(dct_coeffs)
    return (dct_coeffs > median_value).astype(int).flatten()

def hash_to_base64(hash_array):
    """Convert the binary hash array to a Base64 encoded string."""
    # Convert the binary array to a byte string
    byte_string = np.packbits(hash_array).tobytes()
    # Encode the byte string in Base64
    base64_string = base64.b64encode(byte_string).decode('utf-8')
    return base64_string

def pdq_hash(image_path):
    # Load the image
    image = Image.open(image_path).convert('RGB')
    image = np.asarray(image)
    
    # Calculate luminance
    luminance_image = rgb_to_luminance(image)
    
    # Apply Jarosz filter
    smoothed_image = jarosz_filter(luminance_image, radius=1)
    
    # Downsample the image to 64x64
    downsampled_image = downsample(smoothed_image, size=(64, 64))
    
    # Apply DCT
    dct_coeffs = apply_dct(downsampled_image)
    
    # Extract low to mid frequency components
    low_mid_freqs = extract_low_mid_frequencies(dct_coeffs, size=8)
    
    # Generate hash
    hash_array = generate_hash(low_mid_freqs)
    
    # Convert hash to Base64
    base64_hash = hash_to_base64(hash_array)
    
    return base64_hash

# Example usage
image_path = 'assets/test/Similar_image_example_3.png'
base64_hash_value = pdq_hash(image_path)
print(base64_hash_value)