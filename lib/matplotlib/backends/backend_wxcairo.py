import wx.lib.wxcairo as wxcairo

from .. import _api
from .backend_cairo import cairo, FigureCanvasCairo
from .backend_wx import _BackendWx, _FigureCanvasWxBase, FigureFrameWx
from .backend_wx import (  # noqa: F401 # pylint: disable=W0611
    NavigationToolbar2Wx as NavigationToolbar2WxCairo)


@_api.deprecated(
    "3.6", alternative="FigureFrameWx(..., canvas_class=FigureCanvasWxCairo)")
class FigureFrameWxCairo(FigureFrameWx):
    def get_canvas(self, fig):
        return FigureCanvasWxCairo(self, -1, fig)


class FigureCanvasWxCairo(FigureCanvasCairo, _FigureCanvasWxBase):
    def draw(self, drawDC=None):
        size = self.figure.bbox.size.astype(int)
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, *size)
        self._renderer.set_context(cairo.Context(surface))
        self._renderer.dpi = self.figure.dpi
        self.figure.draw(self._renderer)
        self.bitmap = wxcairo.BitmapFromImageSurface(surface)
        self._isDrawn = True
        self.gui_repaint(drawDC=drawDC)


@_BackendWx.export
class _BackendWxCairo(_BackendWx):
    FigureCanvas = FigureCanvasWxCairo
