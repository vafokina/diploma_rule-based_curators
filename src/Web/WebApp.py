import threading, logging
from flask import Flask, jsonify, make_response, request, abort
from flask_cors import cross_origin

from Components.ControlSystem import ControlSystem

class WebApp:

    def __init__(self, controlSystem: ControlSystem):
        self.app = Flask(__name__)
        self.controlSystem = controlSystem

        self.log = logging.getLogger('werkzeug')
        self.log.setLevel(logging.ERROR)
        #self.log.disabled = True

        @self.app.route('/api', methods=['GET'])
        @cross_origin() 
        def getAll():
            ids = self.controlSystem.logHolder.curators.keys()
            data = {}
            data['generalLog'] = self.controlSystem.getGeneralCuratorLog()
            curators = []
            for id in ids:
                curators.append({
                    'id': id,
                    'type': self.controlSystem.logHolder.curators[id].type,
                    'state': self.controlSystem.getFullCuratorState(id),
                    'log': self.controlSystem.getCuratorLog(id)
                })
            data['curators'] = curators
            return make_response(jsonify(data), 200)

        @self.app.route('/api/curators', methods=['GET']) 
        @cross_origin() 
        def getCurators():
            data = self.controlSystem.getCurators()
            return make_response(jsonify(data), 200)

        @self.app.route('/api/state/<int:id>', methods=['GET']) 
        @cross_origin() 
        def getState(id):
            data = self.controlSystem.getFullCuratorState(id)
            return make_response(jsonify(data), 200)

        @self.app.route('/api/log/<int:id>', methods=['GET']) 
        @cross_origin() 
        def getLog(id):
            data = self.controlSystem.getCuratorLog(id)
            return make_response(jsonify(data), 200)

        @self.app.route('/api/generalLog', methods=['GET']) 
        @cross_origin() 
        def getGeneralLog():
            data = self.controlSystem.getGeneralCuratorLog()
            return make_response(jsonify(data), 200)

        @self.app.route('/api/event', methods=['POST']) 
        @cross_origin() 
        def postEvent():
            if not request.is_json:
                abort(400)
            data = request.get_json()
            if not 'factName' in data or type(data['factName']) is not str:
                abort(400)
            if not 'fact' in data or type(data['fact']) is not dict:
                abort(400)
            
            res = self.controlSystem.sendEvent(request.json['factName'],  request.json['fact'])
            if res == False:
                return make_response(jsonify({'error': 'Can not find generator'}), 500)
            return make_response('', 200)
        
        @self.app.route('/api/event', methods=['GET'])
        @cross_origin() 
        def putGenerate():
            generate = request.args.get('generate').lower()
            if generate == 'true':
                res = self.controlSystem.sendGenerateCommand(True)
            elif generate == 'false':
                res = self.controlSystem.sendGenerateCommand(False)
            else:
                return make_response(jsonify({'error': 'Can not resolve generate value'}), 500)
            if res == False:
                return make_response(jsonify({'error': 'Can not find generator'}), 500)
            return make_response('', 200)
    
    def runServerInAnotherThread(self):
        thread = threading.Thread(target=self.runServer, daemon=True)
        thread.name = 'WebServerThread'
        thread.start()

    def runServer(self):
        self.app.run(host='0.0.0.0', port=8080)

   
    


