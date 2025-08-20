#!/bin/bash
export PORT=8080
export STREAMLIT_SERVER_PORT=8080
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export STREAMLIT_SERVER_HEADLESS=true

streamlit run web_app.py --server.port $PORT --server.address $STREAMLIT_SERVER_ADDRESS --server.headless $STREAMLIT_SERVER_HEADLESS 