from Products.CMFCore.utils import getToolByName

DEPENDENCIES = (
    'raptus.article.teaser',
)

def installDependencies(context):
    """ Installs optional dependencies
    """
    if context.readDataFile('raptus.article.listings_install.txt') is None:
        return
    portal = context.getSite()
    
    inst = getToolByName(portal, 'portal_quickinstaller')
    for prod in DEPENDENCIES:
        if inst.isProductInstallable(prod):
            if not inst.isProductInstalled(prod):
                inst.installProduct(prod)
            else:
                inst.reinstallProducts(prod)