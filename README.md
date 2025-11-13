# MATH ADVENTURES - Adaptive Learning System

An interactive console-based adaptive math learning system that dynamically adjusts puzzle difficulty based on user performance using a rule-based approach.

## Features

- Generates math puzzles with varying difficulty: Easy, Medium, Hard
- Tracks detailed user performance:
  - Accuracy, time taken, performance trends, and difficulty-specific stats
- Adaptively adjusts puzzle difficulty in real-time using rule-based logic based on recent accuracy and response times
- Provides a session summary with recommendations and adaptation history

## Architecture

The system comprises four main components:

- **PuzzleGenerator:** Creates math puzzles using operands and operations tuned to difficulty.
- **PerformanceTracker:** Logs every user attempt with timing, correctness, and answer details.
- **AdaptiveEngine:** Applies rule-based thresholds to adapt difficulty level dynamically.
- **MainApplication:** Provides an interactive CLI interface driving puzzles and adaptation.

## Adaptive Logic

The engine uses explicit rules based on recent accuracy and speed, adapting difficulty to optimize learning without overwhelming the learner.

## Usage

1. Clone the repository.
2. Install dependencies:
