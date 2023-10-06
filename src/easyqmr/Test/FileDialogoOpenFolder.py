import sys
from PyQt5.QtWidgets import QTreeView, QFileSystemModel, QApplication
from PyQt5 import QtCore


def get_existing_directory():
    """
    Gets the existing directory from the user.

    Returns:
        str: The path to the selected directory.
    """
    # Create an instance of the QApplication class.
    app = QApplication([])

    # Create a QTreeView object.
    treeView = QTreeView()

    # Set the model for the QTreeView object.
    model = QFileSystemModel()
    treeView.setModel(model)

    # Set the initial directory to the current working directory.
    treeView.setRootIndex(model.setRootPath(QtCore.QDir.currentPath()))

    # Show the QTreeView object.
    treeView.show()

    # Run the event loop until the user closes the window.
    app.exec_()

    # Get the path to the selected directory.
    path = treeView.currentIndex().data(QtCore.Qt.DisplayRole)

    # If the path is not a folder, then return it.
    if not QtCore.QDir(path).exists():
        return path

    # If the user closes the window without selecting a directory, then return None.
    return None


if __name__ == "__main__":
    # Call the get_existing_directory() function and store the result in the dir_path variable.
    dir_path = get_existing_directory()

    # If the dir_path variable is not None, then print the path to the selected directory.
    if dir_path is not None:
        print(dir_path)