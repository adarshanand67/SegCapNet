from serpapi import GoogleSearch
import torch
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import gradio as gr
import requests
import io
import base64
from base64 import encodebytes

API_KEY = "9023d4dbcce2c3e065d7983a642218de01ad8c1cc6a9f556d6dd6bd7351943af"

processor = BlipProcessor.from_pretrained(
    "salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained(
    "salesforce/blip-image-captioning-base")


def get_response_image(image):
    """
    Converts a NumPy array image to a base64 encoded string.

    Parameters:
    image (numpy.ndarray): The input image as a NumPy array.

    Returns:
    str: The base64 encoded string representation of the image.
    """
    pil_image = Image.fromarray(image)
    byte_arr = io.BytesIO()
    pil_image.save(byte_arr, format='JPEG')
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii')
    return encoded_img


def image_captioning(image):
    """
    Generates a caption for the given image using an API.

    Args:
        image: The input image for which the caption needs to be generated.

    Returns:
        If the API call is successful, returns a PIL image object with the generated caption.
        If the API call fails, returns an error message.

    Raises:
        None
    """
    api_url = "http://127.0.0.1:5000/process_image"
    encoded_input = get_response_image(image)

    files = {"image": encoded_input}
    response = requests.post(api_url, json=files)
    response_json = response.json()
    encoded_image = response_json['ImageBytes']

    if response.status_code == 200:
        decoded_image = base64.b64decode(encoded_image)
        pil_image = Image.open(io.BytesIO(decoded_image))
        return pil_image
    else:
        return "Error: Unable to generate caption"


def generate_caption(image):
    """
    Generates a caption for the given image using image captioning model.

    Args:
        image: The input image for which the caption needs to be generated.

    Returns:
        The generated caption for the image.
    """
    global caption
    segmented_image = image_captioning(image)
    inputs = processor(images=segmented_image, text="", return_tensors="pt")
    with torch.no_grad():
        outputs = model.generate(**inputs)
    caption = processor.decode(outputs[0], skip_special_tokens=True)
    return caption


iface1 = gr.Interface(
    generate_caption,
    gr.Image(),
    "text",
    title="Image Captioning",
    description="Generate a caption for an image.",
)


def display_products(input_text):
    """
    Display products based on the given search parameters.

    Returns:
        str: A string containing HTML markup for displaying the products.
    """
    params = {
        "engine": "google_shopping",
        "q": caption,
        "location": "Bengaluru, Karnataka, India",
        "google_domain": "google.com",
        "gl": "in",
        "hl": "en",
        "api_key": API_KEY,
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    shopping_results = results["shopping_results"]
    shopping_results = shopping_results[:min(15, len(shopping_results))]

    ListOfThumbnails = [items.get('thumbnail') for items in shopping_results]
    ListOfTitles = [items.get('title') for items in shopping_results]
    ListOfPrices = [items.get('price') for items in shopping_results]
    ListOfLinks = [items.get('link') for items in shopping_results]
    ListOfStores = [items.get('source') for items in shopping_results]

    product_display = ""
    for i in range(len(ListOfThumbnails)):
        product_display += f"<img src='{ListOfThumbnails[i]}' width=200><br>"
        product_display += f"<b>Title:</b> {ListOfTitles[i]}<br>"
        product_display += f"<b>Price:</b> {ListOfPrices[i]}<br>"
        product_display += f"<b>Store:</b> {ListOfStores[i]}<br>"
        product_display += f"<a href='{ListOfLinks[i]}' target='_blank'>Link</a><br><br>"

    return product_display


iface2 = gr.Interface(
    fn=display_products,
    inputs=gr.Textbox(lines=2, label="Caption"),
    outputs="html",
    title="Google Shopping Search",
    description="Enter the product you want to search for",
    allow_flagging=False,
    theme="huggingface",
)

demo = gr.TabbedInterface(
    [
        iface1,
        iface2
    ],
    [
        "Image Captioning",
        "Google Shopping Search"
    ]
)

demo.launch(share=True)

