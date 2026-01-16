from flask import Flask, render_template, jsonify, send_from_directory
import os
import json
from datetime import datetime, timedelta
import re
from collections import defaultdict, Counter
import plotly
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd

app = Flask(__name__)

# Configuration
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(PROJECT_ROOT, 'reports')
SCREENSHOTS_DIR = os.path.join(PROJECT_ROOT, 'screenshots')
LOGS_DIR = os.path.join(PROJECT_ROOT, 'logs')

class TestResultsParser:
    def __init__(self):
        self.reports_dir = REPORTS_DIR
        self.screenshots_dir = SCREENSHOTS_DIR
        self.logs_dir = LOGS_DIR

    def parse_html_report(self, report_path):
        """Parse pytest HTML report to extract test results"""
        try:
            with open(report_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract test results using regex patterns
            results = {
                'total': 0,
                'passed': 0,
                'failed': 0,
                'skipped': 0,
                'error': 0,
                'duration': 0,
                'tests': []
            }

            # Parse summary from HTML
            total_match = re.search(r'(\d+)\s+tests?', content, re.IGNORECASE)
            if total_match:
                results['total'] = int(total_match.group(1))

            passed_match = re.search(r'(\d+)\s+passed', content, re.IGNORECASE)
            if passed_match:
                results['passed'] = int(passed_match.group(1))

            failed_match = re.search(r'(\d+)\s+failed', content, re.IGNORECASE)
            if failed_match:
                results['failed'] = int(failed_match.group(1))

            # Extract individual test results
            test_pattern = r'<tr[^>]*>.*?<td[^>]*>(.*?)</td>.*?<td[^>]*>(.*?)</td>.*?<td[^>]*>(.*?)</td>.*?<td[^>]*>(.*?)</td>.*?</tr>'
            test_matches = re.findall(test_pattern, content, re.DOTALL | re.IGNORECASE)

            for match in test_matches:
                if len(match) >= 4:
                    test_name = match[0].strip()
                    status = match[1].strip().lower()
                    duration = match[2].strip()
                    error_msg = match[3].strip() if len(match) > 3 else ""

                    results['tests'].append({
                        'name': test_name,
                        'status': status,
                        'duration': duration,
                        'error': error_msg
                    })

            return results

        except Exception as e:
            print(f"Error parsing HTML report: {e}")
            return None

    def get_all_reports(self):
        """Get all available test reports"""
        reports = []
        if os.path.exists(self.reports_dir):
            for file in os.listdir(self.reports_dir):
                if file.endswith('.html'):
                    report_path = os.path.join(self.reports_dir, file)
                    parsed = self.parse_html_report(report_path)
                    if parsed:
                        # Extract timestamp from filename or use file modification time
                        timestamp = datetime.fromtimestamp(os.path.getmtime(report_path))
                        parsed['timestamp'] = timestamp.isoformat()
                        parsed['filename'] = file
                        reports.append(parsed)
        return sorted(reports, key=lambda x: x['timestamp'], reverse=True)

    def get_screenshots(self):
        """Get all available screenshots"""
        screenshots = []
        if os.path.exists(self.screenshots_dir):
            for file in os.listdir(self.screenshots_dir):
                if file.endswith('.png'):
                    file_path = os.path.join(self.screenshots_dir, file)
                    timestamp = datetime.fromtimestamp(os.path.getmtime(file_path))
                    screenshots.append({
                        'filename': file,
                        'path': file_path,
                        'timestamp': timestamp.isoformat(),
                        'url': f'/screenshots/{file}'
                    })
        return sorted(screenshots, key=lambda x: x['timestamp'], reverse=True)

    def get_logs(self):
        """Get all available log files"""
        logs = []
        if os.path.exists(self.logs_dir):
            for file in os.listdir(self.logs_dir):
                if file.endswith('.log'):
                    file_path = os.path.join(self.logs_dir, file)
                    timestamp = datetime.fromtimestamp(os.path.getmtime(file_path))
                    logs.append({
                        'filename': file,
                        'path': file_path,
                        'timestamp': timestamp.isoformat(),
                        'size': os.path.getsize(file_path)
                    })
        return sorted(logs, key=lambda x: x['timestamp'], reverse=True)

    def calculate_metrics(self, reports):
        """Calculate comprehensive metrics from all reports"""
        if not reports:
            return {}

        # Aggregate metrics
        total_executions = len(reports)
        total_tests = sum(r.get('total', 0) for r in reports)
        total_passed = sum(r.get('passed', 0) for r in reports)
        total_failed = sum(r.get('failed', 0) for r in reports)

        # Calculate rates
        pass_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
        fail_rate = (total_failed / total_tests * 100) if total_tests > 0 else 0

        # Recent trends (last 7 days)
        recent_reports = [r for r in reports if datetime.fromisoformat(r['timestamp']) > datetime.now() - timedelta(days=7)]
        recent_pass_rate = 0
        if recent_reports:
            recent_total = sum(r.get('total', 0) for r in recent_reports)
            recent_passed = sum(r.get('passed', 0) for r in recent_reports)
            recent_pass_rate = (recent_passed / recent_total * 100) if recent_total > 0 else 0

        # Failure analysis
        failed_tests = []
        for report in reports:
            for test in report.get('tests', []):
                if test.get('status') == 'failed':
                    failed_tests.append(test['name'])

        failure_counts = Counter(failed_tests)
        most_failed = failure_counts.most_common(5)

        return {
            'total_executions': total_executions,
            'total_tests': total_tests,
            'total_passed': total_passed,
            'total_failed': total_failed,
            'pass_rate': round(pass_rate, 2),
            'fail_rate': round(fail_rate, 2),
            'recent_pass_rate': round(recent_pass_rate, 2),
            'most_failed_tests': most_failed,
            'avg_tests_per_execution': round(total_tests / total_executions, 2) if total_executions > 0 else 0
        }

# Initialize parser
parser = TestResultsParser()

@app.route('/')
def dashboard():
    """Main dashboard page"""
    reports = parser.get_all_reports()
    screenshots = parser.get_screenshots()
    logs = parser.get_logs()
    metrics = parser.calculate_metrics(reports)

    return render_template('dashboard.html',
                         reports=reports,
                         screenshots=screenshots,
                         logs=logs,
                         metrics=metrics)

@app.route('/api/metrics')
def get_metrics():
    """API endpoint for metrics data"""
    reports = parser.get_all_reports()
    metrics = parser.calculate_metrics(reports)
    return jsonify(metrics)

@app.route('/api/charts')
def get_charts():
    """API endpoint for chart data"""
    reports = parser.get_all_reports()

    if not reports:
        return jsonify({})

    # Prepare data for charts
    df = pd.DataFrame(reports)

    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')

    # Pass/Fail trend over time
    trend_data = []
    for _, row in df.iterrows():
        trend_data.append({
            'date': row['timestamp'].strftime('%Y-%m-%d %H:%M'),
            'passed': row['passed'],
            'failed': row['failed'],
            'total': row['total']
        })

    # Status distribution
    status_counts = {
        'passed': df['passed'].sum(),
        'failed': df['failed'].sum(),
        'skipped': df['skipped'].sum(),
        'error': df['error'].sum()
    }

    return jsonify({
        'trend': trend_data,
        'status_distribution': status_counts
    })

@app.route('/screenshots/<filename>')
def get_screenshot(filename):
    """Serve screenshot files"""
    return send_from_directory(SCREENSHOTS_DIR, filename)

@app.route('/logs/<filename>')
def get_log(filename):
    """Serve log files"""
    return send_from_directory(LOGS_DIR, filename)

@app.route('/reports/<filename>')
def get_report(filename):
    """Serve report files"""
    return send_from_directory(REPORTS_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)