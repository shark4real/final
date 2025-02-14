import os
import io
import math
import base64
from flask import Flask, render_template, jsonify
from PIL import Image, ImageDraw
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

def draw_geometric_flower():
    try:
        # Create a new image with a black background
        img = Image.new('RGB', (400, 400), 'black')
        draw = ImageDraw.Draw(img)

        # Set drawing parameters
        center_x, center_y = 200, 200
        petal_size = 80
        num_petals = 12
        images = []

        # Create frames for animation
        for frame in range(num_petals + 1):  # +1 to show complete flower at end
            frame_img = Image.new('RGB', (400, 400), 'black')
            frame_draw = ImageDraw.Draw(frame_img)

            # Draw multiple layers of petals
            for layer in range(3):  # Three layers of petals
                current_size = petal_size - (layer * 20)  # Decrease size for inner layers

                # Draw petals up to current frame
                for i in range(min(frame, num_petals)):
                    angle = (i * 360 / num_petals)
                    rad = math.radians(angle)

                    # Calculate base petal points
                    x1 = center_x + (current_size * math.cos(rad))
                    y1 = center_y + (current_size * math.sin(rad))

                    # Calculate control points for curved edges
                    control_rad1 = rad + math.pi/4  # 45 degrees offset for curve control
                    control_rad2 = rad - math.pi/4  # -45 degrees offset for curve control

                    # Control points for the curved edges
                    ctrl_x1 = center_x + (current_size * 0.8 * math.cos(control_rad1))
                    ctrl_y1 = center_y + (current_size * 0.8 * math.sin(control_rad1))

                    ctrl_x2 = center_x + (current_size * 0.8 * math.cos(control_rad2))
                    ctrl_y2 = center_y + (current_size * 0.8 * math.sin(control_rad2))

                    # Base point near center for petal
                    base_x = center_x + (current_size * 0.2 * math.cos(rad))
                    base_y = center_y + (current_size * 0.2 * math.sin(rad))

                    # Draw curved petal outline
                    points = []
                    steps = 20  # Number of points to create smooth curve

                    # Create first curve
                    for t in range(steps + 1):
                        t = t / steps
                        # Quadratic Bézier curve formula
                        bx = (1-t)**2 * base_x + 2*(1-t)*t * ctrl_x1 + t**2 * x1
                        by = (1-t)**2 * base_y + 2*(1-t)*t * ctrl_y1 + t**2 * y1
                        points.append((bx, by))

                    # Create second curve
                    for t in range(steps, -1, -1):
                        t = t / steps
                        bx = (1-t)**2 * base_x + 2*(1-t)*t * ctrl_x2 + t**2 * x1
                        by = (1-t)**2 * base_y + 2*(1-t)*t * ctrl_y2 + t**2 * y1
                        points.append((bx, by))

                    # Draw petal with gradient colors
                    frame_draw.polygon(
                        points, 
                        fill=None, 
                        outline=f"rgb({255-layer*30}, {105+layer*30}, {180-layer*30})"
                    )

            # Add frame to animation
            images.append(frame_img)

        # Save animation as base64
        buffer = io.BytesIO()
        images[0].save(
            buffer,
            format='GIF',
            save_all=True,
            append_images=images[1:],
            duration=200,  # Slower animation: 200ms per frame
            loop=0
        )
        image_base64 = base64.b64encode(buffer.getvalue()).decode()

        return image_base64

    except Exception as e:
        logger.error(f"Error in draw_geometric_flower: {str(e)}")
        raise

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/draw-flower')
def get_flower():
    try:
        image_base64 = draw_geometric_flower()
        return jsonify({'status': 'success', 'image': image_base64})
    except Exception as e:
        logger.error(f"Error drawing flower: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500