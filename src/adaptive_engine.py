import numpy as np
from typing import List
from dataclasses import dataclass, field

@dataclass
class AdaptationConfig:
    """Configuration for adaptive logic"""
    rule_based_thresholds: dict = field(default_factory=lambda: {'high': 75, 'low': 50})
    lookback_window: int = 5
    min_attempts_before_change: int = 3

class AdaptiveEngine:
    """
    Manages difficulty adaptation using rule-based approach
    """
    
    DIFFICULTY_LEVELS = ['EASY', 'MEDIUM', 'HARD']
    DIFFICULTY_MAP = {'EASY': 0, 'MEDIUM': 1, 'HARD': 2}
    REVERSE_MAP = {0: 'EASY', 1: 'MEDIUM', 2: 'HARD'}
    
    def __init__(self, config: AdaptationConfig = None):
        self.config = config or AdaptationConfig()
        self.attempt_count = 0
        self.history = []  # Track adaptation history
    
    def get_next_difficulty(self, current_difficulty: str, 
                           recent_performance: List[bool],
                           recent_times: List[float]) -> str:
        """
        Determine next difficulty level based on recent performance
        
        Args:
            current_difficulty: Current difficulty level ('EASY', 'MEDIUM', 'HARD')
            recent_performance: List of boolean values (True=correct, False=incorrect)
            recent_times: List of time taken for each attempt (in seconds)
        
        Returns:
            Next difficulty level as string
        """
        self.attempt_count += 1
        
        next_diff = self._adapt_rule_based(
            current_difficulty, recent_performance, recent_times
        )
        
        # Log adaptation
        self.history.append({
            'attempt': self.attempt_count,
            'from': current_difficulty,
            'to': next_diff,
            'accuracy': (sum(recent_performance) / len(recent_performance) * 100) if recent_performance else 0,
            'avg_time': np.mean(recent_times) if recent_times else 0
        })
        
        return next_diff
    
    def _adapt_rule_based(self, current_difficulty: str, 
                         recent_performance: List[bool],
                         recent_times: List[float]) -> str:
        """
        Rule-based adaptation logic:
        - High accuracy (>75%) + fast time → increase difficulty
        - Low accuracy (<50%) or slow time → decrease difficulty
        - Medium performance → stay or make minor adjustment
        
        Args:
            current_difficulty: Current difficulty level
            recent_performance: Recent attempt results
            recent_times: Recent time measurements
        
        Returns:
            Next difficulty level
        """
        if not recent_performance:
            return current_difficulty
        
        # Only adapt after minimum attempts
        if len(recent_performance) < self.config.min_attempts_before_change:
            return current_difficulty
        
        accuracy = (sum(recent_performance) / len(recent_performance)) * 100
        avg_time = np.mean(recent_times) if recent_times else float('inf')
        
        thresholds = self.config.rule_based_thresholds
        current_level = self.DIFFICULTY_MAP[current_difficulty]
        
        # Decision logic
        if accuracy >= thresholds['high'] and avg_time < 10:
            # Doing well - increase difficulty
            next_level = min(current_level + 1, 2)  # Cap at HARD
        elif accuracy <= thresholds['low'] or avg_time > 20:
            # Struggling - decrease difficulty
            next_level = max(current_level - 1, 0)  # Floor at EASY
        else:
            # Medium performance - stay or slight adjustment
            if accuracy > 65 and avg_time < 12:
                next_level = min(current_level + 1, 2)
            elif accuracy < 45 or avg_time > 18:
                next_level = max(current_level - 1, 0)
            else:
                next_level = current_level
        
        return self.REVERSE_MAP[next_level]
    
    def get_adaptation_history(self) -> List[dict]:
        """Return history of all adaptations"""
        return self.history
    
    def reset_history(self):
        """Reset adaptation history and attempt counter"""
        self.history = []
        self.attempt_count = 0
