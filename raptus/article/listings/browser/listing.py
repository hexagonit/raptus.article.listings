from Acquisition import aq_inner
from zope import interface, component

from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize.instance import memoize

from raptus.article.core.config import MANAGE_PERMISSION
from raptus.article.core import RaptusArticleMessageFactory as _
from raptus.article.core import interfaces
from raptus.article.nesting.interfaces import IArticles

TEASER = False
try:
    from raptus.article.teaser.interfaces import ITeaser
    TEASER = True
except:
    pass

REFERENCE = False
try:
    from raptus.article.reference.interfaces import IReference
    REFERENCE = True
except:
    pass

class IListingLeft(interface.Interface):
    """ Marker interface for the listing left viewlet
    """

class ComponentLeft(object):
    """ Component which lists the articles with their images on the left side
    """
    interface.implements(interfaces.IComponent)
    component.adapts(interfaces.IArticle)
    
    title = _(u'Listing left')
    description = _(u'List of the contained articles with their image on the left side.')
    image = '++resource++listing_left.gif'
    interface = IListingLeft
    viewlet = 'raptus.article.listing.left'
    
    def __init__(self, context):
        self.context = context

class ViewletLeft(ViewletBase):
    """ Viewlet listing the articles with their images on the left side
    """
    index = ViewPageTemplateFile('listing.pt')
    image_class = "component componentLeft"
    type = "left"
    thumb_size = "listingleft"
    component = "listing.left"
    
    def _class(self, brain, i, l):
        cls = []
        if i == 0:
            cls.append('first')
        if i == l-1:
            cls.append('last')
        if i % 2 == 0:
            cls.append('odd')
        if i % 2 == 1:
            cls.append('even')
        return ' '.join(cls)
    
    @property
    def title_pre(self):
        props = getToolByName(self.context, 'portal_properties').raptus_article
        return props.getProperty('listings_%s_titletop' % self.type, False)
    
    @property
    @memoize
    def show_caption(self):
        props = getToolByName(self.context, 'portal_properties').raptus_article
        return props.getProperty('listings_%s_caption' % self.type, False)
    
    @property
    @memoize
    def articles(self):
        provider = IArticles(self.context)
        manageable = interfaces.IManageable(self.context)
        mship = getToolByName(self.context, 'portal_membership')
        if mship.checkPermission(MANAGE_PERMISSION, self.context):
            items = provider.getArticles()
        else:
            items = provider.getArticles(component=self.component)
        items = manageable.getList(items, self.component)
        i = 0
        l = len(items)
        for item in items:
            item.update({'title': item['brain'].Title,
                         'description': item['brain'].Description,
                         'url': item['brain'].hasDetail and item['brain'].getURL() or None,
                         'class': self._class(item['brain'], i, l)})
            if item.has_key('show') and item['show']:
                item['class'] += ' hidden'
            if REFERENCE:
                reference = IReference(item['obj'])
                url = reference.getReferenceURL()
                if url:
                    item['url'] = url
            if TEASER:
                teaser = ITeaser(item['obj'])
                image = {'img': teaser.getTeaser(self.thumb_size),
                         'caption': teaser.getCaption(),
                         'url': None,
                         'rel': None}
                if image['img']:
                    w, h = item['obj'].Schema()['image'].getSize(item['obj'])
                    tw, th = teaser.getSize(self.thumb_size)
                    if item['url']:
                        image['url'] = item['url']
                    elif (tw < w and tw > 0) or (th < h and th > 0):
                        image['rel'] = 'lightbox'
                        image['url'] = teaser.getTeaserURL(size="popup")
                    item['image'] = image
            i += 1
        return items

class IListingRight(interface.Interface):
    """ Marker interface for the listing right viewlet
    """

class ComponentRight(object):
    """ Component which lists the articles with their images on the right side
    """
    interface.implements(interfaces.IComponent)
    component.adapts(interfaces.IArticle)
    
    title = _(u'Listing right')
    description = _(u'List of the contained articles with their image on the right side.')
    image = '++resource++listing_right.gif'
    interface = IListingRight
    viewlet = 'raptus.article.listing.right'
    
    def __init__(self, context):
        self.context = context

class ViewletRight(ViewletLeft):
    """ Viewlet listing the articles with their images on the right side
    """
    image_class = "component componentRight"
    type = "right"
    thumb_size = "listingright"
    component = "listing.right"

class IListingColumns(interface.Interface):
    """ Marker interface for the listing columns viewlet
    """

class ComponentColumns(object):
    """ Component which lists the articles in multiple columns
    """
    interface.implements(interfaces.IComponent)
    component.adapts(interfaces.IArticle)
    
    title = _(u'Listing columns')
    description = _(u'List of the contained articles arranged in columns.')
    image = '++resource++listing_columns.gif'
    interface = IListingColumns
    viewlet = 'raptus.article.listing.columns'
    
    def __init__(self, context):
        self.context = context

class ViewletColumns(ViewletLeft):
    """ Viewlet listing the articles in multiple columns
    """
    image_class = "component"
    type = "columns"
    thumb_size = "listingcolumns"
    component = "listing.columns"
    
    def _class(self, brain, i, l):
        props = getToolByName(self.context, 'portal_properties').raptus_article
        prop_columns = props.getProperty('listings_columns', 3)
        i = i % prop_columns   
        return super(ViewletColumns, self)._class(brain, i, prop_columns)
    
