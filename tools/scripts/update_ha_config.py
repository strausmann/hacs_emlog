#!/usr/bin/env python3
"""
Dynamic configuration generator for Home Assistant in Codespaces.
Updates external_url based on environment.
"""

import os
import re
import sys
from pathlib import Path


def main():
    """Main execution."""
    script_dir = Path(__file__).parent.parent.parent
    config_path = script_dir / "tests" / "config" / "configuration.yaml"
    
    # Determine external URL
    if os.getenv("CODESPACES") == "true":
        codespace_name = os.getenv("CODESPACE_NAME")
        forwarding_domain = os.getenv("GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN")
        
        if codespace_name and forwarding_domain:
            external_url = f"https://{codespace_name}-8123.{forwarding_domain}"
            is_codespaces = True
        else:
            external_url = "http://localhost:8123"
            is_codespaces = False
    else:
        external_url = "http://localhost:8123"
        is_codespaces = False
    
    # Update configuration.yaml
    if not config_path.exists():
        print(f"✗ Configuration file not found: {config_path}")
        return 1
    
    with open(config_path, 'r') as f:
        content = f.read()
    
    # Update external_url
    external_pattern = r'(external_url:) "[^"]+"'
    new_content = re.sub(external_pattern, rf'\1 "{external_url}"', content)
    
    with open(config_path, 'w') as f:
        f.write(new_content)
    
    # Display results
    print("🔧 Home Assistant Configuration Update\n")
    print("=" * 50)
    
    if is_codespaces:
        print(f"🔍 Codespaces Environment Detected")
        print(f"   Codespace: {os.getenv('CODESPACE_NAME')}")
        print(f"   Domain: {os.getenv('GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN')}")
    else:
        print(f"🏠 Local Development Environment")
    
    print(f"   External URL: {external_url}\n")
    print("=" * 50)
    print("\n✓ Configuration updated")
    print(f"\n📍 Home Assistant accessible at:")
    print(f"   {external_url}")
    print(f"\n💡 For integration setup, use:")
    print(f"   python3 setup_integration_auto.py --all")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
