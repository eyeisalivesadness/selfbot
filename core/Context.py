from __future__ import annotations
from discord.ext import commands
import functools, discord

__all__ = ("Context", )


class Context(commands.Context):
    def __init__(self, *args, **kwargs):
        super().__init__()

    def with_type(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            context = args[0] if isinstance(args[0],
                                            commands.Context) else args[1]
            try:
                async with context.typing():
                    await func(*args, **kwargs)
            except discord.errors.Forbidden:
                await func(*args, **kwargs)
            return wrapped
