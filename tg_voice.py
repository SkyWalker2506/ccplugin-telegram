#!/usr/bin/env python3
"""
tg_voice.py — Transcribe audio file using available Whisper backend
Usage: python3 tg_voice.py <audio_file> [backend]
Backend priority: openai-whisper → whisper-cpp → apple → openai-api
Outputs transcription text to stdout.
"""
import os
import sys
import subprocess
import shutil
import tempfile


def transcribe_openai_whisper(audio_file: str) -> str:
    """Use openai-whisper Python package (local)."""
    import whisper  # type: ignore
    model = whisper.load_model("base")
    result = model.transcribe(audio_file, language="tr")
    return result["text"].strip()


def transcribe_whisper_cpp(audio_file: str) -> str:
    """Use whisper.cpp CLI."""
    with tempfile.NamedTemporaryFile(suffix="", delete=False) as tf:
        out_base = tf.name
    try:
        subprocess.run(
            ["whisper-cpp", "--language", "tr", "--model", "base", audio_file, "-otxt", "-of", out_base],
            check=True,
            capture_output=True,
        )
        result_file = out_base + ".txt"
        if os.path.exists(result_file):
            with open(result_file) as f:
                return f.read().strip()
        raise RuntimeError("whisper-cpp produced no output")
    finally:
        for f in [out_base, out_base + ".txt"]:
            try:
                os.unlink(f)
            except Exception:
                pass


def transcribe_apple(audio_file: str) -> str:
    """Use Apple Speech Recognition via Swift script."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    swift_script = os.path.join(script_dir, "apple_speech.swift")
    if not os.path.exists(swift_script):
        raise RuntimeError(f"apple_speech.swift not found at {swift_script}")
    result = subprocess.run(
        ["swift", swift_script, audio_file],
        capture_output=True,
        text=True,
        timeout=60,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())
    return result.stdout.strip()


def transcribe_openai_api(audio_file: str) -> str:
    """Use OpenAI Whisper API (cloud)."""
    import openai  # type: ignore
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        # Try loading secrets
        secrets = os.path.expanduser("~/.claude/secrets/secrets.env")
        if os.path.exists(secrets):
            with open(secrets) as f:
                for line in f:
                    if line.startswith("export OPENAI_API_KEY="):
                        api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")
    client = openai.OpenAI(api_key=api_key)
    with open(audio_file, "rb") as f:
        result = client.audio.transcriptions.create(model="whisper-1", file=f, language="tr")
    return result.text.strip()


def main():
    if len(sys.argv) < 2:
        print("Usage: tg_voice.py <audio_file> [backend]", file=sys.stderr)
        sys.exit(1)

    audio_file = sys.argv[1]
    requested_backend = sys.argv[2] if len(sys.argv) > 2 else None

    if not os.path.exists(audio_file):
        print(f"❌ Audio file not found: {audio_file}", file=sys.stderr)
        sys.exit(1)

    # Backend priority
    backends = []
    if requested_backend:
        backends = [requested_backend]
    else:
        # Auto-detect
        try:
            import whisper  # noqa
            backends.append("openai-whisper")
        except ImportError:
            pass
        if shutil.which("whisper-cpp"):
            backends.append("whisper-cpp")
        if shutil.which("swift"):
            backends.append("apple")
        backends.append("openai-api")  # last resort

    errors = []
    for backend in backends:
        try:
            if backend == "openai-whisper":
                text = transcribe_openai_whisper(audio_file)
            elif backend == "whisper-cpp":
                text = transcribe_whisper_cpp(audio_file)
            elif backend == "apple":
                text = transcribe_apple(audio_file)
            elif backend == "openai-api":
                text = transcribe_openai_api(audio_file)
            else:
                raise RuntimeError(f"Unknown backend: {backend}")

            print(text)
            sys.exit(0)
        except Exception as e:
            errors.append(f"{backend}: {e}")
            continue

    print("❌ All transcription backends failed:", file=sys.stderr)
    for err in errors:
        print(f"  - {err}", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
