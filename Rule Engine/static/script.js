document.getElementById('create-rule-form').addEventListener('submit', function(event) {
  event.preventDefault();

  const ruleName = document.getElementById('rule-name').value;
  const ruleString = document.getElementById('rule-string').value;

  fetch('/create_rule', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      name: ruleName,
      rule: ruleString
    })
  })
  .then(response => response.json())
  .then(data => {
    document.getElementById('create-result').innerHTML = data.message || data.error;
  })
  .catch(error => console.error('Error:', error));
});

document.getElementById('evaluate-rule-form').addEventListener('submit', function(event) {
  event.preventDefault();

  const ruleName = document.getElementById('eval-rule-name').value;
  const userData = document.getElementById('user-data').value;

  fetch('/evaluate_rule', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      rule_name: ruleName,
      user_data: JSON.parse(userData)
    })
  })
  .then(response => response.json())
  .then(data => {
    document.getElementById('eval-result').innerHTML = data.result !== undefined ? `Result: ${data.result}` : data.error;
  })
  .catch(error => console.error('Error:', error));
});
