from concurrent.futures import ProcessPoolExecutor
from functools import partial
from pathlib import Path
from timeit import default_timer as timer
from uuid import uuid4

import click
import cv2
import imageio
from psutil import cpu_count
from skimage import img_as_ubyte

from style_transfer_utility.config import IMG_PATH, STYLES, VIDEO_PATH
from style_transfer_utility.inference import inference

click.option = partial(click.option, show_default=True)


@click.command()
@click.option("-i", "--input-path", required=True)
@click.option(
    "--style",
    required=True,
    type=click.Choice(STYLES.keys(), case_sensitive=False),
)
@click.option("-o", "--output", help="the output name")
@click.option("--debug", is_flag=True)
@click.option("--all-style", is_flag=True, help="apply all styles to the image")
@click.version_option()
def main(input_path, style, output, debug, all_style):
    """
    \b
    style-transfer-utility: stu
    Utility for applying style transfer models into images or videos.
    """
    prefix = output or str(uuid4())
    try:
        video = imageio.mimread(input_path, memtest=False)
        reader = imageio.get_reader(input_path)
        fps = reader.get_meta_data()["fps"]
        print("start creating styled images")
        create_styled_images(video, style, prefix)
        print("start creating animation")
        create_animation(fps, prefix)
        if not debug:
            print("clean up temp files")
            clean(prefix)
    except ValueError as e:
        print(e)
        image = imageio.imread(input_path)
        if all_style:
            for style in STYLES.keys():
                create_styled_images([image], style, prefix)
        else:
            create_styled_images([image], style, prefix)


def worker(index, image, style, prefix):
    model = STYLES[style]
    output, _ = inference(model, image)
    name = f"{IMG_PATH}{prefix}-{style}-{index}.jpg"
    print(f"generated image: {name=}")
    cv2.imwrite(name, output)
    return


def create_styled_images(video, style, prefix):
    start = timer()
    with ProcessPoolExecutor(max_workers=cpu_count(logical=False)) as executor:
        [
            executor.submit(worker, index, image, style, prefix)
            for index, image in enumerate(video)
        ]
    end = timer()
    print(f"takes {end - start}s")


def create_animation(fps, prefix):
    path = Path(IMG_PATH).rglob(f"{prefix}*.jpg")
    styled_images = {}
    for file in path:
        styled_images[int(file.stem.split("-")[-1])] = imageio.imread(file)
    images = [styled_images[k] for k in sorted(styled_images.keys())]
    name = f"{VIDEO_PATH}{prefix}.mp4"
    imageio.mimsave(name, [img_as_ubyte(frame) for frame in images], fps=fps)
    print(f"generated animation: {name=}")


def clean(prefix):
    path = Path(IMG_PATH).rglob(f"{prefix}*.jpg")
    for file in path:
        file.unlink()


if __name__ == "__main__":
    main()
