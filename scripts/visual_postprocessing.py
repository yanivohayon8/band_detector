from PIL import Image, ImageDraw
import json

def draw_line_on_image(json_file, image_file, output_file):
    try:
        # Read JSON data
        with open(json_file, 'r') as f:
            data_list = json.load(f)

        # Read the input image
        img = Image.open(image_file)

        # Create a drawing context
        draw = ImageDraw.Draw(img)

        # Draw lines on the image based on the JSON data
        for data in data_list:
            representative_line = data.get('representive_line', [])
            width = data.get('width', 1)

            # for point1, point2 in representative_line:
            draw.line([tuple(representative_line[0]),tuple(representative_line[1])], fill=(0, 0, 255), width=width)

        # Save the new image with the lines drawn on it
        img.save(output_file)

        print(f"Lines drawn and saved to {output_file} successfully.")
    except Exception as e:
        print(f"Error: {e}")
        # sys.exit(1)

