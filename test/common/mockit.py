from __future__ import annotations

from typing import Callable, Any
import builtins
import inspect
from inspect import Parameter

from contextlib import contextmanager
from unittest.mock import Mock, call, ANY, patch
from io import StringIO

_Whatever = object()


class _Call:
    def __init__(self, args=_Whatever, kwargs=_Whatever, return_value=_Whatever):
        self.args: tuple | _Whatever = args
        self.kwargs: dict | _Whatever = kwargs
        self.return_value = return_value


class _Patcher:
    def __init__(self, spec):
        self.spec = spec
        self.spec_name = f'{self.spec.__module__}.{self.spec.__name__}'
        self.sig = inspect.signature(spec)
        self.calls: list[_Call] = []
        self.complete_call = True
        self.patch_object = None
        self.mock_object = None

    @property
    def default_call(self):
        args, kwargs = [], {}
        for name, desc in self.sig.parameters.items():
            if desc.default is not desc.empty:
                continue
            if desc.kind in [Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD]:
                args.append(ANY)
            elif desc.kind == Parameter.KEYWORD_ONLY:
                kwargs[name] = ANY
        return call(*args, **kwargs)

    @property
    def return_values(self):
        return [c.return_value for c in self.calls]

    @property
    def call_list(self):
        # noinspection PyArgumentList
        return [call(*c.args, **c.kwargs)
                if c.args is not _Whatever else self.default_call
                for c in self.calls]

    def expects(self, *args, **kwargs):
        self.calls.append(_Call(args=args, kwargs=kwargs))
        self.complete_call = False
        return self

    def returns(self, return_value=_Whatever, *, skip_previous=False):
        skip_previous = skip_previous or len(self.calls) == 0
        if skip_previous or self.complete_call:
            self.calls.append(_Call())
        self.calls[-1].return_value = return_value
        self.complete_call = True
        return self

    def returns_many(self, *args):
        for arg in args:
            self.returns(arg)
        return self

    def __enter__(self):
        self.patch_object = patch(self.spec_name, spec=self.spec, side_effect=self.return_values)
        self.mock_object = self.patch_object.start()
        return self.mock_object

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mock_object.assert_has_calls(self.call_list)
        self.patch_object.stop()


class _PrintPatcher:
    def __init__(self):
        self.patch_object = None
        self.mock_object = None

    @property
    def spec_name(self):
        return f'sys.stdout'

    def __enter__(self):
        self.received_output = []
        self.patch_object = patch(self.spec_name, new_callable=StringIO)
        self.mock_object = self.patch_object.start()
        return self.mock_object

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.patch_object.stop()


mock = _Patcher
mock_print = _PrintPatcher
