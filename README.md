//setting virtual env for windows
python -m venv .venv
.venv\Scripts\activate


//setting virtual env for macos
python3 -m venv .venv
source .venv/bin/activate


//Requirements File installation
pip install -r requirements.txt



//Code Execution cmd
streamlit run Time_table.py
