from flask import Flask, request, jsonify, Response
from flask_cors import CORS 
from flask_caching import Cache
from model import RefugeeRegistration
from database import db, init_db 
from config import Config
from datetime import datetime

app = Flask(__name__)

app.config.from_object(Config)
cache = Cache(app)
CORS(app, resources={r"/*": {"origins": Config.CORS_ORIGINS}})
init_db(app)



@app.route('/', methods = ['GET'])
def index():
    return jsonify({"message":"It Works!!"})



@app.route('/api/v1/RefugeeRegistrations', methods = ['POST'])
def createRefugee():
    data = request.get_json()
    required_fields = ['camp', 'firstName', 'lastName', 'dateOfBirth', 'sex', 
                      'placeOfBirth', 'nationality', 'householdSize']
    
    for field in required_fields:
        if field not in data:
            return jsonify({"error":f"missing required field {field}"}), 400
    try:
        if 'dateOfBirth' in data and isinstance(data['dateOfBirth'], str):
            data['dateOfBirth'] = datetime.fromisoformat(data['dateOfBirth'])  
        
        refugee = RefugeeRegistration(**data)
        db.session.add(refugee)
        db.session.commit()
        cache.clear()
        return jsonify(refugee.serialize()), 201
    except Exception as e:
        db.session.rollback()
        app.logger.error(str(e))
        return jsonify({"error":str(e)}), 500
    

@app.route('/api/v1/RefugeeRegistrations', methods = ['GET'])
@cache.cached(timeout = 300, query_string = True)
def getAllRefugees():
    page = request.args.get('page', 1, type = int)
    per_page = request.args.get('per_page', 50, type = int)
    
    refugees = RefugeeRegistration.query.paginate(
        page = page, 
        per_page = per_page,
        error_out = False
    )
    
    return jsonify({
            'refugees': [refugee.serialize() for refugee in refugees.items],
            'total': refugees.total,
            'pages': refugees.pages,
            'current_page': page
        }), 200
    
    
@app.route('/api/v1/RefugeeRegistrations/<int:ref_id>', methods = ['GET'])
def GetRefugeeByID(ref_id):
    refugee = RefugeeRegistration.query.get(ref_id)
    if not refugee:
        return jsonify({"error":"record not found"}), 404
    
    return jsonify(refugee.serialize()), 200


@app.route('/api/v1/RefugeeRegistrations/<int:ref_id>', methods=['PUT'])
def updateRefugee(ref_id):
    refugee = RefugeeRegistration.query.get(ref_id)
    if not refugee:
        return jsonify({"error": "record not found"}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "no data provided"}), 400
    
    try:
        # Update all provided fields
        for key, value in data.items():
            if hasattr(refugee, key) and key != 'id':  # Don't allow ID changes
                setattr(refugee, key, value)
        
        db.session.commit()
        cache.clear()
        return jsonify(refugee.serialize()), 200
    
    except Exception as e:
        db.session.rollback()
        app.logger.error(str(e))
        return jsonify({"error": str(e)}), 500



@app.route('/api/v1/RefugeeRegistrations/<int:ref_id>', methods = ['DELETE'])
def deleteRefugee(ref_id):
    refugee = RefugeeRegistration.query.get(ref_id)
    if not refugee:
        return jsonify({"error":"record not found"}), 404
    try:
        cache.clear()
        db.session.delete(refugee)
        db.session.commit()
        return jsonify({"message":"refugee deleted"}), 200
    
    except Exception as e:
        db.session.rollback()
        app.logger.error(str(e))
        return jsonify({"error":str(e)}), 500



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5000, debug=False)

