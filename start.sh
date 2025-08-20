#!/bin/bash
mkdir -p ~/.streamlit/
echo "\
[server]\n\
port = \$PORT\n\
address = \"0.0.0.0\"\n\
headless = true\n\
enableCORS = false\n\
enableXsrfProtection = false\n\
" > ~/.streamlit/config.toml

streamlit run web_app.py 