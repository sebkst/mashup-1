
#connect to redis
rserver = redis.StrictRedis(host='localhost', port=6379, db=0)

################################################################################
#   ProgramTask
################################################################################
class Program(Resource):
    """
    Should have defined "save program" "delete program" "load program"
    """
    def get(self, program_id):
        return json.loads(rserver.get('programs:' + program_id))

    def post(self):
        json_data = request.get_json(force=True)
        #increment the progid in redis to create new one and associate it with the new program
        rserver.incr('progid')
        progid = int(rserver.get('progid'))
        #json_data['id'] = progid
        myjson = {}
        myjson['name'] = json_data['name']
        myjson['pdata'] = json_data['pdata']
        myjson['comment'] = json_data['comment']
        #VALIDATE PDATA
        #rserver.set('programs:' + str(program_id), json.dumps(json_data['pdata']))
        rserver.set('programs:' + str(progid), json.dumps(myjson))
        #push on the list keeping all the ids
        rserver.lpush('plist', 'programs:' + str(progid))
        #return the field with the just saved program
        message = json.loads(rserver.get('programs:' + str(progid)))
        message['id'] = progid
        return "PROGRAM SAVED"

    def put(self, program_id):
        json_data = request.get_json(force=True)
        myjson = {}
        myjson['name'] = json_data['name']
        myjson['pdata'] = json_data['pdata']
        myjson['comment'] = json_data['comment']
        rserver.set('programs:' + program_id, json.dumps(myjson))
        return "PROGRAM UPDATED"

    def delete(self, program_id):
        #pipe = rserver.pipeline()
        rserver.delete('programs:' + program_id)
        rserver.lrem('plist',1,'programs:' + program_id)
        return "PROGRAM DELETED"


api.add_resource(Program,'/v1/program','/v1/program/<string:program_id>')

class ProgramsList(Resource):
    def get(self):
        keys = rserver.lrange('plist',0,-1)

        message=[]
        for i,key in enumerate(keys):
            pj = {}
            pj['id'] = key[9:]
            pj['name'] = json.loads(rserver.get(key))['name']
            pj['comment'] = json.loads(rserver.get(key))['comment']
            message.append(pj)

        return message

    def put(self):
        return "UPDATED (JOKE)"

    def post(self,method):
        #http://stackoverflow.com/questions/30491841/python-flask-restful-post-not-taking-json-arguments
        if(method == "create"):
            json_data = request.get_json(force=True)
            #increment the progid in redis to create new one and associate it with the new program
            for progs in json_data:
                rserver.incr('progid')
                progid = int(rserver.get('progid'))
                #json_data['id'] = progid
                myjson = {}
                myjson['name'] = progs['name']
                myjson['pdata'] = progs['pdata']
                myjson['comment'] = progs['comment']
                #VALIDATE PDATA
                #rserver.set('programs:' + str(program_id), json.dumps(json_data['pdata']))
                rserver.set('programs:' + str(progid), json.dumps(myjson))
                #push on the list keeping all the ids
                rserver.lpush('plist', 'programs:' + str(progid))

            return "CONTENT CREATED"
        elif(method == "delete"):
            json_data = request.get_json(force=True)
            for progid in json_data:
                #pipe = rserver.pipeline()
                rserver.delete('programs:' + progid)
                rserver.lrem('plist',1,'programs:' + progid)
            return "CONTENT DELETED"
        else:
            return "Bad request"

api.add_resource(ProgramsList,'/v1/programs','/v1/programs/<string:method>')


################################################################################
#   UploadSequence
################################################################################
class JobSequence(Resource):
    def get(self):
        keys = rserver.lrange('jobsequence',0,-1)

        message={}
        ids=[]
        for i,key in enumerate(keys):
            #pj['ids'] = key
            ids.append(key)
            #pj['name'] = json.loads(rserver.get(key))['name']
            #message.append(pj)

        message['ids'] = ids
        return message

    def post(self):
        #http://stackoverflow.com/questions/10973614/convert-json-array-to-python-list
        json_data = request.get_json(force=True)
        #rserver.set('programs:' + str(program_id), json.dumps(json_data['pdata']))
        #push on the list keeping all the ids
        rserver.delete('jobsequence')

        for i,key in enumerate(json_data):
            rserver.lpush('jobsequence', key)

        steps = json.loads(rserver.get("programs:" + rserver.lindex('jobsequence',-1)))['pdata']
        rserver.set('status:program:name',json.loads(rserver.get("programs:" + rserver.lindex('jobsequence',-1)))['name'])
        rserver.set('status:program:totalsteps',str(len(steps)))
        rserver.set('status:program:step','0')
        #return the field with the just saved program
        #message = json.loads(rserver.get('programs:' + str(progid)))
        #message['pid'] = progid
        return "OK"

api.add_resource(JobSequence, '/v1/jobsequence')

################################################################################
#   Home
################################################################################
class Home(Resource):

    def post(self):

        #SET THE TASK TO START FROM THE CONTROLLER
        rserver.set('command', 'home')
        os.kill(int(rserver.get('PID')), signal.SIGUSR1)
        return "SENT HOME SIGNAL"

api.add_resource(Home, '/v1/home')


################################################################################
#   Start
################################################################################
class Start(Resource):

    def post(self):
        #SEND THE SIGNAL TO START
        rserver.set('command', 'start')
        os.kill(int(rserver.get('PID')), signal.SIGUSR1)
        return "TASK STARTED"

api.add_resource(Start, '/v1/start')


################################################################################
#   Pause
################################################################################
class Pause(Resource):

    def post(self):
        #SEND THE SIGNAL TO PAUSE
        rserver.set('command', 'pause')
        os.kill(int(rserver.get('PID')), signal.SIGUSR1)
        #os.kill(int(rserver.get('PID')), signal.SIGSTOP)
        return "SENT PAUSE SIGNAL"

api.add_resource(Pause, '/v1/pause')

################################################################################
#   Resume
################################################################################
class Resume(Resource):

    def post(self):
        #SEND THE SIGNAL TO STOP
        rserver.set('command', 'resume')
        os.kill(int(rserver.get('PID')), signal.SIGUSR1)
        #os.kill(int(rserver.get('PID')), signal.SIGCONT)
        return "PROCESS RESUMED"

api.add_resource(Resume, '/v1/resume')

################################################################################
#   POTLIFE
################################################################################
class PotReset(Resource):

    def post(self):
        #SEND THE SIGNAL TO STOP
        rserver.set('command', 'potlifereset')
        os.kill(int(rserver.get('PID')), signal.SIGUSR1)
        #os.kill(int(rserver.get('PID')), signal.SIGCONT)
        return "RESTARTING POTLIFE TIMER.."

api.add_resource(PotReset, '/v1/potlife/reset')

class PotExecute(Resource):

    def post(self):
        #SEND THE SIGNAL TO STOP
        rserver.set('command', 'potlifeexecute')
        os.kill(int(rserver.get('PID')), signal.SIGUSR1)
        #os.kill(int(rserver.get('PID')), signal.SIGCONT)
        return "EXECUTE POTLIFE SIGNAL SENT"

api.add_resource(PotExecute, '/v1/potlife/execute')

################################################################################
#   Settings
################################################################################
class Settings(Resource):

    def put(self):
        json_data = request.get_json(force=True)

        rserver.set('settings:valvedelays',float(json_data['valvedelays']))
        rserver.set('settings:homespeed',int(json_data['homespeed']))
        rserver.set('settings:potlife:volume',float(json_data['potvolume']))
        rserver.set('settings:potlife:timer',int(json_data['pottimer']))
        rserver.set('settings:potlife:loop',int(json_data['loop']))

        return "SETTINGS SAVED"

    def get(self):
        return {'valvedelays': float(rserver.get('settings:valvedelays')),
                'homespeed': float(rserver.get('settings:homespeed')),
                'potvolume': float(rserver.get('settings:potlife:volume')),
                'pottimer': int(rserver.get('settings:potlife:timer')),
                'loop': int(rserver.get('settings:loop'))
                }

api.add_resource(Settings, '/v1/settings')

#supported settings
class Setting(Resource):

    def put(self,setting):
        json_data = request.get_json(force=True)
        rserver.set('settings:' + setting, json_data[0])
        return rserver.get('settings:' + setting)

    def get(self,setting):
        return [rserver.get('settings:' + setting)]

api.add_resource(Setting, '/v1/setting/<string:setting>')

################################################################################
#   Status
################################################################################
class Status(Resource):

    def get(self):
        return rserver.get('status:status')

api.add_resource(Status, '/v1/status')


################################################################################
#   Poweroff
################################################################################
class Poweroff(Resource):

    def post(self):
        #SEND THE SIGNAL TO START
        rserver.set('command', 'poweroff')
        os.kill(int(rserver.get('PID')), signal.SIGUSR1)
        return "Poweroff command sent"

api.add_resource(Poweroff, '/v1/poweroff')
