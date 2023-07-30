import streamlit as st


def app_header() -> None:
    """Creates page header"""
    title = '<p style="text-align: center; font-family:Arial; color:White; font-size: 60px;">Background remover</p>'
    st.markdown(title, unsafe_allow_html=True)


def create_header(text: str) -> None:
    """Template for creating headers"""
    st.markdown("""<hr style="height:10px;border:0;background-color:White;" /> """, unsafe_allow_html=True)
    subtitle = f'<p style="text-align: center; font-family:Arial; color:White; font-size: 30px;">{text}</p>'
    st.markdown(subtitle, unsafe_allow_html=True)
