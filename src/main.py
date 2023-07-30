from streamlit_ui.initialization import Paths, initialize_session_state
from streamlit_ui.removing_background import removing_background_ui
from streamlit_ui.ui import app_header
import sys
import logging

sys.path.append(".")
logging.basicConfig(level=logging.INFO)


def main() -> None:
    paths = Paths()
    initialize_session_state()
    paths.create_dirs()
    app_header()
    removing_background_ui()


if __name__ == '__main__':
    main()
