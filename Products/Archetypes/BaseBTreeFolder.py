from Products.Archetypes import WebDAVSupport
from Products.Archetypes.atapi import BaseFolder
from Products.CMFCore import permissions
from Products.CMFCore.CMFBTreeFolder import CMFBTreeFolder
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass

# to keep backward compatibility
has_btree = 1

from webdav.NullResource import NullResource
from OFS.ObjectManager import REPLACEABLE
from ComputedAttribute import ComputedAttribute

class BaseBTreeFolder(CMFBTreeFolder, BaseFolder):
    """ A BaseBTreeFolder with all the bells and whistles"""

    security = ClassSecurityInfo()

    __implements__ = CMFBTreeFolder.__implements__, BaseFolder.__implements__

    def __init__(self, oid, **kwargs):
        CMFBTreeFolder.__init__(self, oid)
        BaseFolder.__init__(self, oid, **kwargs)

    def __getitem__(self, key):
        """ Override BTreeFolder __getitem__ """
        if key in self.Schema().keys() and key[:1] != "_": #XXX 2.2
            accessor = self.Schema()[key].getAccessor(self)
            if accessor is not None:
                return accessor()
        return CMFBTreeFolder.__getitem__(self, key)

    security.declareProtected(permissions.ModifyPortalContent, 'indexObject')
    indexObject = BaseFolder.indexObject.im_func

    security.declareProtected(permissions.ModifyPortalContent, 'unindexObject')
    unindexObject = BaseFolder.unindexObject.im_func

    security.declareProtected(permissions.ModifyPortalContent, 'reindexObject')
    reindexObject = BaseFolder.reindexObject.im_func

    security.declareProtected(permissions.ModifyPortalContent, 'reindexObjectSecurity')
    reindexObjectSecurity = BaseFolder.reindexObjectSecurity.im_func

    security.declarePrivate('notifyWorkflowCreated')
    notifyWorkflowCreated = BaseFolder.notifyWorkflowCreated.im_func

    security.declareProtected(permissions.AccessContentsInformation, 'opaqueItems')
    opaqueItems = BaseFolder.opaqueItems.im_func

    security.declareProtected(permissions.AccessContentsInformation, 'opaqueIds')
    opaqueIds = BaseFolder.opaqueIds.im_func

    security.declareProtected(permissions.AccessContentsInformation, 'opaqueValues')
    opaqueValues = BaseFolder.opaqueValues.im_func

    security.declareProtected(permissions.ListFolderContents, 'listFolderContents')
    listFolderContents = BaseFolder.listFolderContents.im_func

    security.declareProtected(permissions.AccessContentsInformation,
                              'folderlistingFolderContents')
    folderlistingFolderContents = BaseFolder.folderlistingFolderContents.im_func

    __call__ = BaseFolder.__call__.im_func

    #security.declareProtected(permissions.View, 'view')
    #view = BaseFolder.view.im_func

    def index_html(self):
        """ Allow creation of .
        """
        if self.has_key('index_html'):
            return self._getOb('index_html')
        request = getattr(self, 'REQUEST', None)
        if request and request.has_key('REQUEST_METHOD'):
            if (request.maybe_webdav_client and
                request['REQUEST_METHOD'] in  ['PUT']):
                # Very likely a WebDAV client trying to create something
                nr = NullResource(self, 'index_html')
                nr.__replaceable__ = REPLACEABLE
                return nr
        return None

    index_html = ComputedAttribute(index_html, 1)

    security.declareProtected(permissions.View, 'Title')
    Title = BaseFolder.Title.im_func

    security.declareProtected(permissions.ModifyPortalContent, 'setTitle')
    setTitle = BaseFolder.setTitle.im_func

    security.declareProtected(permissions.View, 'title_or_id')
    title_or_id = BaseFolder.title_or_id.im_func

    security.declareProtected(permissions.View, 'Description')
    Description = BaseFolder.Description.im_func

    security.declareProtected(permissions.ModifyPortalContent, 'setDescription')
    setDescription = BaseFolder.setDescription.im_func

    manage_addFolder = BaseFolder.manage_addFolder.im_func

    MKCOL = BaseFolder.MKCOL.im_func
    MKCOL_handler = BaseFolder.MKCOL_handler.im_func

    security.declareProtected(permissions.ModifyPortalContent, 'PUT')
    PUT = WebDAVSupport.PUT

    security.declareProtected(permissions.View, 'manage_FTPget')
    manage_FTPget = WebDAVSupport.manage_FTPget

    security.declarePrivate('manage_afterPUT')
    manage_afterPUT = WebDAVSupport.manage_afterPUT

    security.declareProtected(permissions.ModifyPortalContent, 'edit')
    edit = BaseFolder.edit.im_func

InitializeClass(BaseBTreeFolder)

BaseBTreeFolderSchema = BaseBTreeFolder.schema

__all__ = ('BaseBTreeFolder', 'BaseBTreeFolderSchema', )
