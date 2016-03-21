from . import admin, home, membership, officers

blueprints = {
    #url_prefix: Blueprint
    '/admin' : admin.bp,
    '': home.bp,
    '/membership': membership.bp,
    '/officers': officers.bp
}
