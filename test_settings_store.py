#!/usr/bin/env python3
"""Test script for the persistent settings store (default toggle states)"""

import os
import shutil
import tempfile

from settings_store import SettingsStore


def test_fresh_store_defaults():
    """A brand-new store should default both toggles to off"""
    tmp_dir = tempfile.mkdtemp()
    try:
        store = SettingsStore(path=os.path.join(tmp_dir, "settings.json"))
        assert not store.get_auto_shift_default()
        assert not store.get_smart_delete_default()
        print("[ok] Fresh store defaults to auto-shift and smart delete off")
    finally:
        shutil.rmtree(tmp_dir)


def test_set_and_get_defaults():
    """Setting a default should be reflected immediately"""
    tmp_dir = tempfile.mkdtemp()
    try:
        store = SettingsStore(path=os.path.join(tmp_dir, "settings.json"))
        store.set_auto_shift_default(True)
        assert store.get_auto_shift_default()
        assert not store.get_smart_delete_default()

        store.set_smart_delete_default(True)
        assert store.get_smart_delete_default()

        store.set_auto_shift_default(False)
        assert not store.get_auto_shift_default()
        assert store.get_smart_delete_default(), "Setting one default shouldn't affect the other"
        print("[ok] Setting defaults updates each toggle independently")
    finally:
        shutil.rmtree(tmp_dir)


def test_persistence_round_trip():
    """Settings should survive being reloaded from disk"""
    tmp_dir = tempfile.mkdtemp()
    try:
        path = os.path.join(tmp_dir, "settings.json")
        store = SettingsStore(path=path)
        store.set_auto_shift_default(True)
        store.set_smart_delete_default(True)

        reloaded = SettingsStore(path=path)
        assert reloaded.get_auto_shift_default()
        assert reloaded.get_smart_delete_default()
        print("[ok] Settings persist across a save/load round trip")
    finally:
        shutil.rmtree(tmp_dir)


def test_corrupt_file_falls_back_to_defaults():
    """A corrupt settings file should not crash the store"""
    tmp_dir = tempfile.mkdtemp()
    try:
        path = os.path.join(tmp_dir, "settings.json")
        with open(path, "w", encoding="utf-8") as f:
            f.write("{not valid json")

        store = SettingsStore(path=path)
        assert not store.get_auto_shift_default()
        assert not store.get_smart_delete_default()
        print("[ok] Corrupt settings file falls back to defaults")
    finally:
        shutil.rmtree(tmp_dir)


def main():
    print("=" * 60)
    print("Testing Virtual Taylor Frame Settings Store")
    print("=" * 60)

    try:
        test_fresh_store_defaults()
        test_set_and_get_defaults()
        test_persistence_round_trip()
        test_corrupt_file_falls_back_to_defaults()

        print("\n" + "=" * 60)
        print("ALL TESTS PASSED!")
        print("=" * 60)

    except AssertionError as e:
        print(f"\nTEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
