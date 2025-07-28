"""
Quick test script for ORIC calculation
Run this to verify the installation is working correctly
"""
from oric_calculator import ORICCalculator

def test_oric_calculation():
    """Test ORIC calculation with sample data"""
    print("Testing ORIC Calculator...")
    print("-" * 50)
    
    # Sample survey responses (scale 1-5)
    test_responses = {
        'Q1': 4, 'Q2': 4, 'Q3': 5, 'Q4': 4, 'Q5': 4,  # High commitment
        'Q6': 2, 'Q7': 2, 'Q8': 3, 'Q9': 2, 'Q10': 2,  # Low efficacy
        'Q11': 4, 'Q12': 4, 'Q13': 3, 'Q14': 4, 'Q15': 3  # Moderate context
    }
    
    calculator = ORICCalculator()
    result = calculator.calculate_score(test_responses)
    
    print(f"\nOverall ORIC Score: {result['overall_score']:.2f}")
    print(f"Readiness Level: {result['readiness_level']}")
    
    print("\nSubscale Scores:")
    for subscale, score in result['subscale_scores'].items():
        print(f"  • {subscale.replace('_', ' ').title()}: {score:.2f}")
    
    # Generate insights
    insights = calculator.generate_insights(result)
    print("\nKey Insights:")
    for i, insight in enumerate(insights, 1):
        print(f"  {i}. {insight}")
    
    print("\n" + "-" * 50)
    print("✓ ORIC Calculator is working correctly!")

if __name__ == "__main__":
    test_oric_calculation()
