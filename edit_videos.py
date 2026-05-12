import os
from moviepy.editor import VideoFileClip, ColorClip, TextClip, CompositeVideoClip

INPUT_DIR = r"C:\VideoEditor\input"
OUTPUT_DIR = r"C:\VideoEditor\output"

BEIGE = (245, 245, 220)
DARK_BROWN = "#654321"

BANNER_HEIGHT_RATIO = 0.18
TEXT = "MEKA"
START_TIME = 28
END_TIME = 30


def process_video(input_path: str, output_path: str) -> None:
    video = VideoFileClip(input_path).subclip(START_TIME, END_TIME)
    width, height = video.size
    banner_height = int(height * BANNER_HEIGHT_RATIO)

    banner = (
        ColorClip(size=(width, banner_height), color=BEIGE)
        .set_duration(video.duration)
        .set_position((0, 0))
    )

    text = (
        TextClip(
            TEXT,
            fontsize=int(banner_height * 0.7),
            color=DARK_BROWN,
            font="DejaVu-Sans-Bold",
        )
        .set_duration(video.duration)
        .set_position(("center", (banner_height - int(banner_height * 0.7)) // 2))
    )

    final = CompositeVideoClip([video, banner, text])
    final.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        temp_audiofile="temp-audio.m4a",
        remove_temp=True,
    )

    final.close()
    video.close()


def main() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if not os.path.isdir(INPUT_DIR):
        raise FileNotFoundError(f"Input folder '{INPUT_DIR}' does not exist.")

    mp4_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".mp4")]

    if not mp4_files:
        print(f"No MP4 files found in '{INPUT_DIR}'.")
        return

    for filename in mp4_files:
        input_path = os.path.join(INPUT_DIR, filename)
        output_path = os.path.join(OUTPUT_DIR, filename)
        print(f"Processing {input_path} -> {output_path}")
        process_video(input_path, output_path)

    print("Done.")


if __name__ == "__main__":
    main()
