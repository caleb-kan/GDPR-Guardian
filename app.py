from flask import Flask, request, render_template
from bs4 import BeautifulSoup
import requests
import openai

app = Flask(__name__)

#API KEY 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

openai.api_key = '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'

# GDPR rights we are looking for
gdpr_rights = [
    'Right to be informed',
    'Right of access',
    'Right to rectification',
    'Right to erasure',
    'Right to restrict processing',
    'Right to data portability',
    'Right to object',
    'Rights related to automated decision making and profiling',
]

def get_privacy_policy(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Locate the privacy policy on the page. This will need to be customised
    # for the specific structure of the website.
    policy_div = soup.find('div', id='landings-privacy-policy')
    
    if policy_div:
        return policy_div.get_text()
    else:
        return "Not Found"

def analyze_privacy_policy(policy):
    response = openai.Completion.create(
      engine="text-davinci-004",
      prompt=policy,
      max_tokens=60
    )
    return response.choices[0].text.strip()

def compare_to_gdpr(policy_analysis):
    # This will require a more complex comparison than the one we're showing here
    missing_rights = [right for right in gdpr_rights if right.lower() not in policy_analysis.lower()]
    compliance_score = len(gdpr_rights) - len(missing_rights)
    return compliance_score, missing_rights

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        policy = scrape_privacy_policy(url)
        policy_analysis = analyze_privacy_policy(policy)
        compliance_score, missing_rights = compare_to_gdpr(policy_analysis)
        
        return render_template('results.html', compliance_score=compliance_score, missing_rights=missing_rights, policy_analysis=policy_analysis)
    return render_template('index.html')

if __name__ == '__main__':
    url = "https://openai.com/policies/privacy-policy"
    policy_text = get_privacy_policy(url)
    print(policy_text)
    
    def write_text_to_file(filename, text):
        f = open(filename, 'w', encoding='utf-8')
        f.write(text)
        f.close()

    write_text_to_file('privacy_policy.txt', policy_text)
    #app.run(debug=True)