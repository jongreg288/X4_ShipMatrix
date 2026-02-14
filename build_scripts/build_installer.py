#!/usr/bin/env python3
"""
Build script for X4 ShipMatrix installer
Compiles the Inno Setup script to create Setup.exe
"""

import subprocess
import sys
from pathlib import Path
import os
import shutil

def find_inno_setup():
    """Find the Inno Setup compiler (ISCC.exe)."""
    # First try PATH
    iscc_from_path = shutil.which("ISCC.exe") or shutil.which("iscc")
    if iscc_from_path:
        return iscc_from_path

    # Common installation paths
    possible_paths = [
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 6\ISCC.exe",
        r"C:\Program Files (x86)\Inno Setup 5\ISCC.exe",
        r"C:\Program Files\Inno Setup 5\ISCC.exe",
        str(Path.home() / "AppData" / "Local" / "Programs" / "Inno Setup 6" / "ISCC.exe"),
        str(Path.home() / "AppData" / "Local" / "Programs" / "Inno Setup 5" / "ISCC.exe"),
    ]
    
    for path in possible_paths:
        if Path(path).exists():
            return path
    
    return None

def main():
    """Build the installer using Inno Setup."""
    print("Building X4 ShipMatrix Installer...")
    print("=" * 50)
    
    # Find Inno Setup compiler
    iscc_path = find_inno_setup()
    
    if not iscc_path:
        print("Inno Setup not found!")
        print("\nPlease install Inno Setup from:")
        print("   https://jrsoftware.org/isdl.php")
        print("\nAfter installation, run this script again.")
        return 1
    
    print(f"Found Inno Setup: {iscc_path}")
    
    # Get script paths
    build_scripts_dir = Path(__file__).parent
    iss_script = build_scripts_dir / "X4_ShipMatrix_Setup.iss"
    
    if not iss_script.exists():
        print(f"Installer script not found: {iss_script}")
        return 1
    
    print(f"Found installer script: {iss_script}")
    
    # Ensure output directory exists
    output_dir = build_scripts_dir.parent / "releases" / "latest"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Compile the installer
    print("\nCompiling installer...")
    try:
        result = subprocess.run(
            [iscc_path, str(iss_script)],
            capture_output=True,
            text=True,
            check=True,
            cwd=build_scripts_dir
        )
        
        print(result.stdout)
        
        # Find the generated installer
        installer_files = list(output_dir.glob("X4_ShipMatrix_v*_Setup.exe"))
        
        if installer_files:
            installer = installer_files[0]
            size_mb = installer.stat().st_size / (1024 * 1024)
            
            print("\n" + "=" * 50)
            print("Installer built successfully!")
            print("=" * 50)
            print(f"File: {installer.name}")
            print(f"Size: {size_mb:.1f} MB")
            print(f"Location: {installer}")
            print("\nYou can now distribute this single file to users!")
            
        else:
            print("Installer was compiled but output file not found")
            print(f"   Expected in: {output_dir}")
            
    except subprocess.CalledProcessError as e:
        print(f"\nBuild failed!")
        print(f"Error: {e.stderr}")
        return 1
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
