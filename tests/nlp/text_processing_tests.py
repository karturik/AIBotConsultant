import sys
import os
import asyncio
import pytest

# Add src directory to Python path
HOME_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src'))
print(HOME_DIR)
sys.path.append(HOME_DIR)

from nlp.utils.text_processor import clear_message, rephrase_message
from unittest import TestCase


@pytest.mark.asyncio
async def test_clear_message():
    # Arrange
    test_message = "Привет, черный тилефон с сильной батареяй"
    
    # Act
    result = await clear_message(test_message)
    print('\nReal processing:')
    print('Input message:', test_message)
    print('Clear message:', result)
    
    # Assert
    assert isinstance(result, str)
    assert len(result) > 0

@pytest.mark.asyncio
async def test_rephrase_message():
    # Arrange
    test_message = "Привет, черный телефон с мощной батареей"
    
    # Act
    result = await rephrase_message(test_message)
    print('\nReal processing:')
    print('Input message:', test_message)
    print('Rephrase messages:', result)
    
    # Assert
    assert isinstance(result, str)
    assert len(result) > 0
