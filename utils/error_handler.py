from PyQt5.QtWidgets import QMessageBox

def show_error_message(self, message):
        QMessageBox.critical(self, "Erro", message)
