class LongestNonOverlappingIntervals:
    def __init__(self, intervals):
        """
        Initializes with a list of intervals.
        :param intervals: List of tuples (start, end).
        """
        self.intervals = intervals

    def get_longest_intervals(self):
        """
        Returns the longest non-overlapping intervals.
        :return: List of tuples representing the longest non-overlapping intervals.
        """
        if not self.intervals:
            return []

        # Step 1: Sort intervals by start time, and for ties, by descending end time
        self.intervals.sort(key=lambda x: (x[0], -x[1]))
        
        # Step 2: check whether there is any overlap
        for i in range(1, len(self.intervals)):
            if self.intervals[i][0] < self.intervals[i-1][1]:
                return self.intervals

        # Step 2: Use a greedy algorithm to select the longest non-overlapping intervals
        selected_intervals = []
        prev_end = float('-inf')

        for start, end in self.intervals:
            if start >= prev_end:
                # Add the interval if it doesn't overlap with the previous one
                selected_intervals.append((start, end))
                prev_end = end

        return selected_intervals
    
    
# Example Usage:
if __name__ == "__main__":
    print("Longest Non-Overlapping Intervals")
    intervals = [(1, 5), (2, 6), (8, 10), (3, 4), (9, 11)]
    selector = LongestNonOverlappingIntervals(intervals)
    longest_intervals = selector.get_longest_intervals()
    print(longest_intervals)
    
    intervals = [(1, 5), (6, 9), (12,43)]
    selector = LongestNonOverlappingIntervals(intervals)
    longest_intervals = selector.get_longest_intervals()
    print(longest_intervals)
    

    