from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
from flask.views import MethodView
import os
from flask.ext.cors import CORS
from collections import OrderedDict
import json
from datetime import timedelta
import random
from datetime import datetime

#Instantiate app
application = Flask(__name__)

#Apply CORS
CORS(application)

#Instantiate api
api = Api(application)

#Load all the answers and questions
ifile = open("aq.txt")

data=json.load(ifile)


class QuestionsDealer(Resource):
    def get(self):

        random.seed(datetime.now())
        question=random.choice(data)

        message=[]
        message.append(question['id'])
        message.append(question['question'])
        message.append(question['choices'])

        return message

    def post(self):
        #http://stackoverflow.com/questions/10973614/convert-json-array-to-python-list
        json_data = request.get_json(force=True)
        #rserver.set('programs:' + str(program_id), json.dumps(json_data['pdata']))
        #push on the list keeping all the ids

        if( json_data['answer'] == data[int(json_data['id'])]['answer'] ):
            return "CORRECT"
        else:
            return "WRONG"

api.add_resource(QuestionsDealer, '/questions')
