from flask import Flask, request, send_file
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
import io


app = Flask(__name__)

def generate_mla_format_pdf(student_name, professor_name, course_name, title, content):
    current_date = datetime.now().strftime("%d %B %Y")
    buffer = io.BytesIO()

    # Create a PDF canvas
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Set margins
    margin = inch
    text_margin = 0.5 * inch

    # Draw header
    c.setFont("Times-Roman", 12)
    c.drawString(margin, height - margin, student_name)
    c.drawString(margin, height - margin - 14, professor_name)
    c.drawString(margin, height - margin - 28, course_name)
    c.drawString(margin, height - margin - 42, current_date)
    c.drawRightString(width - margin, height - margin, "Page 1")

    # Draw title
    c.setFont("Times-Bold", 14)
    c.drawCentredString(width / 2, height - margin - 100, title)

    # Draw content
    c.setFont("Times-Roman", 12)
    text = c.beginText(margin, height - margin - 140)
    text.setTextOrigin(margin, height - margin - 140)
    text.setLeading(14)
    for line in content.split('\n'):
        text.textLine(line)
    c.drawText(text)

    # Save the PDF
    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer

@app.route('/')
def index():
    return '''
    <html>
        <body>
            <h1>Go to /upload to submit your MLA formatting details</h1>
        </body>
    </html>
    '''

@app.route('/upload')
def upload_page():
    with open('index.html') as f:
        return f.read()

@app.route('/generate', methods=['POST'])
def generate():
    student_name = request.form['studentName']
    professor_name = request.form['professorName']
    course_name = request.form['courseName']
    title = request.form['title']
    content = request.form['content']
    buffer = generate_mla_format_pdf(student_name, professor_name, course_name, title, content)
    return send_file(buffer, as_attachment=True, download_name='output.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)