from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QStyleFactory

app = QApplication([])
app.setStyle(QStyleFactory.create('Fusion'))

# Define your stylesheet
stylesheet = """
    QWidget {
        background-color: #2b2b2b;
        color: #ffffff;
    }
    QPushButton {
        background-color: #4b4b4b;
        border: none;
        color: #ffffff;
        padding: 5px;
        min-width: 70px;
    }
    QPushButton:hover {
        background-color: #5b5b5b;
    }
    QPushButton:pressed {
        background-color: #4b4b4b;
    }
"""

# Apply the stylesheet
app.setStyleSheet(stylesheet)

window = QWidget()
layout = QVBoxLayout()
layout.addWidget(QPushButton("Button 1"))
layout.addWidget(QPushButton("Button 2"))
window.setLayout(layout)
window.show()

app.exec()