import streamlit.components.v1 as components
import os

_component_func = components.declare_component(
    "qr_scanner",
    path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend")
)

def qr_scanner(key=None):
    """Create a new instance of "qr_scanner".
    Returns:
        str: The decoded QR code text, or None if nothing detected yet.
    """
    return _component_func(key=key)
