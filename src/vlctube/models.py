from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(slots=True)
class QueueItem:
    url: str
    title: str = ""
    status: str = "queued"


@dataclass(slots=True)
class ResolvedStream:
    source_url: str
    title: str
    video_url: str
    audio_url: str | None = None
    webpage_url: str | None = None
    duration: int | None = None
    extractor: str | None = None
    resolved_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def has_separate_audio(self) -> bool:
        return bool(self.audio_url and self.audio_url != self.video_url)
