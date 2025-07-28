"""
ORIC Score Calculator
Calculates Organizational Readiness for Implementing Change scores
Based on validated survey responses
"""
from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np
from datetime import datetime


class ORICCalculator:
    """Calculate ORIC scores from survey responses"""
    
    # ORIC-12 subscales matching WFD Manager Survey
    # Updated to match exact Qualtrics question IDs
    SUBSCALES = {
        'change_efficacy': ['Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7'],
        'change_commitment': ['Q8', 'Q9', 'Q10', 'Q11', 'Q12', 'Q13']
    }
    
    # Score ranges for interpretation
    SCORE_RANGES = {
        'low': (0, 2.5),
        'moderate': (2.5, 3.5),
        'high': (3.5, 5.0)
    }
    
    def __init__(self, custom_weights: Optional[Dict[str, float]] = None):
        """
        Initialize calculator with optional custom weights
        
        Args:
            custom_weights: Dictionary of subscale weights
        """
        self.weights = custom_weights or {
            'change_commitment': 0.4,
            'change_efficacy': 0.4,
            'contextual_factors': 0.2
        }
    
    def calculate_score(self, responses: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate ORIC score from survey responses
        
        Args:
            responses: Dictionary of question IDs and response values
            
        Returns:
            Dictionary containing overall score and subscale scores
        """
        subscale_scores = {}
        
        # Calculate subscale scores
        for subscale, questions in self.SUBSCALES.items():
            scores = []
            for q in questions:
                if q in responses and responses[q] is not None:
                    try:
                        score = float(responses[q])
                        scores.append(score)
                    except (ValueError, TypeError):
                        continue
            
            if scores:
                subscale_scores[subscale] = np.mean(scores)
            else:
                subscale_scores[subscale] = None
        
        # Calculate weighted overall score
        weighted_scores = []
        total_weight = 0
        
        for subscale, score in subscale_scores.items():
            if score is not None:
                weight = self.weights.get(subscale, 0)
                weighted_scores.append(score * weight)
                total_weight += weight
        
        overall_score = sum(weighted_scores) / total_weight if total_weight > 0 else None
        
        # Determine readiness level
        readiness_level = self._get_readiness_level(overall_score)
        
        return {
            'overall_score': overall_score,
            'subscale_scores': subscale_scores,
            'readiness_level': readiness_level,
            'timestamp': datetime.now().isoformat()
        }
    
    def _get_readiness_level(self, score: Optional[float]) -> Optional[str]:
        """Determine readiness level based on score"""
        if score is None:
            return None
        
        for level, (min_score, max_score) in self.SCORE_RANGES.items():
            if min_score <= score < max_score:
                return level
        
        return 'high' if score >= 5.0 else 'low'
    
    def calculate_trends(self, historical_scores: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate trends from historical ORIC scores
        
        Args:
            historical_scores: List of score dictionaries with timestamps
            
        Returns:
            Dictionary containing trend analysis
        """
        if not historical_scores:
            return {'error': 'No historical data available'}
        
        # Convert to DataFrame for easier analysis
        df = pd.DataFrame(historical_scores)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
        
        # Calculate trends
        trends = {
            'overall_trend': self._calculate_trend(df['overall_score'].dropna()),
            'current_score': df['overall_score'].iloc[-1] if not df.empty else None,
            'average_score': df['overall_score'].mean(),
            'score_volatility': df['overall_score'].std(),
            'improvement_rate': None,
            'subscale_trends': {}
        }
        
        # Calculate improvement rate
        if len(df) >= 2:
            first_score = df['overall_score'].iloc[0]
            last_score = df['overall_score'].iloc[-1]
            if first_score and last_score:
                trends['improvement_rate'] = (
                    (last_score - first_score) / first_score * 100
                )
        
        # Calculate subscale trends
        for subscale in self.SUBSCALES:
            subscale_col = f'subscale_scores.{subscale}'
            if subscale_col in df.columns:
                trends['subscale_trends'][subscale] = self._calculate_trend(
                    df[subscale_col].dropna()
                )
        
        return trends
    
    def _calculate_trend(self, series: pd.Series) -> str:
        """Calculate trend direction from a series of values"""
        if len(series) < 2:
            return 'insufficient_data'
        
        # Simple linear regression
        x = np.arange(len(series))
        y = series.values
        
        if len(x) > 1:
            slope = np.polyfit(x, y, 1)[0]
            
            if slope > 0.05:
                return 'improving'
            elif slope < -0.05:
                return 'declining'
            else:
                return 'stable'
        
        return 'insufficient_data'
    
    def generate_insights(self, score_data: Dict[str, Any]) -> List[str]:
        """
        Generate actionable insights based on ORIC scores
        
        Args:
            score_data: Dictionary containing score information
            
        Returns:
            List of insight strings
        """
        insights = []
        overall_score = score_data.get('overall_score')
        subscale_scores = score_data.get('subscale_scores', {})
        readiness_level = score_data.get('readiness_level')
        
        # Overall readiness insights
        if readiness_level == 'low':
            insights.append(
                "Organization shows low readiness for change. "
                "Consider building foundation through leadership "
                "alignment and communication."
            )
        elif readiness_level == 'moderate':
            insights.append(
                "Organization shows moderate readiness. "
                "Focus on strengthening weak areas before "
                "full implementation."
            )
        else:
            insights.append(
                "Organization shows high readiness for change. "
                "Capitalize on momentum for implementation."
            )
        
        # Subscale-specific insights
        for subscale, score in subscale_scores.items():
            if score is not None:
                if score < 2.5:
                    if subscale == 'change_commitment':
                        insights.append(
                            "Low change commitment detected. "
                            "Increase stakeholder buy-in through "
                            "clear vision communication."
                        )
                    elif subscale == 'change_efficacy':
                        insights.append(
                            "Low change efficacy detected. "
                            "Provide training and resources to "
                            "build confidence."
                        )
                    elif subscale == 'contextual_factors':
                        insights.append(
                            "Contextual barriers identified. "
                            "Address organizational constraints "
                            "and resource limitations."
                        )
        
        # Identify strongest and weakest areas
        if subscale_scores:
            strongest = max(subscale_scores.items(), 
                          key=lambda x: x[1] if x[1] else 0)
            weakest = min(subscale_scores.items(), 
                        key=lambda x: x[1] if x[1] else 5)
            
            if strongest[1] and weakest[1]:
                insights.append(
                    f"Leverage strength in {strongest[0].replace('_', ' ')} "
                    f"to address weakness in {weakest[0].replace('_', ' ')}."
                )
        
        return insights
