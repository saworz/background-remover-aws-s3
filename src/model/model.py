import streamlit as st
from .u2net import U2NET
import os
from pathlib import Path
import torch
import logging


@st.cache_data
def load_model() -> U2NET:
    """Loads model's weights only on the first run"""

    current_dir = os.path.dirname(__file__)

    logging.info("Loading model...")
    model_name = 'u2net'
    model_dir = os.path.join(
        Path(current_dir).parents[1], 'saved_models',
        model_name, model_name + '.pth')

    net = U2NET(3, 1)
    net.load_state_dict(torch.load(model_dir, map_location='cpu'))

    logging.info("Model loaded on cpu.")
    return net
