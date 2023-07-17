from PyQt5.QtWidgets import QMessageBox, QGridLayout, QWizardPage


def show_dialog(title="Warning", message="Message box pop up window"):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setText(message)
    msg_box.setWindowTitle(title)
    msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

    return_value = msg_box.exec()

    if return_value == QMessageBox.Ok:
        print('OK clicked')

    if return_value == QMessageBox.Cancel:
        print('Cancel clicked')