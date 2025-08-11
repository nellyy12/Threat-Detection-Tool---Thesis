from flask import Flask, render_template, request, redirect, url_for, flash
import subprocess
import os
import glob
import json
from datetime import datetime
import sys
sys.path.append('anomaly_web')
from utils.detection import get_anomaly_results
import openai

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this in production
OUTPUT_DIR = 'output'

openai.api_key = "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"

@app.template_filter('datetimeformat')
def datetimeformat(value):
    try:
        return datetime.utcfromtimestamp(int(value)).strftime('%Y-%m-%d %H:%M:%S UTC')
    except Exception:
        return value

@app.template_filter('to_unix')
def to_unix(value):
    try:
        return int(float(value)) // 1000
    except Exception:
        return 0

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        domain = request.form.get('domain', '').strip()
        if not domain:
            flash('Please enter a domain.', 'danger')
            return redirect(url_for('index'))
        # Run the scraper CLI
        try:
            subprocess.run([
                'python', 'scraper_cli.py', '-d', domain, '--all'
            ], check=True)
        except subprocess.CalledProcessError as e:
            flash(f'Error running scraper: {e}', 'danger')
            return redirect(url_for('index'))
        return redirect(url_for('results', domain=domain))
    return render_template('index.html')

@app.route('/results/<domain>')
def results(domain):
    # Find all output files for this domain
    safe_domain = domain.replace('.', '_')
    pattern = os.path.join(OUTPUT_DIR, f'{safe_domain}_*.txt')
    files = glob.glob(pattern)
    data = {}
    for file in files:
        key = os.path.basename(file).replace(f'{safe_domain}_', '').replace('.txt', '')
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                try:
                    data[key] = json.loads(content)
                except Exception:
                    data[key] = content
        except Exception as e:
            data[key] = f'Error reading file: {e}'
    return render_template('results.html', domain=domain, data=data)

@app.route('/anomaly')
def anomaly_dashboard():
    try:
        logs = get_anomaly_results()
    except Exception as e:
        logs = []
        print("Error loading anomaly results:", e)
    return render_template("anomaly_dashboard.html", logs=logs)

@app.route('/ai_analysis/<domain>')
def ai_analysis(domain):
    import glob, os, json
    safe_domain = domain.replace('.', '_')
    pattern = os.path.join(OUTPUT_DIR, f'{safe_domain}_*.txt')
    files = glob.glob(pattern)
    all_data = {}
    for file in files:
        key = os.path.basename(file).replace(f'{safe_domain}_', '').replace('.txt', '')
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                try:
                    all_data[key] = json.loads(content)
                except Exception:
                    all_data[key] = content
        except Exception as e:
            all_data[key] = f'Error reading file: {e}'
    # Compose prompt
    prompt = (
        "You are an expert in brand analysis. Given the following OSINT and cyber data for an organization, "
        "calculate a Brand Value Index (BVI) for the organization out of 10, and provide a concise reason for your score. "
        "The BVI should reflect the organization's reputation, trust, and digital presence based on the data. "
        "Output your answer as: 'Brand Value Index: <score>/10\nReason: <reason>'\n\nData: " + json.dumps(all_data, indent=2)
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": prompt}],
            max_tokens=400
        )
        ai_result = response.choices[0].message.content.strip()
    except Exception as e:
        ai_result = f"Error with AI analysis: {e}"
    return {"result": ai_result}

if __name__ == '__main__':
    app.run(debug=True) 