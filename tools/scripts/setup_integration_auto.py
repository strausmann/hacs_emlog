#!/usr/bin/env python3
"""
Automatic Home Assistant integration setup for Emlog development.
Configures HACS and Emlog integrations without manual UI steps.
"""

import json
import os
import sys
import uuid
from pathlib import Path
from typing import Dict


class HAIntegrationSetup:
    """Setup Home Assistant integrations automatically."""
    
    def __init__(self, config_dir: Path = None):
        """Initialize with HA config directory."""
        if config_dir is None:
            config_dir = Path(__file__).parent / "test_config"
        self.config_dir = config_dir
        self.storage_dir = config_dir / ".storage"
        self.config_entries_file = self.storage_dir / "core.config_entries"
    
    def load_config_entries(self) -> Dict:
        """Load config entries from storage."""
        if not self.config_entries_file.exists():
            return {
                "version": 1,
                "minor_version": 2,
                "key": "core.config_entries",
                "data": {"entries": []}
            }
        
        try:
            with open(self.config_entries_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Error reading config entries: {e}", file=sys.stderr)
            return {
                "version": 1,
                "minor_version": 2,
                "key": "core.config_entries",
                "data": {"entries": []}
            }
    
    def save_config_entries(self, data: Dict) -> bool:
        """Save config entries to storage."""
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        try:
            with open(self.config_entries_file, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"✗ Error saving config entries: {e}")
            return False
    
    def integration_exists(self, domain: str) -> bool:
        """Check if integration already exists."""
        data = self.load_config_entries()
        for entry in data.get("data", {}).get("entries", []):
            if entry.get("domain") == domain:
                return True
        return False
    
    def add_hacs(self) -> bool:
        """Add HACS integration."""
        if self.integration_exists("hacs"):
            print("ℹ️  HACS already configured")
            return True
        
        data = self.load_config_entries()
        
        
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc).isoformat()
        
        hacs_entry = {
            "created_at": now,
            "data": {},
            "disabled_by": None,
            "discovery_keys": {},
            "domain": "hacs",
            "entry_id": str(uuid.uuid4()),
            "minor_version": 3,
            "modified_at": now,
            "options": {},
            "pref_disable_new_entities": False,
            "pref_disable_polling": False,
            "source": "integration_discovery",
            "subentries": [],
            "title": "HACS",
            "unique_id": None,
            "version": 6
        }
        data["data"]["entries"].append(hacs_entry)
        
        if self.save_config_entries(data):
            print("✓ HACS integration added")
            return True
        return False
    
    def add_emlog(self, host: str = "emlog-mock", 
                  strom_index: int = 1, 
                  gas_index: int = 2,
                  scan_interval: int = 30) -> bool:
        """Add Emlog integration."""
        if self.integration_exists("emlog"):
            print("ℹ️  Emlog already configured")
            return True
        
        data = self.load_config_entries()
        
        
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc).isoformat()
        
        emlog_entry = {
            "created_at": now,
            "data": {
                "host": host,
                "strom_index": strom_index,
                "gas_index": gas_index,
                "scan_interval": scan_interval
            },
            "disabled_by": None,
            "discovery_keys": {},
            "domain": "emlog",
            "entry_id": str(uuid.uuid4()),
            "minor_version": 1,
            "modified_at": now,
            "options": {},
            "pref_disable_new_entities": False,
            "pref_disable_polling": False,
            "source": "user",
            "subentries": [],
            "title": f"Emlog ({host})",
            "unique_id": host,
            "version": 1
        }
        data["data"]["entries"].append(emlog_entry)
        
        if self.save_config_entries(data):
            print(f"✓ Emlog integration added (host={host})")
            return True
        return False


def main():
    """Main execution."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Automatically setup Home Assistant integrations"
    )
    parser.add_argument("--hacs", action="store_true", help="Setup HACS")
    parser.add_argument("--emlog", action="store_true", help="Setup Emlog")
    parser.add_argument("--all", action="store_true", help="Setup all (HACS + Emlog)")
    parser.add_argument("--host", default="emlog-mock", help="Emlog host")
    
    args = parser.parse_args()
    
    setup = HAIntegrationSetup()
    
    print("🔌 Home Assistant Integration Setup\n")
    print("=" * 50)
    
    success = True
    
    if args.all or args.hacs:
        print("\n📦 Setting up HACS...")
        if not setup.add_hacs():
            success = False
    
    if args.all or args.emlog:
        print("\n⚡ Setting up Emlog...")
        if not setup.add_emlog(host=args.host):
            success = False
    
    if not (args.hacs or args.emlog or args.all):
        print("Usage: python3 setup_integration_auto.py --all")
        print("  or:  python3 setup_integration_auto.py --hacs --emlog")
        return 1
    
    print("\n" + "=" * 50)
    if success:
        print("✅ Integration setup complete!\n")
        print("💡 Integrations configured:")
        if args.all or args.hacs:
            print("   ✓ HACS (Community Store)")
        if args.all or args.emlog:
            print("   ✓ Emlog (Energy Meter)")
        print("\n⚠️  Note: HA requires restart for changes to take effect")
        print("   Run: docker-compose -f tools/docker/compose.yml restart homeassistant")
        return 0
    else:
        print("✗ Setup failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
