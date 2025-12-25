import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from database import db, User, Pokemon, Team

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    return render_template('dashboard.html')

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "Email already registered"}), 400

    hashed_pw = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = User(name=data['name'], email=data['email'], password=hashed_pw)
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    
    if user and check_password_hash(user.password, data['password']):
        session['user_id'] = user.id
        session['user_name'] = user.name
        return jsonify({"message": "Login successful", "redirect": "/dashboard"})
    
    return jsonify({"message": "Invalid email or password"}), 401

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/api/wild-pokemon')
def get_wild_pokemon():
    pokemon_list = Pokemon.query.all()
    output = [{
        'id': p.id, 
        'name': p.name, 
        'type': p.type, 
        'cp': p.cp, 
        'img': p.image_url
    } for p in pokemon_list]
    return jsonify(output)

@app.route('/api/my-team')
def get_my_team():
    if 'user_id' not in session: return jsonify([]), 401
    
    results = db.session.query(Pokemon).join(Team).filter(Team.user_id == session['user_id']).all()
    
    output = [{
        'id': p.id, 
        'name': p.name, 
        'type': p.type, 
        'cp': p.cp, 
        'img': p.image_url
    } for p in results]
    
    return jsonify(output)

@app.route('/api/team/add', methods=['POST'])
def add_to_team():
    if 'user_id' not in session: return jsonify({"error": "Unauthorized"}), 401
    
    user_id = session['user_id']
    pokemon_id = request.json['pokemon_id']
    
    count = Team.query.filter_by(user_id=user_id).count()
    if count >= 6:
        return jsonify({"error": "Team is full! Max 6 members."}), 400
    
    exists = Team.query.filter_by(user_id=user_id, pokemon_id=pokemon_id).first()
    if exists:
        return jsonify({"error": "You already have this specific Pokemon!"}), 400

    new_member = Team(user_id=user_id, pokemon_id=pokemon_id)
    db.session.add(new_member)
    db.session.commit()
    
    return jsonify({"message": "Added to team"})

@app.route('/api/team/remove', methods=['POST'])
def remove_from_team():
    if 'user_id' not in session: return jsonify({"error": "Unauthorized"}), 401
    
    user_id = session['user_id']
    pokemon_id = request.json['pokemon_id']
    
    member = Team.query.filter_by(user_id=user_id, pokemon_id=pokemon_id).first()
    if member:
        db.session.delete(member)
        db.session.commit()
        return jsonify({"message": "Removed from team"})
    
    return jsonify({"error": "Pokemon not found in team"}), 404

def seed_database():
    if not Pokemon.query.first():
        print("Seeding Database...")
        starters = [
            Pokemon(name='Bulbasaur', type='Grass', cp=320, image_url='https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png'),
            Pokemon(name='Charmander', type='Fire', cp=410, image_url='https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png'),
            Pokemon(name='Squirtle', type='Water', cp=350, image_url='https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/7.png'),
            Pokemon(name='Pikachu', type='Electric', cp=500, image_url='https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png'),
            Pokemon(name='Gengar', type='Ghost', cp=950, image_url='https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/94.png'),
            Pokemon(name='Snorlax', type='Normal', cp=1200, image_url='https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/143.png'),
        ]
        db.session.add_all(starters)
        db.session.commit()
        print("Database Seeded!")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_database()
    app.run(debug=True, port=5000)