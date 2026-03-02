from datetime import datetime
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)

def _calculate_hour_frequency(hour_data: dict) -> dict:
    """Calculate data-driven busyness_level for each hour.
    
    For each hour (0-23), counts how many days it appears as busy,
    then calculates percentage: (count / 7) * 100
    
    Example:
    Input:  {"monday": [8, 9, 10], "tuesday": [9, 10, 11], ...}
    Output: {0: 0.0, 8: 28.57, 9: 85.71, 10: 85.71, 11: 14.29, ...}
    
    Args:
        hour_data: Dict with day names as keys and lists of busy hours as values
    
    Returns:
        Dict mapping hour (0-23) to busyness_level (0-100%)
    """
    # Initialize frequency counter for all 24 hours
    hour_count = defaultdict(int)
    
    # Count how many days each hour appears as busy
    for day_name, hours in hour_data.items():
        for hour in hours:
            if 0 <= hour < 24:  # Validate hour range
                hour_count[hour] += 1
    
    # Convert counts to percentages (out of 7 days)
    hour_frequency = {}
    for hour in range(24):
        count = hour_count.get(hour, 0)
        busyness_level = (count / 7) * 100
        hour_frequency[hour] = round(busyness_level, 2)
    
    return hour_frequency


def process_and_store_busy_hours_pattern(
    hour_data: dict
):
    """Process busy hours data
    
    Args:
        hour_data: Dict with day names as keys and lists of busy hours as values
                   Supports both formats:
                   - Integer: {"monday": [8, 9, 10]}
                   - Range: {"monday": ["8-9", "9-10", "10-11"]}
    """

    
    # Store pattern data for all day/hour combinations
    day_name_to_dow = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6,
    }
    
    parsed_hour_data = {}

    for day_name, hours in hour_data.items():
        parsed_hours = []
        for hour in hours:
            if isinstance(hour, str):
                # Range format: "20-21" -> extract start hour 20
                try:
                    start_hour = int(hour.split('-')[0])
                    parsed_hours.append(start_hour)
                except (ValueError, IndexError):
                    logger.warning("could not parse hour range: %s, skipping", hour)
            else:
                # Integer format: just use it
                parsed_hours.append(int(hour))
        parsed_hour_data[day_name] = parsed_hours
    
    return parsed_hour_data