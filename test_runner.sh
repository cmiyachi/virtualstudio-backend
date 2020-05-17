. setup.sh
export ENV='test'
echo 'DROPPING TABLES... (if any)'
python3 manage.py db downgrade

echo 'CREATING TABLES...'
python3 manage.py db upgrade

echo 'SEEDING TABLES...'
python3 manage.py seed

echo 'RUNNING TEST...'
python3  test.py