class Loaders:
    def __init__(self):
        # Fill with dataloaders from other apps
        # For example:
        # self.incidence_by_order_loader = IncidenceByOrderLoader()
        # self.incidence_parent_by_incidence_loader = IncidenceParentByIncidenceLoader()
        # self.order_attached_by_order_loader = OrderAttachedByOrderLoader()
        # self.order_status_by_order_loader = OrderStatusByOrderLoader()
        # self.package_by_order_loader = PackageByOrderLoader()
        pass


class DataLoaderMiddleware:
    def resolve(self, next, root, info, **args):
        if not hasattr(info.context, "loaders"):
            info.context.loaders = Loaders()

        return next(root, info, **args)
