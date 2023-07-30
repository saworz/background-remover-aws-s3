from pathlib import Path
import streamlit as st
import logging

from os.path import dirname, abspath
import inspect
import sys

current_dir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parent_dir = dirname(dirname(current_dir))
sys.path.insert(0, parent_dir)


class CommonPaths:
    """Contains and creates paths to directories used in other parts of program"""
    def __init__(self) -> None:
        self.temp_dir = Path(__file__).parents[2] / 'data' / 'temp'
        self.inputs_dir = self.temp_dir / 'inputs'
        self.masks_dir = self.temp_dir / 'masks'
        self.results_dir = self.temp_dir / 'results'

    @st.cache_data
    def create_dirs(_self) -> None:
        """Works only once, creates directories to store temporary images"""
        logging.info('Creating required directories')
        Path(_self.inputs_dir).mkdir(parents=True, exist_ok=True)
        Path(_self.masks_dir).mkdir(parents=True, exist_ok=True)
        Path(_self.results_dir).mkdir(parents=True, exist_ok=True)


@st.cache_data
def initialize_session_state() -> None:
    """Works only once, initializes session state variables used in program"""
    logging.info('Initialization of st.session.state')
    st.session_state.uploaded_image = None
    st.session_state.display_results = False
    st.session_state.mask_image = None
    st.session_state.result_image = None
    st.session_state.files_list = []
    st.session_state.requested_filename = ''
    st.session_state.image_to_crop = None
    st.session_state.cropped_image = None
