from PySide2 import QtWidgets
from shiboken2 import wrapInstance
from maya import OpenMayaUI as omui
from maya import cmds
import maya.api.OpenMaya as om2
from typing import Optional


def get_maya_main_window() -> QtWidgets.QWidget:
    '''
    mayaのメインウィンドウを取得する

    Returns:
        QtWidgets.QWidget: メインウィンドウ
    '''
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=get_maya_main_window()):
        super().__init__(parent)
        self.setWindowTitle('Main Window')
        # table widget
        self.table_widget = QtWidgets.QTableWidget()
        self.table_widget.setColumnCount(2)
        self.set_table_widget()
        # button
        button = QtWidgets.QPushButton('Reload')
        button.clicked.connect(self.set_table_widget)

        central_widget = QtWidgets.QWidget()
        v_layout = QtWidgets.QVBoxLayout()

        v_layout.addWidget(self.table_widget)
        v_layout.addWidget(button)
        central_widget.setLayout(v_layout)
        self.setCentralWidget(central_widget)
        self.show()
        self.activateWindow()

    def set_table_widget(self):
        self.table_widget.clear()
        self.table_widget.setRowCount(0)
        self.table_widget.setHorizontalHeaderLabels(['Alias', 'Real'])

        alias_dict = self.get_alias_dict()
        for i, (alias, real) in enumerate(alias_dict.items()):
            self.table_widget.insertRow(i)
            self.table_widget.setItem(i, 0, QtWidgets.QTableWidgetItem(alias))
            self.table_widget.setItem(i, 1, QtWidgets.QTableWidgetItem(real))

    @staticmethod
    def get_alias_dict() -> dict[str, str]:
        '''
        エイリアスを取得する

        Returns:
            Dict: エイリアスの辞書
                    {alias_name: real_name}
        '''
        if not cmds.ls(selection=True):
            print('Please select a node')
            return {}
        selection_list: om2.MSelectionList = om2.MGlobal.getActiveSelectionList()
        node_mobject = selection_list.getDependNode(0)
        dep_node: om2.MFnDependencyNode = om2.MFnDependencyNode(node_mobject)
        alias_list: tuple[Optional[tuple[str, str]]] = dep_node.getAliasList()

        if not alias_list:
            print('No alias found')
            return {}
        return dict(filter(None, alias_list))


def main():
    MainWindow()
