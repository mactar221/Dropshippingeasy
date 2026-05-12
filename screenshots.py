import cv2
import os
import sys


def capture_frames(video_path: str, interval_seconds: int = 5, output_dir: str = "screenshots") -> None:
    os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file: {video_path}")
        sys.exit(1)

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps if fps > 0 else 0
    frame_interval = int(fps * interval_seconds)

    print(f"Video: {video_path}")
    print(f"FPS: {fps:.2f} | Duration: {duration:.1f}s | Total frames: {total_frames}")
    print(f"Capturing one frame every {interval_seconds}s (every {frame_interval} frames)")

    saved = 0
    frame_number = 0

    while True:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()
        if not ret:
            break

        timestamp_seconds = int(frame_number / fps)
        minutes = timestamp_seconds // 60
        seconds = timestamp_seconds % 60
        filename = os.path.join(output_dir, f"frame_{minutes:02d}m{seconds:02d}s.jpg")

        cv2.imwrite(filename, frame)
        print(f"  Saved: {filename}")
        saved += 1

        frame_number += frame_interval

    cap.release()
    print(f"\nDone. {saved} screenshots saved to '{output_dir}/'")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python screenshots.py <video_file> [interval_seconds] [output_dir]")
        print("  video_file       Path to the video file")
        print("  interval_seconds Seconds between frames (default: 5)")
        print("  output_dir       Output folder name (default: screenshots)")
        sys.exit(1)

    video_file = sys.argv[1]
    interval = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    output = sys.argv[3] if len(sys.argv) > 3 else "screenshots"

    capture_frames(video_file, interval, output)
