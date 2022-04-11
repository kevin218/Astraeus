import pytest
import astreus.example

def test_type():
    """
    Test addition with float, int and strung.
    """
    assert astreus.example.add_one(1) == 2
    assert astreus.example.add_one(1.1) == 2.1
    assert astreus.example.add_one('1') == '11'

def test_error():
    """
    Test addition with list.
    """
    with pytest.raises(TypeError):
        astreus.example.add_one([1])
