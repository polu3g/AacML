from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET

app = Flask(__name__)

class Agent:
    def __init__(self, agent_id, role, state, action, reward):
        self.agent_id = agent_id
        self.role = role
        self.state = state
        self.action = action
        self.reward = reward

    def to_dict(self):
        return {
            "agent_id": self.agent_id,
            "role": self.role,
            "state": self.state,
            "action": self.action,
            "reward": self.reward
        }

@app.route('/intercept', methods=['POST'])
def intercept_xml():
    if request.content_type != 'application/xml':
        return jsonify({"error": "Invalid content type, expecting XML"}), 400
    
    xml_data = request.data.decode('utf-8')
    root = ET.fromstring(xml_data)
    
    agents = []
    for agent in root.findall('Agent'):
        agent_id = agent.get('id')
        role = agent.get('role')
        
        state = {}
        for state_elem in agent.find('State'):
            state[state_elem.tag] = state_elem.attrib
        
        action = {}
        for action_elem in agent.find('Action'):
            action[action_elem.tag] = action_elem.attrib
        
        reward = {}
        reward_elem = agent.find('Reward')
        if reward_elem is not None:
            reward = {
                "type": reward_elem.get('type'),
                "value": reward_elem.get('value'),
                "reason": reward_elem.get('reason')
            }
        
        agent_obj = Agent(agent_id, role, state, action, reward)
        agents.append(agent_obj.to_dict())
    
    return jsonify({"agents": agents})

if __name__ == '__main__':
    app.run(debug=True)
