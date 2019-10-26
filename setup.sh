<<<<<<< HEAD
mkdir -p ~/.streamlit/
echo "\
[general]\n\
email = \"email@website.com\"\n\
" > ~/.streamlit/credentials.toml
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
=======
mkdir -p ~/.streamlit/
echo "\
[general]\n\
email = \"email@website.com\"\n\
" > ~/.streamlit/credentials.toml
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
>>>>>>> 33a962bcea60f5ec8cd27ac3ef64df461ef3617c
" > ~/.streamlit/config.toml