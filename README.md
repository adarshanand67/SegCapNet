# Abstract

This project is an Image Search System that employs advanced image segmentation and caption generation techniques. It enables users to upload images and receive relevant product suggestions based on similarities in the generated captions.

## Installation

To install the project, follow these steps:

1. Clone the repository:

2. Navigate to the project directory:

3. Install dependencies:

```python
pip install -r requirements.txt
```

4. Run the backend.py server:

```python
python backend.py
```

5. Run the frontend interface:

```python
gradio frontend.py
```

After running frontend, upload image of the product you want to search for and click on search button. The model will generate the caption for the image, then copy the image and paste it in the search bar and click on search button. The model will search for the similar products and display the results.

## Tech Stack

- Python
- Gradio
- Segmentation Models
- Salesforce BLIP
- TensorFlow
- **Hugging Face Transformers**

## Optimizations

The development methodology of this image search system is comprehensive and involves several key steps:

1. **Image Segmentation**: The system begins with the implementation of an image segmentation model using the U2-Net architecture. This model is trained on a dataset containing images and their corresponding masks, allowing it to segment the images effectively.

2. **Caption Generation**: Following successful segmentation, the system utilizes the Salesforce BLIP Transformer for caption generation. The BLIP model is fine-tuned on a fashion product dataset consisting of segmented images paired with captions. This process leverages the learned representations from both image and text modalities to generate descriptive captions for segmented images.

3. **Integration with Gradio**: Gradio, a user-friendly library for building web-based applications with machine learning models, is integrated into the system. An intuitive user interface is designed to allow users to upload images for segmentation and caption generation. On the backend, functionality is developed to process uploaded images, perform segmentation using the trained U-Net model, and generate captions using the fine-tuned BLIP model. Real-time inference capabilities ensure prompt feedback to users upon image submission.

4. **Product Search Mechanism**: Once the system is capable of segmenting images and generating captions in real-time, a mechanism for searching similar products based on the generated captions is implemented. This involves tokenizing the captions to extract meaningful tokens representing product attributes. These tokens are then transformed into feature representations, and a similarity search mechanism is implemented to retrieve products with similar features.

## File Structure
```
.
├── README.md
├── backend.py
├── bg.py
├── cmd
│   ├── cli.py
│   └── server.py
├── final.ipynb
├── flagged
├── frontend.py
├── github.py
├── models
│   ├── u2aa
│   ├── u2ab
│   ├── u2ac
│   ├── u2ad
│   ├── u2haa
│   ├── u2hab
│   ├── u2hac
│   ├── u2had
│   └── u2netp.pth
├── out.txt
├── requirements.txt
├── u2net
│   ├── data_loader.py
│   ├── detect.py
│   └── u2net.py
└── utilities.py

4 directories, 23 files
```

## Assets

- [Slides](https://docs.google.com/presentation/d/1jWnSKEZwkR7TFKF6CKk4FsvzkKxcxsTkeVn0Zi_GVgo/edit?usp=sharing)

- [Research Paper](https://drive.google.com/file/d/1wVwc-aCXEQR6S_1Aa6yJ5-8heb7e-I9p/view?usp=sharing)

- [Video](https://drive.google.com/file/d/1CW_cH9Ux6eAjOsfyxthEosLrhofPKqUp/view?resourcekey)

## References

- [U2-Net: Going Deeper with Nested U-Structure for Salient Object Detection](https://arxiv.org/pdf/2005.09007)
- [BLIP: Bootstrapping Language-Image Pre-training for
  Unified Vision-Language Understanding and Generation](https://arxiv.org/pdf/2201.12086)

## Authors

- Adarsh Anand
- Aniket Chaudhari
- Rajat Singh
- Vivek Bandrele
