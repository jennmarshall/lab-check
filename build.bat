@ECHO OFF

pip install -r requirements.txt

python src/builders/build-db.py
python src/builders/populate-db.py