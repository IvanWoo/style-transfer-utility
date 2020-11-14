from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from timeit import default_timer as timer

import cv2
import imageio
from psutil import cpu_count
from skimage import img_as_ubyte

from style_transfer_utility.config import IMG_PATH, STYLES, VIDEO_PATH
from style_transfer_utility.inference import inference


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
