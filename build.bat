@ECHO OFF

pip install -r requirements.txt

python src/builders/build_db.py
python src/builders/populate_db.py