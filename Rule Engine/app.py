from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import re

app = Flask(__name__)

Base = declarative_base()

class Node:
    def __init__(self, type, value=None, left=None, right=None):
        self.type = type
        self.value = value
        self.left = left
        self.right = right

class Rule(Base):
    __tablename__ = 'rules'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    ast = Column(JSON)

engine = create_engine('sqlite:///rules.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def create_rule(rule_string):
    def parse_expression(tokens):
        if len(tokens) == 0:
            return None, 0
        if tokens[0] == '(':
            left, left_consumed = parse_expression(tokens[1:])
            if left_consumed + 1 >= len(tokens):
                return left, left_consumed + 1
            op = tokens[left_consumed + 1]
            right, right_consumed = parse_expression(tokens[left_consumed + 2:])
            return Node('operator', op, left, right), left_consumed + right_consumed + 3
        else:
            return Node('operand', ' '.join(tokens[:3])), 3

    tokens = re.findall(r'\(|\)|[\w\'=<>]+', rule_string)
    return parse_expression(tokens)[0]

def node_to_dict(node):
    if node is None:
        return None
    return {
        'type': node.type,
        'value': node.value,
        'left': node_to_dict(node.left),
        'right': node_to_dict(node.right)
    }

def dict_to_node(d):
    if d is None:
        return None
    return Node(
        d['type'],
        d['value'],
        dict_to_node(d['left']),
        dict_to_node(d['right'])
    )

def evaluate_rule(root, data):
    if root.type == 'operand':
        attr, op, value = root.value.split()
        if op == '=':
            return str(data.get(attr)) == value.strip("'")
        elif op == '>':
            return float(data.get(attr, 0)) > float(value)
        elif op == '<':
            return float(data.get(attr, 0)) < float(value)
    elif root.type == 'operator':
        if root.value == 'AND':
            return evaluate_rule(root.left, data) and evaluate_rule(root.right, data)
        elif root.value == 'OR':
            return evaluate_rule(root.left, data) or evaluate_rule(root.right, data)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_rule', methods=['POST'])
def api_create_rule():
    data = request.json
    if not data or 'rule' not in data or 'name' not in data:
        return jsonify({'error': 'Invalid request data'}), 400
    
    rule_string = data['rule']
    rule_name = data['name']
    
    session = Session()
    existing_rule = session.query(Rule).filter_by(name=rule_name).first()

    if existing_rule:
        return jsonify({'error': f"Rule with name '{rule_name}' already exists"}), 400

    try:
        ast = create_rule(rule_string)
        new_rule = Rule(name=rule_name, ast=node_to_dict(ast))
        session.add(new_rule)
        session.commit()
        return jsonify({'message': 'Rule created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/evaluate_rule', methods=['POST'])
def api_evaluate_rule():
    data = request.json
    if not data or 'rule_name' not in data or 'user_data' not in data:
        return jsonify({'error': 'Invalid request data'}), 400
    
    rule_name = data['rule_name']
    user_data = data['user_data']
    
    try:
        session = Session()
        rule = session.query(Rule).filter_by(name=rule_name).first()
        if rule is None:
            return jsonify({'error': 'Rule not found'}), 404
        ast = dict_to_node(rule.ast)
        result = evaluate_rule(ast, user_data)
        return jsonify({'result': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
