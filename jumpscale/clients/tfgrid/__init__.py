def export_module_as():
    from jumpscale.core.base import StoredFactory

    from .client import TfgridClient

    return StoredFactory(TfgridClient)
