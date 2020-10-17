rm ./log.txt
export FLASK_APP=gameRec
nohup python3 -m flask run --host=0.0.0.0 >> ./log.txt 2>&1 &

