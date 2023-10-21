from nudenet import NudeDetector
from flask import Flask,request,jsonify
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

@app.route("/check_nsfw",methods=["POST"])
def home():
    if not os.path.exists('images'):
        print("images klasörü yok")
    # if "image" not in request.files:
    #     return jsonify({'error':"No image file provided"},{"isSafe":False})
    # f = request.files['image']
    # f.save('images/{filename}'.format(filename=f.filename))
    # try:
    #     result=nsfwCheck('images/{filename}'.format(filename=f.filename))
    # except Exception as e:
    #     return jsonify({"error":e},{"isSafe":False})

    # os.remove('images/{filename}'.format(filename=f.filename))
    # return jsonify(result)
