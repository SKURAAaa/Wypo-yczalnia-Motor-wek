from flask import Flask, jsonify, request, render_template, redirect, url_for
from user import User
from boat import Boat
from booking import Booking

global activeUser

users = [
    User(1, "Adam Miauczyński"),
    User(2, "Andrzej Kmicic"),
    User(3, "Janusz Tracz"),
    User(4, "Ewa Lipska"),
    User(5, "Ola Burska"),
]

boats = [
    Boat(1, "Yamaha", "242X", 1000),
    Boat(2, "Sea Ray", "SLX 400", 2000),
    Boat(3, "Bayliner", "VR5", 1500),
    Boat(4, "Chaparral", "267 SSX", 2500),
    Boat(5, "Regal", "LS4", 1800),
]

# Lista rezerwacji
bookings = []

app = Flask(__name__)

# Strona główna
@app.route('/')
def renderUsers():
    return render_template('users.html', users=users)

# Wybór użytkownika
@app.route('/selectUser', methods=['POST'])
def selectUser():
    global activeUser
    user_id = int(request.form.get('user_id'))
    if user_id > 0 and user_id <= len(users):
        activeUser = users[user_id - 1]
        return redirect(url_for('main'))
    return jsonify({'error': 'Invalid user ID'}), 404

# Stronapo wybraniu użytkownika
@app.route('/main')
def main():
    return render_template('main.html')

# motorówyy
@app.route('/boats')
def renderBoats():
    return render_template('boats.html', boats=boats)

# rezerwacje
@app.route('/bookings')
def renderBookings():
    return render_template('bookings.html', bookings=bookings)

@app.route('/addBooking/html')
def renderAddBooking():
    return render_template('addBooking.html')

# Dodawanie nowej rezerwacji
@app.route('/addBooking', methods=['POST'])
def addBookings():
    boatId = int(request.form.get('boat_id'))
    startDay = request.form.get('start_date')
    days = int(request.form.get('days'))

    if boatId > 0 and boatId <= len(boats) and days > 0:
        global activeUser
        bookings.append(Booking(activeUser, boats[boatId - 1], startDay, days))
        return render_template('bookings.html', bookings=bookings)
    return jsonify({'error': 'Invalid input data'}), 400

# API motorówy
@app.route('/api/boats', methods=['GET'])
def get_boats():
    return jsonify([boat.__dict__ for boat in boats])

@app.route('/api/boats/<int:boat_id>', methods=['GET'])
def get_boat(boat_id):
    boat = next((boat for boat in boats if boat.id == boat_id), None)
    if boat is None:
        return jsonify({'error': 'Boat not found'}), 404
    return jsonify(boat.__dict__)

@app.route('/api/boats', methods=['POST'])
def add_boat():
    data = request.get_json()
    if 'brand' in data and 'model' in data and 'costPerDay' in data:
        new_boat = Boat(len(boats) + 1, data['brand'], data['model'], data['costPerDay'])
        boats.append(new_boat)
        return jsonify(new_boat.__dict__), 201
    return jsonify({'error': 'Invalid input data'}), 400

@app.route('/api/boats/<int:boat_id>', methods=['PUT'])
def update_boat(boat_id):
    boat = next((boat for boat in boats if boat.id == boat_id), None)
    if boat is None:
        return jsonify({'error': 'Boat not found'}), 404
    data = request.get_json()
    boat.brand = data.get('brand', boat.brand)
    boat.model = data.get('model', boat.model)
    boat.costPerDay = data.get('costPerDay', boat.costPerDay)
    return jsonify(boat.__dict__), 200

@app.route('/api/boats/<int:boat_id>', methods=['DELETE'])
def delete_boat(boat_id):
    global boats
    if any(boat.id == boat_id for boat in boats):
        boats = [boat for boat in boats if boat.id != boat_id]
        return '', 204
    return jsonify({'error': 'Boat not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
