def load_transforms(transforms):
    """
    Load transform modules and return instance of transform class.

    Parameters
    ----------
    transforms : [str] or [[str]]
        array of transform module name,
        or nested array of transform module name with argv to load

    Returns
    -------
        array of transform instance
    """

    from . import Transform
    import inspect

    # normalize arguments to form as [(name, [option, ...]), ...]
    transforms_with_argv = map(lambda t: (t[0], t[1:]) if isinstance(t, list) else (t, []),
                               transforms)

    def instantiate_transform(module_name, argv):
        tr_module = __import__(module_name, fromlist=['dummy'])
        tr_classes = inspect.getmembers(
            tr_module,
            lambda c: issubclass(c if inspect.isclass(c) else None.__class__,
                                 Transform))

        if len(tr_classes) != 1:
            raise TypeError('Transform module must have only one subclass of Transform')

        tr_class = tr_classes[0]
        return tr_class[1](argv)

    return [instantiate_transform(tr[0], tr[1])
            for tr in transforms_with_argv]
