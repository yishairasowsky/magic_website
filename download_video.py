"""
Video downloader using yt-dlp.
Supports YouTube, Instagram, Twitter/X, Facebook, Vimeo, and 1000+ other sites.

Usage:
    python download_video.py <URL>
    python download_video.py <URL> --audio-only
    python download_video.py <URL> --output /path/to/folder
"""

import sys
import os
import argparse
import yt_dlp


def download_video(url, audio_only=False, output_dir="."):
    output_dir = os.path.abspath(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
        "noplaylist": True,  # download single video, not whole playlist
    }

    if audio_only:
        ydl_opts["format"] = "bestaudio/best"
        ydl_opts["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
        }]
        print("Downloading audio only (mp3)...")
    else:
        ydl_opts["format"] = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
        print("Downloading best quality video...")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get("title", "video")
        print(f"\nDone: '{title}' saved to {output_dir}")


def main():
    parser = argparse.ArgumentParser(description="Download a video from the internet.")
    parser.add_argument("url", help="URL of the video to download")
    parser.add_argument("--audio-only", action="store_true", help="Extract audio as mp3 instead of video")
    parser.add_argument("--output", default=".", help="Output folder (default: current directory)")
    args = parser.parse_args()

    download_video(args.url, audio_only=args.audio_only, output_dir=args.output)


if __name__ == "__main__":
    main()
