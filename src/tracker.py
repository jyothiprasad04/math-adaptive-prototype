from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict
from enum import Enum

@dataclass
class PerformanceRecord:
    """Record of a single attempt"""
    puzzle_id: int
    difficulty: str
    correct: bool
    time_taken: float  # in seconds
    user_answer: int
    correct_answer: int
    timestamp: datetime = field(default_factory=datetime.now)
    
    @property
    def is_correct(self) -> bool:
        return self.correct

class PerformanceTracker:
    """Tracks and analyzes user performance"""
    
    def __init__(self, user_name: str):
        self.user_name = user_name
        self.records: List[PerformanceRecord] = []
        self.session_start = datetime.now()
    
    def log_attempt(self, puzzle_id: int, difficulty: str, correct: bool, 
                   time_taken: float, user_answer: int, correct_answer: int) -> None:
        """Log a single puzzle attempt"""
        record = PerformanceRecord(
            puzzle_id=puzzle_id,
            difficulty=difficulty,
            correct=correct,
            time_taken=time_taken,
            user_answer=user_answer,
            correct_answer=correct_answer
        )
        self.records.append(record)
    
    def get_accuracy(self, recent_n: int = None) -> float:
        """
        Calculate accuracy percentage.
        If recent_n is specified, calculate only for last N attempts.
        """
        if not self.records:
            return 0.0
        
        records = self.records[-recent_n:] if recent_n else self.records
        correct_count = sum(1 for r in records if r.correct)
        return (correct_count / len(records)) * 100
    
    def get_average_time(self, recent_n: int = None) -> float:
        """Get average time per puzzle (in seconds)"""
        if not self.records:
            return 0.0
        
        records = self.records[-recent_n:] if recent_n else self.records
        total_time = sum(r.time_taken for r in records)
        return total_time / len(records)
    
    def get_difficulty_stats(self) -> Dict:
        """Get statistics broken down by difficulty level"""
        stats = {}
        for difficulty in ['EASY', 'MEDIUM', 'HARD']:
            records = [r for r in self.records if r.difficulty == difficulty]
            if records:
                correct = sum(1 for r in records if r.correct)
                avg_time = sum(r.time_taken for r in records) / len(records)
                stats[difficulty] = {
                    'attempts': len(records),
                    'accuracy': (correct / len(records)) * 100,
                    'avg_time': avg_time
                }
        return stats
    
    def get_performance_trend(self, window_size: int = 5) -> List[bool]:
        """Get recent performance trend (last window_size attempts)"""
        return [r.correct for r in self.records[-window_size:]]
    
    def get_session_duration(self) -> float:
        """Get session duration in seconds"""
        return (datetime.now() - self.session_start).total_seconds()
    
    def get_session_summary(self) -> Dict:
        """Generate complete session summary"""
        return {
            'user_name': self.user_name,
            'total_puzzles': len(self.records),
            'overall_accuracy': self.get_accuracy(),
            'average_time_per_puzzle': self.get_average_time(),
            'session_duration_seconds': self.get_session_duration(),
            'difficulty_stats': self.get_difficulty_stats(),
            'recent_trend': self.get_performance_trend(),
            'total_correct': sum(1 for r in self.records if r.correct)
        }
