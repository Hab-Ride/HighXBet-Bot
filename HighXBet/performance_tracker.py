import pandas as pd
import json
from datetime import datetime
import os

class PerformanceTracker:
    def __init__(self):
        self.results_file = "betting_results.csv"
        self.setup_tracker()
    
    def setup_tracker(self):
        """Initialize results tracking file"""
        if not os.path.exists(self.results_file):
            df = pd.DataFrame(columns=[
                'date', 'match', 'bet_type', 'odds', 'probability', 
                'expected_value', 'outcome', 'profit'
            ])
            df.to_csv(self.results_file, index=False)
            print("✅ Created betting results tracker")
    
    def record_bet(self, match, bet_type, odds, probability, expected_value):
        """Record a new value bet"""
        df = pd.read_csv(self.results_file)
        
        new_bet = {
            'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'match': match,
            'bet_type': bet_type,
            'odds': odds,
            'probability': probability,
            'expected_value': expected_value,
            'outcome': 'PENDING',
            'profit': 0
        }
        
        df = pd.concat([df, pd.DataFrame([new_bet])], ignore_index=True)
        df.to_csv(self.results_file, index=False)
        print(f"✅ Recorded: {match} - {bet_type} @ {odds}")
    
    def get_performance_stats(self):
        """Get performance statistics"""
        if not os.path.exists(self.results_file):
            return "No bets recorded yet"
        
        df = pd.read_csv(self.results_file)
        if len(df) == 0:
            return "No bets recorded yet"
        
        total_bets = len(df)
        completed_bets = len(df[df['outcome'] != 'PENDING'])
        winning_bets = len(df[df['profit'] > 0])
        
        if completed_bets > 0:
            win_rate = (winning_bets / completed_bets) * 100
            total_profit = df['profit'].sum()
            avg_ev = df['expected_value'].mean() * 100
        else:
            win_rate = 0
            total_profit = 0
            avg_ev = df['expected_value'].mean() * 100
        
        stats = f"""
📊 PERFORMANCE TRACKER
====================
Total Value Bets: {total_bets}
Completed Bets: {completed_bets}
Win Rate: {win_rate:.1f}%
Total Profit: ${total_profit:.2f}
Average EV: +{avg_ev:.1f}%
Pending: {total_bets - completed_bets}
====================
"""
        return stats

# Test the tracker
if __name__ == "__main__":
    tracker = PerformanceTracker()
    
    # Test with your found bets
    tracker.record_bet("Udinese vs Genoa", "Over 2.5", 2.52, 0.555, 0.399)
    tracker.record_bet("Lecce vs Torino", "Over 2.5", 2.60, 0.420, 0.092)
    
    print(tracker.get_performance_stats())