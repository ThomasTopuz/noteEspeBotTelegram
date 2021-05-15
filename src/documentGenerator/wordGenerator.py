import docx
from src.firebaseconnector.firebase import get_week_number, get_tests_done, get_test_received_curr_week
from datetime import datetime
import os
from src.encryption.encrypter import decrypt


# function to generate a docx to send to the trainer
def generate_docx(username, fullname):
    def get_week_day(n):
        d = datetime.now().strftime("%Y") + "-W" + str(get_week_number())
        r = str(datetime.strptime(d + '-' + n, "%Y-W%W-%w"))
        return r.split(" ", 1)[0]

    filename = "noteEspeSett" + str(datetime.now().isocalendar()[1]) + "_" + fullname + ".docx"
    doc = docx.Document(os.path.join(os.path.dirname(__file__), 'template.docx'))
    # creazione heading
    doc.paragraphs[9].text = fullname
    doc.paragraphs[12].text = datetime.now().strftime("%d.%m.%Y")

    doc.paragraphs[16].text = "Settimana dal " + get_week_day("1") + " al " + get_week_day("5")

    # Tests done
    # table generation
    doc.add_heading('Espe fatti', level=1)
    tests_done = get_tests_done(username)
    table_tests_done = doc.add_table(rows=1, cols=3)
    heading_cells = table_tests_done.rows[0].cells
    heading_cells[0].text = 'data'
    heading_cells[1].text = 'materia'
    heading_cells[2].text = 'osservazioni'
    table_tests_done.style = 'Grid Table 1 Light'

    for i in tests_done:
        test = i.val()
        cells = table_tests_done.add_row().cells
        cells[0].text = test['data']
        cells[1].text = test['materia']
        cells[2].text = decrypt(test['osservazioni_fatto'])

    doc.add_paragraph()
    doc.add_paragraph()
    # TESTS RECEIVED
    doc.add_heading('Espe Ritornati', level=1)
    tests_received = get_test_received_curr_week(username)
    table_tests_received = doc.add_table(rows=1, cols=5)
    table_tests_received.style = 'Grid Table 1 Light'

    # heading
    heading_cells = table_tests_received.rows[0].cells
    heading_cells[0].text = 'data espe'
    heading_cells[1].text = 'materia'
    heading_cells[2].text = 'nota'
    heading_cells[3].text = 'media'
    heading_cells[4].text = 'osservazioni'

    for i in tests_received:
        test_received = i.val()
        cells = table_tests_received.add_row().cells
        cells[0].text = test_received['data']
        cells[1].text = test_received['materia']
        cells[2].text = decrypt(test_received['nota'])
        cells[3].text = decrypt(str(test_received['media']))
        cells[4].text = decrypt(test_received['osservazioni_ricevuto'])

    doc.save(filename)
    return filename


# function to delete the generated docx once is sent
def delete_file(filename):
    os.remove(filename)
