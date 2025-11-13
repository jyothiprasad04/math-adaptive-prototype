"""
Main Application Module
Console-based interactive adaptive learning system (Rule-Based Only)
"""
import time
from puzzle_generator import PuzzleGenerator, DifficultyLevel
from tracker import PerformanceTracker
from adaptive_engine import AdaptiveEngine, AdaptationConfig

class AdaptiveLearningApp:
    """Main application class - Rule-based adaptation only"""
    
    def __init__(self):
        pass
        
    def run(self):
        """Main application flow"""
        print("\n" + "=" * 70)
        print("MATH ADVENTURES - AI-Powered Adaptive Learning System")
        print("=" * 70 + "\n")
        
        # Get user name
        user_name = input("Welcome! What's your name? ").strip()
        if not user_name:
            user_name = "Learner"
        
        print(f"\nHi {user_name}! Let's practice some math! \n")
        
        # Choose difficulty
        print("Choose your starting difficulty:")
        print("1. Easy   (1-10, +/-)")
        print("2. Medium (5-50, +/-/*)")
        print("3. Hard   (10-100, +/-/*/÷)")
        
        while True:
            choice = input("\nEnter (1/2/3): ").strip()
            if choice in ['1', '2', '3']:
                difficulty_map = {'1': 'EASY', '2': 'MEDIUM', '3': 'HARD'}
                current_difficulty = difficulty_map[choice]
                break
            print("Invalid choice. Please enter 1, 2, or 3.")
        
        print(f"\nGreat! Starting with {current_difficulty} level.\n")
        
        # Initialize components
        puzzle_gen = PuzzleGenerator()
        tracker = PerformanceTracker(user_name)
        config = AdaptationConfig(
            rule_based_thresholds={'high': 75, 'low': 50},
            min_attempts_before_change=2
        )
        adaptive_engine = AdaptiveEngine(config=config)
        
        puzzle_count = 0
        max_puzzles = 10
        
        print("Adaptation Strategy: RULE-BASED\n")
        print("-" * 70)
        
        # Main loop
        try:
            while puzzle_count < max_puzzles:
                # Generate puzzle
                difficulty_enum = DifficultyLevel[current_difficulty]
                puzzle = puzzle_gen.generate_puzzle(difficulty_enum)
                puzzle_count += 1
                
                # Display puzzle
                print(f"\n[Question {puzzle_count}/{max_puzzles}] ({current_difficulty})")
                print(f"Problem: {puzzle}")
                
                # Get user answer with timeout tracking
                start_time = time.time()
                try:
                    user_answer = input("Your answer: ").strip()
                    elapsed_time = time.time() - start_time
                    
                    if not user_answer:
                        print("Please enter a number!")
                        continue
                    
                    user_answer = int(user_answer)
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
                    continue
                
                # Check answer
                is_correct = user_answer == puzzle.correct_answer
                result = " Correct!" if is_correct else f" Wrong! Correct answer: {puzzle.correct_answer}"
                print(result)
                
                # Log attempt
                tracker.log_attempt(
                    puzzle_id=puzzle_count,
                    difficulty=current_difficulty,
                    correct=is_correct,
                    time_taken=elapsed_time,
                    user_answer=user_answer,
                    correct_answer=puzzle.correct_answer
                )
                
                # Get performance trend for adaptation
                trend = tracker.get_performance_trend(window_size=5)
                times = [r.time_taken for r in tracker.records[-5:]]
                
                # Adapt difficulty (rule-based only)
                new_difficulty = adaptive_engine.get_next_difficulty(
                    current_difficulty=current_difficulty,
                    recent_performance=trend,
                    recent_times=times
                )
                
                # Notify if difficulty changed
                if new_difficulty != current_difficulty:
                    print(f" Difficulty adjusted: {current_difficulty} → {new_difficulty}")
                    current_difficulty = new_difficulty
                else:
                    print(f" Keeping {current_difficulty} level")
                
                print(f" Time: {elapsed_time:.2f}s | Accuracy (last 5): {tracker.get_accuracy(recent_n=5):.1f}%")
                print("-" * 70)
        
        except KeyboardInterrupt:
            print("\n\nSession interrupted by user.")
        
        # Display summary
        self.display_summary(tracker, adaptive_engine)
    
    def display_summary(self, tracker: PerformanceTracker, adaptive_engine: AdaptiveEngine):
        """Display session summary"""
        summary = tracker.get_session_summary()
        
        print("\n" + "=" * 70)
        print("SESSION SUMMARY")
        print("=" * 70)
        print(f"\nStudent: {summary['user_name']}")
        print(f"Total Puzzles: {summary['total_puzzles']}")
        print(f"Correct Answers: {summary['total_correct']}/{summary['total_puzzles']}")
        print(f"Overall Accuracy: {summary['overall_accuracy']:.1f}%")
        print(f"Average Time Per Puzzle: {summary['average_time_per_puzzle']:.2f}s")
        print(f"Session Duration: {summary['session_duration_seconds']:.1f}s")
        
        print("\nPerformance by Difficulty:")
        for difficulty, stats in summary['difficulty_stats'].items():
            print(f"  {difficulty}: {stats['accuracy']:.1f}% accuracy ({stats['attempts']} attempts, {stats['avg_time']:.2f}s avg)")
        
        print("\n Adaptation History:")
        for i, event in enumerate(adaptive_engine.get_adaptation_history()[-10:], 1):
            print(f"  {i}. Attempt {event['attempt']}: {event['from']} → {event['to']} "
                  f"(Accuracy: {event['accuracy']:.1f}%, Avg Time: {event['avg_time']:.2f}s)")
        
        print("\n Recommendation:")
        if summary['overall_accuracy'] >= 80:
            print(f"   Excellent work! You're ready for harder challenges!")
        elif summary['overall_accuracy'] >= 60:
            print(f"   Good progress! Keep practicing to improve!")
        else:
            print(f"   Keep practicing! You'll get better with more attempts!")
        
        print("\n" + "=" * 70 + "\n")

def main():
    """Entry point"""
    print("\n MATH ADVENTURES - Adaptive Learning System")
    
    app = AdaptiveLearningApp()
    app.run()

if __name__ == "__main__":
    main()
