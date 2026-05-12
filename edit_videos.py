import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip

INPUT_DIR = r"C:\VideoEditor\input"
OUTPUT_DIR = r"C:\VideoEditor\output"

BEIGE = (245, 245, 220)
DARK_BROWN = (101, 67, 33)

BANNER_HEIGHT_RATIO = 0.18
TEXT = "MEKA"
START_TIME = 28
END_TIME = 30

FONT_CANDIDATES = [
    r"C:\Windows\Fonts\arialbd.ttf",
    r"C:\Windows\Fonts\arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


def load_font(size: int) -> ImageFont.FreeTypeFont:
    for path in FONT_CANDIDATES:
        if os.path.isfile(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def build_banner(width: int, height: int) -> np.ndarray:
    img = Image.new("RGB", (width, height), BEIGE)
    draw = ImageDraw.Draw(img)

    font_size = int(height * 0.7)
    font = load_font(font_size)

    bbox = draw.textbbox((0, 0), TEXT, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    x = (width - text_w) // 2 - bbox[0]
    y = (height - text_h) // 2 - bbox[1]

    draw.text((x, y), TEXT, fill=DARK_BROWN, font=font)
    return np.array(img)


def process_video(input_path: str, output_path: str) -> None:
    video = VideoFileClip(input_path).subclip(START_TIME, END_TIME)
    width, height = video.size
    banner_height = int(height * BANNER_HEIGHT_RATIO)

    banner_array = build_banner(width, banner_height)
    banner_clip = (
        ImageClip(banner_array)
        .set_duration(video.duration)
        .set_position((0, 0))
    )

    final = CompositeVideoClip([video, banner_clip])
    final.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        temp_audiofile="temp-audio.m4a",
        remove_temp=True,
    )

    final.close()
    banner_clip.close()
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
