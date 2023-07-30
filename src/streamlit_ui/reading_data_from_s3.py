from src.streamlit_ui.ui import create_header
import streamlit as st
from src.features.aws_client import AwsClient


def display_data_in_columns(files: list[str]) -> None:
    """Displays list of files in 3 columns"""
    columns = st.columns(5)
    current_col = 1

    for file in files:
        match current_col:
            case 1:
                with columns[0]:
                    st.markdown('- ' + file)
                    current_col = 3
            case 3:
                with columns[2]:
                    st.markdown('- ' + file)
                    current_col = 5
            case 5:
                with columns[4]:
                    st.markdown('- ' + file)
                    current_col = 1


def reading_data_from_s3_ui(aws_client: AwsClient) -> None:
    """Creates user interface and handles reading data from S3 bucket"""
    text = 'Press to read all files in the Amazon S3 bucket service.'
    create_header(text)

    columns = st.columns(5)
    with columns[2]:
        if st.button('Read data from S3'):
            files_list = aws_client.get_files_list()
            st.session_state.files_list = files_list

    if len(st.session_state.files_list) != 0:
        display_data_in_columns(st.session_state.files_list)
