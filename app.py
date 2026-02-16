from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import datetime
import json
import os

app = Flask(__name__)
CORS(app)

# Restaurant Menu
MENU = {
    "pizzas": [
        {"id": "p1", "name": "Margherita Pizza", "price": 12},
        {"id": "p2", "name": "Pepperoni Pizza", "price": 14},
        {"id": "p3", "name": "Veggie Supreme Pizza", "price": 13}
    ],
    "pasta": [
        {"id": "pa1", "name": "Spaghetti Carbonara", "price": 11},
        {"id": "pa2", "name": "Fettuccine Alfredo", "price": 12}
    ],
    "drinks": [
        {"id": "d1", "name": "Coke", "price": 2},
        {"id": "d2", "name": "Water", "price": 1},
        {"id": "d3", "name": "House Wine", "price": 8}
    ]
}

@app.route('/')
def home():
    table = request.args.get('table', '')
    return render_template('index.html', table_number=table)

@app.route('/api/menu')
def get_menu():
    return jsonify(MENU)

@app.route('/api/order', methods=['POST'])
def submit_order():
    data = request.json
    order_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    order_data = {
        "order_id": order_id,
        "table": data.get('table'),
        "customer_name": data.get('name'),
        "phone": data.get('phone'),
        "items": data.get('items'),
        "total": data.get('total'),
        "timestamp": datetime.datetime.now().isoformat()
    }
    
    os.makedirs('orders', exist_ok=True)
    
    filename = f"orders/order_{order_id}.json"
    with open(filename, 'w') as f:
        json.dump(order_data, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"🔔 NEW ORDER #{order_id}")
    print(f"{'='*60}")
    print(f"📍 Table: {data.get('table')}")
    print(f"👤 Customer: {data.get('name')}")
    print(f"📞 Phone: {data.get('phone')}")
    print(f"\n📦 ITEMS:")
    for item in data.get('items', []):
        print(f"   • {item['name']} - ${item['price']}")
    print(f"\n💰 TOTAL: ${data.get('total')}")
    print(f"{'='*60}\n")
    
    return jsonify({
        "success": True,
        "order_id": order_id,
        "message": "Order received!"
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

