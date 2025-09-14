from PIL import Image, ImageEnhance, ImageFont


class ImageUtils:
    @staticmethod
    def set_brightness(image: Image.Image, brightness: float) -> Image.Image:
        return ImageEnhance.Brightness(image).enhance(brightness)

    @staticmethod
    def get_centered_position(
        width: int, height: int, element_width: int, element_height: int
    ) -> tuple[int, int]:
        x = (width - element_width) // 2
        y = (height - element_height) // 2
        return (x, y)

    @staticmethod
    def get_font(font_path: str, font_size: int) -> ImageFont.FreeTypeFont:
        return ImageFont.truetype(font_path, font_size)

    @staticmethod
    def get_text_dimensions(
        text: str, font: ImageFont.FreeTypeFont
    ) -> tuple[float, float, tuple[float, float, float, float]]:
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        return (text_width, text_height, bbox)

    @staticmethod
    def get_image(image_path: str, size: tuple[int, int] | None = None) -> Image.Image:
        image = Image.open(image_path)

        if size:
            return image.resize(size, Image.Resampling.LANCZOS)

        return image
