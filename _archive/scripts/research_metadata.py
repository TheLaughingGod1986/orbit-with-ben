"""Keep public research fields without yt-dlp's multi-megabyte caption/format URL trees."""
FIELDS = frozenset(('id', 'title', 'description', 'timestamp', 'upload_date', 'view_count',
                    'duration', 'channel', 'channel_id', 'channel_url', 'webpage_url',
                    'thumbnails', 'thumbnail', 'availability', 'live_status', 'release_timestamp',
                    'like_count', 'comment_count', 'categories', 'tags', 'age_limit'))


def compact(value):
    """Preserve research data; never retain expiring playback URLs or captions."""
    return {k: v for k, v in value.items() if k in FIELDS}
