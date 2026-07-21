#!/usr/bin/env python3
"""Test script for the persistent progress store / unlock system"""

import os
import shutil
import tempfile

from progress_store import ProgressStore


def test_fresh_store_defaults():
    """A brand-new store should report nothing completed and no stars"""
    tmp_dir = tempfile.mkdtemp()
    try:
        store = ProgressStore(path=os.path.join(tmp_dir, "progress.json"))
        assert not store.is_completed("easy_addition")
        assert store.get_best_stars("easy_addition") == 0
        print("✓ Fresh store defaults to nothing completed")
    finally:
        shutil.rmtree(tmp_dir)


def test_record_completion_and_best_stars():
    """Best stars should track the highest score across repeated plays"""
    tmp_dir = tempfile.mkdtemp()
    try:
        store = ProgressStore(path=os.path.join(tmp_dir, "progress.json"))
        store.record_completion("easy_addition", 2)
        assert store.is_completed("easy_addition")
        assert store.get_best_stars("easy_addition") == 2

        # A worse replay should not lower the recorded best
        store.record_completion("easy_addition", 1)
        assert store.get_best_stars("easy_addition") == 2

        # A better replay should raise it
        store.record_completion("easy_addition", 3)
        assert store.get_best_stars("easy_addition") == 3
        print("✓ Best stars tracks the highest score across replays")
    finally:
        shutil.rmtree(tmp_dir)


def test_persistence_round_trip():
    """Progress should survive being reloaded from disk"""
    tmp_dir = tempfile.mkdtemp()
    try:
        path = os.path.join(tmp_dir, "progress.json")
        store = ProgressStore(path=path)
        store.record_completion("easy_addition", 3)

        reloaded = ProgressStore(path=path)
        assert reloaded.is_completed("easy_addition")
        assert reloaded.get_best_stars("easy_addition") == 3
        print("✓ Progress persists across a save/load round trip")
    finally:
        shutil.rmtree(tmp_dir)


def test_corrupt_file_falls_back_to_empty():
    """A corrupt progress file should not crash the store"""
    tmp_dir = tempfile.mkdtemp()
    try:
        path = os.path.join(tmp_dir, "progress.json")
        with open(path, "w", encoding="utf-8") as f:
            f.write("{not valid json")

        store = ProgressStore(path=path)
        assert not store.is_completed("easy_addition")
        print("✓ Corrupt progress file falls back to a fresh empty state")
    finally:
        shutil.rmtree(tmp_dir)


def test_unlock_progression():
    """Only the first tutorial starts unlocked; each next one needs the prior completed"""
    tmp_dir = tempfile.mkdtemp()
    try:
        order = ["easy_addition", "easy_subtraction", "easy_multiplication"]
        store = ProgressStore(path=os.path.join(tmp_dir, "progress.json"))

        assert store.is_unlocked("easy_addition", order), "First tutorial should always be unlocked"
        assert not store.is_unlocked("easy_subtraction", order), "Second should be locked initially"
        assert not store.is_unlocked("easy_multiplication", order), "Third should be locked initially"

        store.record_completion("easy_addition", 1)
        assert store.is_unlocked("easy_subtraction", order), "Second unlocks once first is completed"
        assert not store.is_unlocked("easy_multiplication", order), "Third still locked"

        store.record_completion("easy_subtraction", 2)
        assert store.is_unlocked("easy_multiplication", order), "Third unlocks once second is completed"

        print("✓ Locked progression unlocks tutorials sequentially")
    finally:
        shutil.rmtree(tmp_dir)


def test_total_stars_and_completed_count():
    """Aggregate helpers should sum/count correctly across tutorials"""
    tmp_dir = tempfile.mkdtemp()
    try:
        order = ["easy_addition", "easy_subtraction", "easy_multiplication"]
        store = ProgressStore(path=os.path.join(tmp_dir, "progress.json"))
        store.record_completion("easy_addition", 3)
        store.record_completion("easy_subtraction", 2)

        assert store.total_stars(order) == 5
        assert store.completed_count(order) == 2
        print("✓ total_stars and completed_count aggregate correctly")
    finally:
        shutil.rmtree(tmp_dir)


def main():
    print("=" * 60)
    print("Testing Virtual Taylor Frame Progress Store")
    print("=" * 60)

    try:
        test_fresh_store_defaults()
        test_record_completion_and_best_stars()
        test_persistence_round_trip()
        test_corrupt_file_falls_back_to_empty()
        test_unlock_progression()
        test_total_stars_and_completed_count()

        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED!")
        print("=" * 60)

    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
