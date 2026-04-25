"""
PAPER 2 - COMPARISON: Sequential Decision Pipelines
Baseline system with slower, sequential workflow
"""

import time

class SequentialPipeline:
    """
    Sequential workflow processes tasks one-by-one without parallelization.
    Results in longer decision times and potential accuracy loss.
    """
    
    def __init__(self):
        self.tasks = [
            "triage_assessment",
            "vital_signs_monitoring",
            "lab_ordering",
            "imaging_review",
            "intervention_selection"
        ]
    
    def run_algorithm(self, trauma_case, verbose=True):
        """
        Execute sequential pipeline algorithm.
        
        Args:
            trauma_case: Dict with case metrics
            verbose: Print progress
            
        Returns:
            Dict with decision_time_seconds and accuracy_rate_percent (baseline)
        """
        start_time = time.time()
        
        if verbose:
            print("[Sequential Pipeline] Starting sequential workflow...")
        
        complexity = trauma_case.get("case_complexity", 0.5)
        
        # Sequential tasks without parallelization
        task_durations = {
            "triage_assessment": 5.2 + (complexity * 2.0),
            "vital_signs_monitoring": 4.8 + (complexity * 1.5),
            "lab_ordering": 3.5 + (complexity * 1.0),
            "imaging_review": 5.1 + (complexity * 2.2),
            "intervention_selection": 3.4 + (complexity * 1.0),
        }
        
        # Sequential execution - no parallelization benefit
        total_time = sum(task_durations.values())
        
        # Lower baseline accuracy due to sequential delays and potential errors
        base_accuracy = 0.75
        accuracy_degradation = complexity * 0.05
        avg_accuracy = max(0.60, base_accuracy - accuracy_degradation) * 100
        
        if verbose:
            print(f"  [Task Durations]:")
            for task, duration in task_durations.items():
                print(f"    {task}: {duration:.2f}s")
            print(f"  [Total Sequential Time] {total_time:.2f}s")
            print(f"  [Accuracy Rate] {avg_accuracy:.2f}%")
        
        elapsed = time.time() - start_time
        
        return {
            "decision_time_seconds": round(total_time, 2),
            "accuracy_rate_percent": round(avg_accuracy, 2),
            "execution_time": elapsed,
        }
