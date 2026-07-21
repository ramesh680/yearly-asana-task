"""
Ulta Brands tool: A-Z brand directory from Ulta.com

Each brand includes its official Ulta page link and auto-generated social handles.
Social handles are auto-generated from brand names and mostly unverified, except
a small set of prominent brands with known verified handles.
"""

from . import ulta_brands_data as DATA
from . import socials

INFO = {
    'name': 'Ulta Brands',
    'description': "Ulta's full A–Z brand directory (ulta.com/brand/all), each with its official Ulta page and social handles.",
}

def columns():
    """Return list of (label, key) tuples for CSV/XLSX export"""
    return [
        ('Rank', 'rank'),
        ('Brand', 'brand'),
        ('Ulta Page', 'ulta_url'),
        ('Facebook', 'facebook'),
        ('Instagram', 'instagram'),
        ('X / Twitter', 'twitter'),
        ('YouTube', 'youtube'),
        ('TikTok', 'tiktok'),
        ('Wikipedia', 'wikipedia'),
    ]

def get_brands(live=False):
    """
    Return (rows, meta) tuple.
    
    Each row is a dict with rank, brand, ulta_url, and social handles.
    Meta contains edition info.
    """
    rows = []
    for entry in DATA.ULTA_BRANDS:
        row = dict(entry)
        # Add auto-generated social handles
        socials.fill(row, row['brand'])
        rows.append(row)
    
    meta = {
        'edition': DATA.ULTA_EDITION,
        'source': DATA.ULTA_SOURCE_URL,
        'count': len(rows),
    }
    return rows, meta

def to_csv(rows):
    """Convert rows to CSV format"""
    cols = columns()
    
    # Header
    csv_lines = [','.join(label for label, _ in cols)]
    
    # Data rows
    for row in rows:
        values = []
        for label, key in cols:
            val = row.get(key, '')
            # Escape quotes and wrap if contains comma
            if val:
                val_str = str(val)
                if ',' in val_str or '"' in val_str:
                    val_str = '"' + val_str.replace('"', '""') + '"'
                values.append(val_str)
            else:
                values.append('')
        csv_lines.append(','.join(values))
    
    return '\n'.join(csv_lines)
