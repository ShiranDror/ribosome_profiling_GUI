from PySide2.QtWidgets import QHBoxLayout, QFileDialog, QPushButton
from PySide2.QtCore import QObject


class ExportToolbar(QHBoxLayout):
    """description of class"""
    def __init__(self, parent=None):
        QHBoxLayout.__init__(self)
        self.parent = parent

        self.save_button = QPushButton("Export Figure")
        self.save_button.clicked.connect(self.open_save_dialog)

        self.addWidget(self.save_button)

    def tr(self, text):
        return QObject.tr(self, text)

    def open_save_dialog(self):
        """ opens files selection dialog """
        file_name, _ = QFileDialog.getSaveFileName(self.save_button, self.tr('Save file'), self.tr("~/Desktop/"), self.tr("Images (*.svg)"))
        self.parent.export_plot(file_name)
        # plt.savefig(file_name, format="svg", transparent = True, dpi = 1200)