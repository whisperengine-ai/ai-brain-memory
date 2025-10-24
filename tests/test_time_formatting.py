"""Quick test to verify time formatting."""

from datetime import datetime, timedelta

def format_time_ago(timestamp: str) -> str:
    """Format timestamp as human-readable 'time ago' string."""
    try:
        ts = datetime.fromisoformat(timestamp)
        now = datetime.now()
        delta = now - ts
        
        if delta.days > 0:
            return f"{delta.days} day{'s' if delta.days != 1 else ''} ago"
        elif delta.seconds >= 3600:
            hours = delta.seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif delta.seconds >= 60:
            minutes = delta.seconds // 60
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        else:
            return "just now"
    except Exception:
        return "recently"

# Test cases
print("Testing time formatting:")
print()

# Just now
now = datetime.now().isoformat()
print(f"Now: {format_time_ago(now)}")

# 5 minutes ago
five_min_ago = (datetime.now() - timedelta(minutes=5)).isoformat()
print(f"5 minutes ago: {format_time_ago(five_min_ago)}")

# 2 hours ago
two_hours_ago = (datetime.now() - timedelta(hours=2)).isoformat()
print(f"2 hours ago: {format_time_ago(two_hours_ago)}")

# 1 day ago
one_day_ago = (datetime.now() - timedelta(days=1)).isoformat()
print(f"1 day ago: {format_time_ago(one_day_ago)}")

# 3 days ago
three_days_ago = (datetime.now() - timedelta(days=3)).isoformat()
print(f"3 days ago: {format_time_ago(three_days_ago)}")

# Test with actual timestamp from logs
print()
print("Testing with real timestamp from logs:")
test_timestamp = "2025-10-24T12:11:44.297730"
print(f"Timestamp: {test_timestamp}")
print(f"Formatted: {format_time_ago(test_timestamp)}")
