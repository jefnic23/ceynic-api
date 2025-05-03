from functools import wraps
import inspect
from typing import TYPE_CHECKING, Callable, TypeVar, Awaitable


if TYPE_CHECKING:
    from src.services.orders_service import OrdersService

_T = TypeVar('_T', bound='OrdersService')  # Forward reference


def with_payment_processor(func):
    @wraps(func)
    async def wrapper(self: _T, *args, **kwargs):
        # Get the function signature
        sig = inspect.signature(func)
        bound_args = sig.bind(self, *args, **kwargs)
        bound_args.apply_defaults()

        # Try to find storefront_id in args or kwargs
        storefront_id = bound_args.arguments.get('storefront_id')
        if storefront_id is None:
            raise ValueError(f"'storefront_id' must be provided to {func.__name__}")

        # Fetch payment processor
        payment_processor = await self._get_payment_processor(storefront_id)

        # Inject payment_processor into kwargs
        bound_args.arguments['payment_processor'] = payment_processor

        return await func(*bound_args.args, **bound_args.kwargs)
    return wrapper
