"""Device and GPU detection utilities for cross-platform compatibility."""

import platform
import sys
from typing import Tuple, Literal

DeviceType = Literal["mps", "cuda", "cpu"]


def detect_device() -> Tuple[DeviceType, str]:
    """
    Detect the best available device for PyTorch operations.
    
    Returns:
        Tuple of (device_type, device_description)
        - "mps": Apple Silicon GPU (Mac M1/M2/M3/M4)
        - "cuda": NVIDIA GPU (Windows/Linux)
        - "cpu": Fallback CPU processing
    """
    system = platform.system()
    
    # Check for Apple Silicon (MPS)
    if system == "Darwin":  # macOS
        try:
            import torch
            if torch.backends.mps.is_available():
                return ("mps", "Apple Silicon GPU (MPS)")
        except (ImportError, AttributeError):
            pass
    
    # Check for NVIDIA CUDA (Windows/Linux)
    try:
        import torch
        if torch.cuda.is_available():
            device_name = torch.cuda.get_device_name(0)
            return ("cuda", f"NVIDIA GPU: {device_name}")
    except (ImportError, AttributeError):
        pass
    
    # Fallback to CPU
    return ("cpu", "CPU (No GPU acceleration)")


def get_torch_device() -> str:
    """
    Get PyTorch device string for model placement.
    
    Returns:
        Device string: "mps", "cuda", or "cpu"
    """
    device_type, _ = detect_device()
    return device_type


def is_mlx_available() -> bool:
    """
    Check if MLX is available (Mac only).
    
    Returns:
        True if MLX can be imported and used
    """
    if platform.system() != "Darwin":
        return False
    
    try:
        import mlx.core as mx
        return True
    except ImportError:
        return False


def print_device_info():
    """Print detailed device information."""
    device_type, device_desc = detect_device()
    
    print("🖥️  System Information:")
    print(f"   OS: {platform.system()} {platform.release()}")
    print(f"   Platform: {platform.machine()}")
    print(f"   Python: {sys.version.split()[0]}")
    print(f"\n🚀 Compute Device:")
    print(f"   Device: {device_desc}")
    print(f"   Type: {device_type}")
    
    # Check MLX availability
    if platform.system() == "Darwin":
        mlx_status = "✅ Available" if is_mlx_available() else "❌ Not installed"
        print(f"   MLX: {mlx_status}")
    
    # Check PyTorch availability
    try:
        import torch
        print(f"   PyTorch: {torch.__version__}")
    except ImportError:
        print("   PyTorch: ❌ Not installed")
    
    print()


def get_optimal_batch_size(device_type: DeviceType) -> int:
    """
    Get optimal batch size based on device.
    
    Args:
        device_type: Type of compute device
        
    Returns:
        Recommended batch size
    """
    if device_type == "mps":
        return 8  # Apple Silicon
    elif device_type == "cuda":
        return 16  # NVIDIA GPU (can be higher)
    else:
        return 4  # CPU (smaller batches)


# Global device detection (cached)
_DEVICE_TYPE: DeviceType | None = None
_DEVICE_DESC: str | None = None


def get_device() -> Tuple[DeviceType, str]:
    """Get cached device information."""
    global _DEVICE_TYPE, _DEVICE_DESC
    if _DEVICE_TYPE is None:
        _DEVICE_TYPE, _DEVICE_DESC = detect_device()
    return _DEVICE_TYPE, _DEVICE_DESC


if __name__ == "__main__":
    # Test device detection
    print_device_info()
    device_type, device_desc = get_device()
    print(f"Optimal batch size: {get_optimal_batch_size(device_type)}")
