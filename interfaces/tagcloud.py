# This Python file uses the following encoding: utf-8

__author__ = 'Héctor Velarde <hvelarde@jornada.com.mx>'
__docformat__ = 'restructuredtext'
__copyright__ = 'Copyright (C) 2006-2007  DEMOS, Desarrollo de Medios, S.A. de C.V.'
__license__  = 'The GNU General Public License version 2 or later'

from zope.interface import Interface

class ITagCloudTool(Interface):
    """ marker interface for TagCloudTool """
    def getCloud():
        """ returns a list of {tag, size} pairs in alphabetical order """
