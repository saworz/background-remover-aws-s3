import os
from io import BytesIO
import logging
import streamlit as st
import streamlit.runtime.uploaded_file_manager
from .ui import create_header
from .initialization import Paths
from src.features.background_remover import remove_background


def upload_file() -> st.runtime.uploaded_file_manager.UploadedFile:
    """Loads file using built-in streamlit function"""
    st.session_state.display_results = False
    return st.file_uploader('Upload file', type=['jpg', 'jpeg', 'png'])


def display_uploaded_image(image: st.runtime.uploaded_file_manager.UploadedFile) -> None:
    """If loaded, displays uploaded image"""
    show_file = st.empty()
    if not image:
        show_file.info('Please upload a file in the JPG, JPEG or PNG format')

    if isinstance(image, BytesIO):
        show_file.image(image)


def set_threshold() -> float:
    """Sets threshold with built-in streamlit slider"""
    threshold = st.slider('Set threshold', min_value=0.05, max_value=0.99, value=0.5)
    return threshold


def save_uploaded_file(file) -> None:
    """Saves uploaded file locally"""
    filename = file.name

    with open(os.path.join(Paths().inputs_dir, filename), 'wb') as f:
        f.write(file.getbuffer())
    logging.info('Uploaded file saved')


def removing_background_ui() -> None:
    """Creates UI for removing background and displays created images"""
    header_text = 'Upload an image and get .png without the background.'
    create_header(header_text)
    st.session_state.uploaded_image = upload_file()
    display_uploaded_image(st.session_state.uploaded_image)
    st.session_state.threshold = set_threshold()

    if st.button('Delete background', disabled=not st.session_state.uploaded_image):
        save_uploaded_file(st.session_state.uploaded_image)
        st.session_state.mask_image, st.session_state.result_image = remove_background(st.session_state.uploaded_image)
        st.session_state.display_results = True

    if st.session_state.display_results:
        st.image([st.session_state.mask_image, st.session_state.result_image],
                 width=350, caption=['Generated mask', 'Final result'])
