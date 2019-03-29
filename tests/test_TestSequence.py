"""
Automated test suite for the Automated Test Environment.  This file focuses
on testing the ``TestSequence`` class.
"""
from time import sleep
import pytest
import ate


@pytest.fixture
def normal_test_sequence():
    class T1(ate.Test):
        def __init__(self):
            super().__init__('test 1')

        def execute(self, is_passing):
            sleep(0.2)
            return None

    class T2(ate.Test):
        def __init__(self):
            super().__init__('test 2')

        def execute(self, is_passing):
            return None

    yield ate.TestSequence(
        sequence=[
            T1(), T2()
        ]
    )


def test_TestSequence_creation(normal_test_sequence):
    ts = normal_test_sequence

    assert ts.in_progress is False


def test_TestSequence_retrieve_by_moniker(normal_test_sequence):
    ts = normal_test_sequence
    test = ts['test 1']
    assert test.moniker == 'test 1'


def test_TestSequence_run(normal_test_sequence):
    ts = normal_test_sequence
    ts.start()

    # wait a small amount of time, ensure that the test sequence has
    # begun and is in progress
    sleep(0.1)
    assert ts.in_progress is True

    while ts.in_progress is True:
        sleep(0.1)

    assert ts.in_progress is False