import re
from typing import Optional
from datetime import datetime


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)
    return text


def truncate_string(text: str, max_length: int = 100) -> str:
    """Truncate string to max length with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def format_datetime(dt: datetime, format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format datetime to string."""
    if dt is None:
        return ""
    return dt.strftime(format)


def parse_datetime(
    date_string: str, 
    format: str = "%Y-%m-%d %H:%M:%S"
) -> Optional[datetime]:
    """Parse string to datetime."""
    try:
        return datetime.strptime(date_string, format)
    except ValueError:
        return None


def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def generate_filename(
    original_filename: str, 
    prefix: str = ""
) -> str:
    """Generate a unique filename."""
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    name, ext = original_filename.rsplit(".", 1) if "." in original_filename else (original_filename, "")
    slugified_name = slugify(name)
    
    if prefix:
        return f"{prefix}_{timestamp}_{slugified_name}.{ext}"
    return f"{timestamp}_{slugified_name}.{ext}"
