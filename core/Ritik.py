from __future__ import annotations

from discord.ext import commands
import discord, json, math, traceback, os
from .Context import Context
import jishaku
from datetime import datetime

with open('extension.json') as f:
    extension = json.load(f)

os.environ["JISHAKU_HIDE"] = "True"
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"

intents = discord.Intents.default()
intents.members = True

class Ritik(commands.Bot):
    def __init__(self, prefix: str, token: str, **kwargs):
        self.prefix = prefix
        self.token = token
        super().__init__(command_prefix=self.prefix,
                         case_insensitive=True,
                         strip_after_prefix=True,
                         owner_ids=[873859494264860692, 741614468546560092],
                         allowed_mentions=discord.AllowedMentions(
                             everyone=True, replied_user=True),
                          intents=intents,
                         **kwargs)
        for ext in extension:
            try:
                self.load_extension(ext)
                print(f"[EXTENSION] {ext} was loaded successfully!")
            except Exception as e:
                tb = traceback.format_exception(type(e), e, e.__traceback__)
                tbe = "".join(tb) + ""
                print(f"[WARNING] Could not load extension {ext}: {tbe}")

    def run(self) -> None:
        super().run(self.token, bot=False, reconnect=True)

    async def process_commands(self, message: discord.Message):
        ctx = await self.get_context(message, cls=Context)
        if ctx.command is None:
            return
        await self.invoke(ctx)

    async def on_message(self, message: discord.Message):
        await self.process_commands(message)

    async def on_command_error(self, ctx: Context, error):
        # if command has local error handler, return
        if hasattr(ctx.command, 'on_error'): return

        # get the original exception
        error = getattr(error, 'original', error)

        ignore = (commands.CommandNotFound, discord.errors.NotFound,
                  discord.Forbidden)

        if isinstance(error, ignore): return

        elif isinstance(error, commands.BotMissingPermissions):
            missing = [
                perm.replace('_', ' ').replace('guild', 'server').title()
                for perm in error.missing_permissions
            ]
            if len(missing) > 2:
                fmt = '{}, and {}'.format(", ".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            _message = f'nBot Missing permissions. Please provide the following permission(s) to the bot.```\n{fmt}```'
            return await ctx.send(_message)

        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(
                f'{ctx.author.mention} this command has been disabled. Consider asking your Server Manager to fix this out'
            )

        elif isinstance(error, commands.CommandOnCooldown):
            is_owner = await ctx.bot.is_owner(ctx.author)
            if is_owner: return await ctx.reinvoke()
            return await ctx.send(
                f"Command On Cooldown. You are on command cooldown, please retry in **{math.ceil(error.retry_after)}**s"
            )

        elif isinstance(error, commands.MissingPermissions):
            is_owner = await ctx.bot.is_owner(ctx.author)
            if is_owner: return await ctx.reinvoke()
            missing = [
                perm.replace('_', ' ').replace('guild', 'server').title()
                for perm in error.missing_permissions
            ]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]),
                                          missing[-1])
            else:
                fmt = ' and '.join(missing)
            _message = 'Missing Permissions. You need the the following permission(s) to use the command```\n{}```'.format(
                fmt)
            await ctx.send(_message)
            return

        elif isinstance(error, commands.MissingRole):
            is_owner = await ctx.bot.is_owner(ctx.author)
            if is_owner: return await ctx.reinvoke()
            _message = 'Missing Role. You need the the following role(s) to use the command```\n{}```'.format(
                fmt)
            await ctx.send(_message)
            return

        elif isinstance(error, commands.MissingAnyRole):
            is_owner = await ctx.bot.is_owner(ctx.author)
            if is_owner: return await ctx.reinvoke()
            missing = [role for role in error.missing_roles]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]),
                                          missing[-1])
            else:
                fmt = ' and '.join(missing)
            _message = 'Missing Role. You need the the following role(s) to use the command```\n{}```'.format(
                fmt)
            await ctx.send(_message)
            return

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.send(
                    f'No Private Message. This command cannot be used in direct messages. It can only be used in server'
                )
            except discord.Forbidden:
                pass
            return

        elif isinstance(error, commands.NSFWChannelRequired):
            is_owner = await ctx.bot.is_owner(ctx.author)
            if is_owner: return await ctx.reinvoke()

            if ctx.channel.permissions_for(ctx.guild.me).embed_links:
                em = discord.Embed(timestamp=datetime.utcnow())
                em.set_image(url="https://i.imgur.com/oe4iK5i.gif")
                await ctx.send(
                    content=
                    f"NSFW Channel Required. This command will only run in NSFW marked channel. https://i.imgur.com/oe4iK5i.gif",
                    embed=em)
            else:
                await ctx.send(
                    content=
                    f"NSFW Channel Required. This command will only run in NSFW marked channel. https://i.imgur.com/oe4iK5i.gif"
                )
            return

        elif isinstance(error, commands.NotOwner):
            await ctx.send(
                f"Not Owner. You must have ownership of the bot to run {ctx.command.name}"
            )
            return

        elif isinstance(error, commands.PrivateMessageOnly):
            await ctx.send(
                f"Private Message Only. This comamnd will only work in DM messages"
            )

        elif isinstance(error, commands.BadArgument):
            if isinstance(error, commands.MessageNotFound):
                return await ctx.send(
                    f'Message Not Found. Message ID/Link you provied is either invalid or deleted'
                )
            elif isinstance(error, commands.MemberNotFound):
                return await ctx.send(
                    f'Member Not Found. Member ID/Mention/Name you provided is invalid or bot can not see that Member'
                )
            elif isinstance(error, commands.UserNotFound):
                return await ctx.send(
                    f'User Not Found. User ID/Mention/Name you provided is invalid or bot can not see that User'
                )
            elif isinstance(error, commands.ChannelNotFound):
                return await ctx.send(
                    f'Channel Not Found. Channel ID/Mention/Name you provided is invalid or bot can not see that Channel'
                )
            elif isinstance(error, commands.RoleNotFound):
                return await ctx.send(
                    f'Role Not Found. Role ID/Mention/Name you provided is invalid or bot can not see that Role'
                )
            elif isinstance(error, commands.EmojiNotFound):
                return await ctx.send(
                    f'Emoji Not Found. Emoji ID/Name you provided is invalid or bot can not see that Emoji'
                )

        elif isinstance(error, commands.MissingRequiredArgument):
            command = ctx.command
            return await ctx.send(
                f"Missing Required Argument. Please use proper syntax.```\n[p]{command.qualified_name}{'|' if command.aliases else ''}{'|'.join(command.aliases if command.aliases else '')} {command.signature}```"
            )

        elif isinstance(error, commands.MaxConcurrencyReached):
            return await ctx.send(
                f"Max Concurrenry Reached. This command is already running in this server. You have wait for it to finish"
            )

        elif isinstance(error, commands.CheckFailure):
            return await ctx.send(error.__str__().format(ctx=ctx))

        elif isinstance(error, commands.CheckAnyFailure):
            return await ctx.send(' or '.join(
                [error.__str__().format(ctx=ctx) for error in error.errors]))

        else:
            await ctx.send(
                f"Well this is embarrassing. For some reason **{ctx.command.qualified_name}** is not working"
            )
