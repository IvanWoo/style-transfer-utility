from functools import partial
from uuid import uuid4

import click
import imageio

from style_transfer_utility.config import STYLES
from style_transfer_utility.utils import clean, create_animation, create_styled_images

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
@click.option("--all-styles", is_flag=True, help="apply all styles to the image")
@click.version_option()
def main(input_path, style, output, debug, all_styles):
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
        if all_styles:
            for style in STYLES.keys():
                create_styled_images([image], style, prefix)
        else:
            create_styled_images([image], style, prefix)


if __name__ == "__main__":
    main()
