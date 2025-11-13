import random
from enum import Enum
from dataclasses import dataclass
from typing import Tuple, Literal

class DifficultyLevel(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3

@dataclass
class MathPuzzle:
    """Represents a single math puzzle"""
    operand1: int
    operand2: int
    operation: str
    correct_answer: int
    difficulty: DifficultyLevel
    
    def __str__(self) -> str:
        return f"{self.operand1} {self.operation} {self.operand2} = ?"

class PuzzleGenerator:
    """Generates math puzzles with progressive difficulty"""
    
    OPERATIONS = ['+', '-', '*', '/']
    DIFFICULTY_CONFIG = {
        DifficultyLevel.EASY: {
            'operand_range': (1, 10),
            'operations': ['+', '-'],
            'allow_decimals': False
        },
        DifficultyLevel.MEDIUM: {
            'operand_range': (5, 50),
            'operations': ['+', '-', '*'],
            'allow_decimals': False
        },
        DifficultyLevel.HARD: {
            'operand_range': (10, 100),
            'operations': ['+', '-', '*', '/'],
            'allow_decimals': True
        }
    }
    
    def __init__(self, seed: int = None):
        if seed is not None:
            random.seed(seed)
    
    def generate_puzzle(self, difficulty: DifficultyLevel) -> MathPuzzle:
        """Generate a single puzzle for the given difficulty level"""
        config = self.DIFFICULTY_CONFIG[difficulty]
        min_op, max_op = config['operand_range']
        
        operand1 = random.randint(min_op, max_op)
        operand2 = random.randint(max(1, min_op // 2), max_op)
        operation = random.choice(config['operations'])
        
        # Calculate correct answer
        if operation == '+':
            correct_answer = operand1 + operand2
        elif operation == '-':
            correct_answer = operand1 - operand2
        elif operation == '*':
            correct_answer = operand1 * operand2
        elif operation == '/':
            # Ensure division results in whole number
            operand2 = max(1, operand1 // (random.randint(2, 5)))
            correct_answer = operand1 // operand2
        
        return MathPuzzle(
            operand1=operand1,
            operand2=operand2,
            operation=operation,
            correct_answer=correct_answer,
            difficulty=difficulty
        )
    
    def generate_batch(self, difficulty: DifficultyLevel, count: int) -> list:
        """Generate multiple puzzles"""
        return [self.generate_puzzle(difficulty) for _ in range(count)]
