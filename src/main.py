from streamlit_ui.initialization import CommonPaths, initialize_session_state
from streamlit_ui.removing_background import removing_background_ui
from streamlit_ui.ui import app_header
from streamlit_ui.reading_data_from_s3 import reading_data_from_s3_ui
from streamlit_ui.cropping_images_utils import crop_image_ui

import logging
import streamlit as st
from src.features.aws_client import AwsClient

logging.basicConfig(level=logging.INFO)


@st.cache_resource
def init_aws_client(bucket: str) -> AwsClient:
    """Works once, creates AwsClient instance"""
    logging.info('Creating AwsClient instance')
    return AwsClient(bucket)


def main() -> None:
    paths = CommonPaths()
    initialize_session_state()
    paths.create_dirs()
    aws_client = init_aws_client('backgr-remover-swz')
    app_header()
    removing_background_ui()
    reading_data_from_s3_ui(aws_client)
    crop_image_ui(aws_client)


if __name__ == '__main__':
    main()
