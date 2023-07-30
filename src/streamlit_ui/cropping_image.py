import streamlit as st
from src.streamlit_ui.ui import create_header
from src.features.aws_client import AwsClient
from PIL import Image


def get_coordinates(max_x: int, max_y: int) -> tuple[int, int, int, int]:
    """Creates number inputs for cropping coordinates"""
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        x0 = st.number_input(label='x0', min_value=0, max_value=max_x)
    with col2:
        y0 = st.number_input(label='y0', min_value=0, max_value=max_y)
    with col3:
        x1 = st.number_input(label='x1', min_value=0, max_value=max_x)
    with col4:
        y1 = st.number_input(label='y1', min_value=0, max_value=max_y)

    return x0, y0, x1, y1


def preview_image(x0: int, y0: int, x1: int, y1: int) -> Image:
    """Displays cropped image"""
    cropped_img = st.session_state.image_to_crop.crop((x0, y0, x1, y1))
    st.columns(5)[1].image(cropped_img, width=350, caption='Cut preview')
    return cropped_img


def crop_image_ui(aws_client: AwsClient) -> None:
    """Creates UI for image cropping and invoking lambda function"""
    text = "Enter filename and two diagonal positions of the image to be cut."
    create_header(text)
    st.session_state.requested_filename = st.text_input(label="Enter file name")

    if st.columns(5)[2].button('Get image', disabled=len(st.session_state.requested_filename) == 0):
        image = aws_client.get_image_from_s3(st.session_state.requested_filename)
        st.session_state.image_to_crop = image

    if st.session_state.image_to_crop:
        w, h = st.session_state.image_to_crop.size
        st.columns(5)[1].image(st.session_state.image_to_crop, width=350, caption=f"Downloaded image, size {w}x{h}")
        x0, y0, x1, y1 = get_coordinates(w, h)

        col1, col2, col3, col4 = st.columns(4)
        with col2:
            if st.button('Apply & preview'):
                st.session_state.cropped_image = preview_image(x0, y0, x1, y1)

        with col3:
            if st.button('Save image to S3', disabled=not st.session_state.cropped_image):
                aws_client.lambda_crop_image(st.session_state.requested_filename, [x0, y0, x1, y1])
