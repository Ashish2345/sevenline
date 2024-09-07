
import os
from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile
from io import BytesIO

from django.conf import settings


class ProcessImage():

    def __init__(self, image_path):
        self.font_path = os.path.join(settings.BASE_DIR,'servenline', 'image_processing', 'Sanujfont.ttf')


    def result_generate(self, date, first_prize, three_digits, two_down, next_drawn_date):
        # Open the first image (template)
        img_path_template = os.path.join(settings.BASE_DIR, 'servenline', 'image_processing', 'result.png')
        print(img_path_template)
        img_template = Image.open(img_path_template)
        
        font_large_med = ImageFont.truetype(self.font_path, 38)
        font_large = ImageFont.truetype(self.font_path, 40)
        font_small = ImageFont.truetype(self.font_path, 38)

        # Create a drawing context
        draw = ImageDraw.Draw(img_template)

        # Define the positions for text on the template
        draw_date = (190, 110)
        draw_1st_prize = (155, 225)
        draw_3digits = (70, 325)
        draw_2down = (190, 435)
        draw_next_draw = (190, 550)

        # Drawing the text onto the template image
        draw.text(draw_date, date, font=font_large_med, fill="black")
        draw.text(draw_1st_prize, first_prize, font=font_large, fill="black")
        draw.text(draw_3digits, three_digits, font=font_large, fill="black")
        draw.text(draw_2down, two_down, font=font_large, fill="black")
        draw.text(draw_next_draw, next_drawn_date, font=font_small, fill="black")

        # Save the image to a BytesIO object
        img_io = BytesIO()
        img_template.save(img_io, format='PNG')
        img_io.seek(0)

        return img_io


    def sasima_img_generate(self):

        # Load the original image
        image_path = 'sasima.jpg'  # The original image you uploaded

        # Open the image
        image = Image.open(image_path)

        # Create a drawing context
        draw = ImageDraw.Draw(image)

        # Load font (adjust path to a valid .ttf font on your system)
        try:
            font_path = "Sanujfont.ttf"
            font = ImageFont.truetype(font_path, 48)
            font_date = ImageFont.truetype(font_path, 15)
            font_watermark = ImageFont.truetype('arial.ttf', 30)  # Font for the watermark
        except IOError:
            font = ImageFont.load_default()

        # Function to draw rotated text
        def draw_rotated_text(draw, position, text, angle, font, fill):
            # Create a separate image for the text to rotate
            text_image = Image.new('RGBA', (100, 100), (255, 255, 255, 0))
            text_draw = ImageDraw.Draw(text_image)
            text_draw.text((0, 0), text, font=font, fill=fill)

            # Rotate the image and paste it back on the original
            rotated_image = text_image.rotate(angle, expand=1)
            image.paste(rotated_image, position, rotated_image)

        # Define text positions, content, and angles based on your second image
        positions = {
            "5": ((25, 20), -10),  # Rotated slightly to the left
            "7": ((180, 20), -10),  # Rotated slightly to the right
            "2": ((25, 100), -10),  # Rotated slightly to the left
            "8": ((180, 100), -10),  # Rotated slightly to the right
            "date": ((100, 138), 0),  # Bottom center with no rotation
            "watermark": ((0, 80), 25)  # Position of watermark
        }

        # Define colors
        text_color = (255, 0, 0)  # Red for numbers
        date_color = (0, 0, 0)  # Black for the date
        watermark_color = (255, 165, 0)  # Orange color for the watermark

        # Draw the numbers with rotation
        draw_rotated_text(draw, positions["5"][0], "5", positions["5"][1], font, text_color)
        draw_rotated_text(draw, positions["7"][0], "7", positions["7"][1], font, text_color)
        draw_rotated_text(draw, positions["2"][0], "2", positions["2"][1], font, text_color)
        draw_rotated_text(draw, positions["8"][0], "8", positions["8"][1], font, text_color)

        # Draw the date without rotation
        draw.text(positions["date"][0], "2024-09-16", fill=date_color, font=font_date)

    def x_cross_img(self):
        # Load the original image
        original_image_path = "x_cross[1].jpg"
        image = Image.open(original_image_path)

        # Define font for numbers and date with decreased size and bold weight
        try:
            custom_font_path = "Sanujfont.ttf"  # Replace with the path to your custom font file
            font = ImageFont.truetype(custom_font_path, 105)  # Custom font, bold, smaller size
            date_font = ImageFont.truetype(custom_font_path, 40)  # Custom font, bold for date
        except IOError:
            font = ImageFont.load_default()
            date_font = ImageFont.load_default()

        # Define positions for numbers to center them in each square
        image_width, image_height = image.size
        square_size = image_width // 3  # Assuming a 3x3 grid

        positions = {
            "0": (square_size // 2, square_size // 2),
            "3": (2 * square_size + square_size // 2, square_size // 2),
            "2": (square_size + square_size // 2, square_size + square_size // 2),
            "5": (square_size // 2, 2 * square_size + square_size // 2),
            "1": (2 * square_size + square_size // 2, 2 * square_size + square_size // 2),
        }

        # Create a drawing object
        draw = ImageDraw.Draw(image)

        # Draw the numbers on the image centered in each square
        for number, position in positions.items():
            bbox = draw.textbbox((0, 0), number, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            centered_position = (position[0] - text_width // 2, position[1] - text_height // 2)
            draw.text(centered_position, number, font=font, fill="black")

        # Draw the date at the bottom center
        date_text = "2024-09-01"
        date_bbox = draw.textbbox((0, 0), date_text, font=date_font)
        date_width = date_bbox[2] - date_bbox[0]
        date_height = date_bbox[3] - date_bbox[1]
        date_position = ((image_width - date_width) // 2, image_height - date_height - 10)
        draw.text(date_position, date_text, font=date_font, fill="black")

        # Save the edited image
        edited_image_path = "x_cross_edited.jpg"
        image.save(edited_image_path)

        print(f"Edited image saved as {edited_image_path}")





