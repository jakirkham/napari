from PyQt5.QtCore import QCoreApplication, Qt, QSize
from PyQt5.QtWidgets import QWidget, QSlider, QVBoxLayout, QSplitter
from PyQt5.QtGui import QCursor, QPixmap
from vispy.scene import SceneCanvas, PanZoomCamera

from .controls import QtControls

import os.path as osp
from ....resources import resources_dir


class QtViewer(QSplitter):
    with open(osp.join(resources_dir, 'stylesheet.qss'), 'r') as f:
        default_stylesheet = f.read()

    def __init__(self, viewer):
        super().__init__()

        QCoreApplication.setAttribute(Qt.AA_UseStyleSheetPropagationInWidgetStyles, True)
        self.setStyleSheet(self.default_stylesheet)

        self.viewer = viewer

        self.canvas = SceneCanvas(keys=None, vsync=True)
        self.canvas.native.setMinimumSize(QSize(100, 100))

        self.canvas.connect(self.on_mouse_move)
        self.canvas.connect(self.on_mouse_press)
        self.canvas.connect(self.on_mouse_release)
        self.canvas.connect(self.on_key_press)
        self.canvas.connect(self.on_key_release)

        self.view = self.canvas.central_widget.add_view()
        # Set 2D camera (the camera will scale to the contents in the scene)
        self.view.camera = PanZoomCamera(aspect=1)
        # flip y-axis to have correct aligment
        self.view.camera.flip = (0, 1, 0)
        self.view.camera.set_range()

        center = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.canvas.native)
        layout.addWidget(self.viewer.dims._qt)
        center.setLayout(layout)

        # Add controls, center, and layerlist
        self.control_panel = QtControls(viewer)
        self.addWidget(self.control_panel)
        self.addWidget(center)
        self.addWidget(self.viewer.layers._qt)

        viewer.dims._qt.setFixedHeight(0)

        self._cursors = {
                'disabled': QCursor(QPixmap(':/icons/cursor_disabled.png')
                                    .scaled(20, 20)),
                'cross': Qt.CrossCursor,
                'forbidden': Qt.ForbiddenCursor,
                'pointing': Qt.PointingHandCursor,
                'standard': QCursor()
            }

    def set_cursor(self, cursor):
        self.canvas.native.setCursor(self._cursors[cursor])

    def on_mouse_move(self, event):
        """Called whenever mouse moves over canvas.
        """
        layer = self.viewer._top
        if layer is not None:
            layer.on_mouse_move(event)

    def on_mouse_press(self, event):
        """Called whenever mouse pressed in canvas.
        """
        layer = self.viewer._top
        if layer is not None:
            layer.on_mouse_press(event)

    def on_mouse_release(self, event):
        """Called whenever mouse released in canvas.
        """
        layer = self.viewer._top
        if layer is not None:
            layer.on_mouse_release(event)

    def on_key_press(self, event):
        """Called whenever key pressed in canvas.
        """
        layer = self.viewer._top
        if layer is not None:
            layer.on_key_press(event)

    def on_key_release(self, event):
        """Called whenever key released in canvas.
        """
        layer = self.viewer._top
        if layer is not None:
            layer.on_key_release(event)
