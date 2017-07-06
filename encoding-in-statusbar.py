# -*- coding: UTF-8 -*-
#
# Encoding in statusbar (gedit plugin) - Display document encoding in statusbar
# 
# Copyright 2012 Tibor Bősze <tibor.boesze@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from gi.repository import GObject, Gtk, Gedit

class EncodingInStatusbar(GObject.Object, Gedit.WindowActivatable):
    window = GObject.property(type=Gedit.Window)
   
    def __init__(self):
        GObject.Object.__init__(self)
        
    def do_activate(self):
        self._label = Gtk.Label()
        self.window.get_statusbar().pack_end(self._label, False, False, 5)
        
        handlers = []
        handlers.append(self.window.connect("active_tab_changed", self._on_active_tab_change))
        handlers.append(self.window.connect("active_tab_state_changed", self._on_active_tab_state_change))
        self.window.encoding_tab_handlers = handlers
        
        self._update_via_doc(self.window.get_active_document())

    def do_deactivate(self):
        Gtk.Container.remove(self.window.get_statusbar(), self._label)
        del self._label
        for handler in self.window.encoding_tab_handlers:
            self.window.disconnect(handler)
        self.window.encoding_tab_handlers = None

    def do_update_state(self):
        pass

    def _update_via_doc(self, doc):
        if doc and doc.get_encoding() is not None:
            self._label.set_text(doc.get_encoding().to_string())
            self._label.show()
        else:
            self._label.hide()

    def _on_active_tab_change(self, window, tab):
        self._update_via_doc(tab.get_document())

    def _on_active_tab_state_change(self, window):
        if Gedit.TabState.STATE_NORMAL == window.get_active_tab().get_state():
            self._update_via_doc(self.window.get_active_document())
