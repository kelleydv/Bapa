from . import home, membership, officers

blueprints = {
    #url_prefix: Blueprint
    '': home.bp,
    '/membership': membership.bp,
    '/officers': officers.bp
}
