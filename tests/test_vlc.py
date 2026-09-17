from vlctube.models import ResolvedStream
from vlctube.vlc import build_vlc_command


def test_build_vlc_command_single_stream(tmp_path):
    vlc = tmp_path / "vlc.exe"
    vlc.write_bytes(b"")
    stream = ResolvedStream(
        source_url="https://example.com/watch?v=1",
        title="Example",
        video_url="https://cdn.example/video",
    )
    command = build_vlc_command(str(vlc), stream)
    assert command[0] == str(vlc)
    assert "--one-instance" in command
    assert command[-1] == "https://cdn.example/video"
    assert not any(part.startswith("--input-slave=") for part in command)


def test_build_vlc_command_separate_audio_and_enqueue(tmp_path):
    vlc = tmp_path / "vlc.exe"
    vlc.write_bytes(b"")
    stream = ResolvedStream(
        source_url="https://example.com/watch?v=1",
        title="Example",
        video_url="https://cdn.example/video",
        audio_url="https://cdn.example/audio",
    )
    command = build_vlc_command(str(vlc), stream, enqueue=True)
    assert "--playlist-enqueue" in command
    assert "--input-slave=https://cdn.example/audio" in command
