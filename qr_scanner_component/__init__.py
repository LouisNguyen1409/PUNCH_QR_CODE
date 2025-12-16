import streamlit.components.v1 as components
import os

_component_func = components.declare_component(
    "qr_scanner",
    path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend")
)

def qr_scanner(expected_match=None, key=None):
    """Create a new instance of "qr_scanner".
    
    Args:
        expected_match (str): The value to compare against. If set, JS will play OK/Sai audio internally.
        key (str): Unique key for the component.
        
    Returns:
        str: The decoded QR code text, or None if nothing detected yet.
    """
    return _component_func(expected_match=expected_match, key=key)