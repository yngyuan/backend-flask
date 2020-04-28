from flask_restful import Resource
from flask import request, render_template, make_response, session, redirect, jsonify
from models.user_db_api import user_db_api
from models.report_db_api import report_db_api, ObjectId
from models.theme_db_api import theme_db_api
from flask_jwt_extended import jwt_required
import logging
import cv2, base64
import math

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

class ShareMobile(Resource):

    def __init__(self):
        self.log = logging
        self.log.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

    def post(self):
        data = request.get_json()
        img_src = data['uri']
        description = data['description']
        
        cap = cv2.VideoCapture(img_src)
        if (cap.isOpened()):
            ret, img = cap.read()  
        height, width, channels = img.shape
        self.log.debug("height " + str(height) + " width " + str(width) + " description " + str(len(description)))
        
        #add padding to the bottom
        # specify the font and draw the key using puttext
        font = cv2.FONT_HERSHEY_DUPLEX
        #copyMakeBorder( src, dst, top, bottom, left, right, borderType, value )
        #cv2.putText(image, text, org, font, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]])
        if len(description)*20 > width*2:
            img = cv2.copyMakeBorder(img, 0, math.floor(height*0.4 + 0.5), 0, 0, cv2.BORDER_CONSTANT, None, [255, 255, 255])
            cv2.putText(img, description[:math.floor(width/20+0.5)], (math.floor(width*0.05 + 0.5), math.floor(height*1.15 + 0.5)), font, 1, (0, 0, 0), 1, cv2.LINE_AA) 
            cv2.putText(img, description[math.floor(width/20+0.5):math.floor(width/20+0.5)*2], (math.floor(width*0.05 + 0.5), math.floor(height*1.21 + 0.5)), font, 1, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(img, description[math.floor(width/20+0.5)*2:], (math.floor(width*0.05 + 0.5), math.floor(height*1.27 + 0.5)), font, 1, (0, 0, 0), 1, cv2.LINE_AA)  
        elif len(description)*20 > width:
            img = cv2.copyMakeBorder(img, 0, math.floor(height*0.4 + 0.5), 0, 0, cv2.BORDER_CONSTANT, None, [255, 255, 255])
            cv2.putText(img, description[:math.floor(width/20+0.5)], (math.floor(width*0.05 + 0.5), math.floor(height*1.15 + 0.5)), font, 1, (0, 0, 0), 1, cv2.LINE_AA) 
            cv2.putText(img, description[math.floor(width/20+0.5):], (math.floor(width*0.05 + 0.5), math.floor(height*1.21 + 0.5)), font, 1, (0, 0, 0), 1, cv2.LINE_AA) 
        else:
            img = cv2.copyMakeBorder(img, 0, math.floor(height*0.2 + 0.5), 0, 0, cv2.BORDER_CONSTANT, None, [255, 255, 255])
            cv2.putText(img, description, (math.floor(width*0.05 + 0.5), math.floor(height*1.1 + 0.5)), font, 1, (0, 0, 0), 1, cv2.LINE_AA) 
        
        # compress the image and send response
        ret, jpeg = cv2.imencode('.png', img)
        response = make_response(jsonify({"image" : str(base64.b64encode(jpeg))}))
        #response = make_response(jpeg.tobytes())
        #response.headers['Content-Type'] = 'image/png'
        return response
        #self.log.debug(str(len(themes)) + " themes " + str(len(reports)) + " reports")
        #return make_response(jsonify({'themes': themes, 'lists': reports, 'length': len(reports)}), 200)
