def export_module_as():
    from jumpscale.core.base import StoredFactory

    from .rmb_http import RmbHttp

    return StoredFactory(RmbHttp)
