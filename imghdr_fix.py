"""
Custom imghdr module replacement for Python 3.13+
This provides the basic functionality needed by lama-cleaner
"""

import os
import struct

def what(file, h=None):
    """Recognize image file formats based on their first few bytes."""
    if h is None:
        if isinstance(file, str):
            f = open(file, 'rb')
            h = f.read(32)
            f.close()
        else:
            location = file.tell()
            h = file.read(32)
            file.seek(location)
            if not h:
                return None
    
    if len(h) >= 2:
        if h[:2] == b'\xff\xd8':
            return 'jpeg'
    
    if len(h) >= 8:
        if h[:8] == b'\x89PNG\r\n\x1a\n':
            return 'png'
    
    if len(h) >= 6:
        if h[:6] in (b'GIF87a', b'GIF89a'):
            return 'gif'
    
    if len(h) >= 2:
        if h[:2] == b'BM':
            return 'bmp'
    
    if len(h) >= 4:
        if h[:4] == b'RIFF' and h[8:12] == b'WEBP':
            return 'webp'
    
    if len(h) >= 4:
        if h[:4] == b'\x00\x00\x01\x00':
            return 'ico'
    
    return None

def tests():
    """Test the module with sample files."""
    test_files = [
        ('test.jpg', b'\xff\xd8\xff\xe0'),
        ('test.png', b'\x89PNG\r\n\x1a\n'),
        ('test.gif', b'GIF87a'),
        ('test.bmp', b'BM'),
    ]
    
    for filename, header in test_files:
        result = what(filename, header)
        print(f"{filename}: {result}")

if __name__ == '__main__':
    tests()
