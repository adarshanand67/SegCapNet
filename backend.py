from flask import Flask, request, jsonify
from PIL import Image
from backgroundremover.bg import remove
import io
from base64 import encodebytes
from PIL import Image
import base64


from PIL import Image
import io
from base64 import encodebytes

app = Flask(__name__)


def remove_bg(src_img_path, out_img_path):
    """
    Remove the background from an image using the specified model.

    Args:
        src_img_path (str): The path to the source image file.
        out_img_path (str): The path to save the output image file.

    Returns:
        None
    """
    model_choices = ["u2net", "u2net_human_seg", "u2netp"]
    with open(src_img_path, "rb") as f:
        data = f.read()
    img = remove(data, model_name=model_choices[0],
                 alpha_matting=True,
                 alpha_matting_foreground_threshold=240,
                 alpha_matting_background_threshold=10,
                 alpha_matting_erode_structure_size=10,
                 alpha_matting_base_size=1000)
    with open(out_img_path, "wb") as f:
        f.write(img)



def get_response_image(image_path):
    """
    Converts an image to a base64-encoded string.

    Args:
        image_path (str): The path to the image file.

    Returns:
        str: The base64-encoded image string.
    """
    pil_img = Image.open(image_path, mode='r')
    pil_img = pil_img.convert('RGB')
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='JPEG')
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii')
    return encoded_img


@app.route("/process_image", methods=["POST"])
def process_image():
    """
    Process the uploaded image by removing the background and returning the result.

    Returns:
        A JSON response containing the status code and the encoded image bytes.
    """
    image_file = request.json['image']

    decoded_image = base64.b64decode((image_file))

    image_path = 'input.jpeg'
    output_path = 'output.jpeg'

    with open(image_path, 'wb') as f:
        f.write(decoded_image)

    remove_bg(image_path, output_path)

    encoded_image = get_response_image('output.jpeg')
    response = {'status_code': 200, 'ImageBytes': encoded_image}

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
