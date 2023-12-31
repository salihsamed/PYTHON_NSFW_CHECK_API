from nudenet import NudeDetector
from flask import Flask,request,jsonify
from flask_cors import CORS
import os

nude_detector = NudeDetector()
forbiddens=["ANUS EXPOSED","BUTTOCKS_EXPOSED","FEMALE_BREAST_EXPOSED","MALE_GENITALIA_EXPOSED","FEMALE_GENITALIA_EXPOSED"]

def nsfwCheck(image):
    isSafe=True
    data=nude_detector.detect(image)
    tempArr=[]
    for val in data:
        tempArr.append({val["class"]:val["score"]})
        for forbidden in forbiddens:
            if(val["class"]==forbidden and float(val["score"])>0.5):
                isSafe=False


    return [{"FORBIDDEN EXPOSES":tempArr},{"isSafe":isSafe}]


app=Flask(__name__)
CORS(app)

@app.route("/check_nsfw",methods=["POST"])
def home():
    if "image" not in request.files:
        return jsonify({'error':"No image file provided"},{"isSafe":False})
    f = request.files['image']
    f.save('{filename}'.format(filename=f.filename))
    try:
        result=nsfwCheck('{filename}'.format(filename=f.filename))
    except Exception as e:
        return jsonify({"error":e},{"isSafe":False})

    os.remove('{filename}'.format(filename=f.filename))
    return jsonify(result)
