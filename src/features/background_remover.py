from skimage import io, transform
from io import BytesIO
import cv2
import numpy as np
import streamlit.runtime.uploaded_file_manager
import torch
import streamlit as st
from PIL import Image
from src.streamlit_ui.initialization import Paths
from src.model.model import load_model


def open_image(image: st.runtime.uploaded_file_manager.UploadedFile) -> bytearray:
    """Loads local image"""
    if isinstance(image, BytesIO):
        with open(Paths().inputs_dir / st.session_state.uploaded_image.name, 'rb') as image:
            f = image.read()
            return bytearray(f)


def transform_image(bytes_img) -> torch.FloatTensor:
    """Transforms image to be compatible model input"""
    def normalize(input_image: cv2.imdecode) -> torch.Tensor:
        """Normalizes color channels"""
        resized_image = transform.resize(input_image, (320, 320), mode='constant')
        temp_img = np.zeros((resized_image.shape[0], resized_image.shape[1], 3))

        temp_img[:, :, 0] = (resized_image[:, :, 0] - 0.485) / 0.229
        temp_img[:, :, 1] = (resized_image[:, :, 1] - 0.456) / 0.224
        temp_img[:, :, 2] = (resized_image[:, :, 2] - 0.406) / 0.225

        temp_img = temp_img.transpose((2, 0, 1))
        temp_img = np.expand_dims(temp_img, 0)
        return torch.from_numpy(temp_img)

    np_arr = np.frombuffer(bytes_img, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    image = normalize(image)
    return image.type(torch.FloatTensor)


def apply_threshold(input_pred: torch.Tensor, threshold: float) -> torch.Tensor:
    """Applies set threshold on model's output"""
    pred = input_pred[:, 0, :, :]
    pred_max = torch.max(pred)
    pred_min = torch.min(pred)
    pred = (pred - pred_min) / (pred_max - pred_min)

    return torch.from_numpy(np.where(pred > threshold, 1, 0))


def get_images_from_model_output(results: torch.Tensor) -> tuple[np.array, np.array]:
    """Model's output postprocessing to get mask and image with no background"""
    results_np = results.squeeze().cpu().data.numpy()
    raw_img_path = Paths().inputs_dir / st.session_state.uploaded_image.name

    img = Image.fromarray((results_np * 255).astype(np.uint8)).convert('RGB')
    input_image = io.imread(str(raw_img_path))
    mask = img.resize((input_image.shape[1], input_image.shape[0]))

    mask = np.array(mask)[:, :, 0]
    mask = np.expand_dims(mask, axis=2)
    image_out = np.concatenate((input_image, mask), axis=2)
    return mask, image_out


def remove_background(image) -> tuple[np.array, np.array]:
    """Removes background from an image, returns mask and image without background"""
    model = load_model()
    bytes_img = open_image(image)
    results = model(transform_image(bytes_img))[0]
    results = apply_threshold(results, st.session_state.threshold)
    return get_images_from_model_output(results)
