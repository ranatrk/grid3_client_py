def export_module_as():
    from jumpscale.core.base import StoredFactory

    from .rmb import Rmb

    return StoredFactory(Rmb)
