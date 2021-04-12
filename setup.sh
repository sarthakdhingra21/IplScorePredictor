mkdir -p ~/.streamlit/
echo "[theme]
primaryColor="#f63366"
backgroundColor="#0e1117"
secondaryBackgroundColor="#31333F"
textColor="#fafafa"
font="sans serif"
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
