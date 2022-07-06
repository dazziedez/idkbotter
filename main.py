import discord
from discord.ext import commands
import os
import asyncio
import sys
import time


intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=".", intents=intents)
client.remove_command("help")


def restart_bot():
    os.execv(sys.executable, ['python'] + sys.argv)


@client.command(aliases=["reboot", "reload"])
@commands.has_permissions(administrator=True)
async def restart(ctx):
    await ctx.reply("Success")
    await print('-' * 10 + f'\nRestarting\n' + '-' * 10)
    restart_bot()


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name="you - .gg/bottle"))
    print(f"🟢 successfully logged in as {client.user}")

@client.command()
async def load(ctx, extension):
    client.load_extension(f'events.{extension}')
    await ctx.reply(f'{extension} successfully loaded')
    await print(f'🔵 {extension} successfully loaded')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'events.{extension}')
    await ctx.reply(f'{extension} successfully unloaded')
    await print(f'🔵 {extension} successfully unloaded')


for filename in os.listdir('./events'):
  if filename.endswith('.py'):
    client.load_extension(f'events.{filename[:-3]}')
    print(f'🔵 "{filename[:-3]}" successfully loaded')
    
  else:
    print(f'🟠 "{filename[:-3]}" could not be read')

@client.event
async def on_message(message):
    await client.process_commands(message)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'Please pass in all requirements - `{error}`')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"You don't have permission to do that - `{error}`")


@client.event
async def on_member_join(member):
    guild = client.get_guild(874440438604496976)
    channel = guild.get_channel(876101520297443388)
    general = guild.get_channel(876085929117352016)
    verify = guild.get_channel(876102248185339925)
    log = guild.get_channel(876104888122212413)
    if time.time() - member.created_at.timestamp() < 2592000:
        embed = discord.Embed(description=f'You were kicked from `{guild.name}` because your account is too young \n<t:{int(member.created_at.timestamp())}:R> < `30 days ago`')
        logembed = discord.Embed(description=f'{member.name} was kicked because their account is too young \n<t:{int(member.created_at.timestamp())}:R> < `30 days ago`')
        await member.send(embed=embed)
        await guild.kick(member)
        await log.send(embed=logembed)
    else:
        logembed = discord.Embed(title='Member joined', description=f'{member}')
        logembed.add_field(name="Account Created",
                    value=f'<t:{int(member.created_at.timestamp())}:R>')
        logembed.set_thumbnail(url=member.avatar_url)
        await channel.send(
        f'{member.mention} joined this server :O\nRemember, you can\'t leave')
        await member.send(f'Welcome to **{guild.name}**, {member.name}!\njust to make things clear, you\'ll die if you leave\nhttps://discord.gg/T5BZayunBB')
        await general.send(f'{member.mention} just joined, say hi!',
                       delete_after=60)
        await verify.send(f'welcome {member.mention}!\nPlease react with ✅ above to gain access to the server',
        delete_after=10)
        await log.send(embed=logembed)


@client.event
async def on_member_remove(member):
    guild = client.get_guild(874440438604496976)
    channel = guild.get_channel(879118347088834620)
    log = guild.get_channel(876104888122212413)
    logembed = discord.Embed(title='Member left', description=f'{member}')
    logembed.set_thumbnail(url=member.avatar_url)
    logembed.add_field(name="Joined At", value=f'<t:{int(member.joined_at.timestamp())}:R>')
    await channel.send(
        f'Someone just left...\nMay {member.name}#{member.discriminator} rest in peace.'
    )
    await log.send(embed=logembed)


snipe_message_content = None
snipe_message_author = None
snipe_message_id = None


@client.event
@commands.cooldown(1, 4, commands.BucketType.user)
async def on_message_delete(message):

    global snipe_message_content
    global snipe_message_author
    global sn_author_name
    global snipe_message_id

    if message.author.id == 879083602082684968:
        return

    else:
        snipe_message_content = message.content
        snipe_message_author = message.author.id
        snipe_message_id = message.id
        sn_author_name = client.get_user(snipe_message_author)
        await asyncio.sleep(60)

    if message.id == snipe_message_id:
        snipe_message_author = None
        snipe_message_content = None
        snipe_message_id = None
        sn_author_name = None


@client.command()
@commands.cooldown(1, 4, commands.BucketType.user)
async def snipe(message):
    if snipe_message_content == None:
        await message.channel.send("Couldn't find anything to snipe!")
    else:
        embed = discord.Embed(description=snipe_message_content)
        embed.set_footer(
            text=
            f"Asked by {message.author.name}#{message.author.discriminator}",
            icon_url=message.author.avatar_url)
        embed.set_author(name=f"{sn_author_name}")
        await message.channel.send(embed=embed)
        return


@client.command()
@commands.cooldown(1, 4, commands.BucketType.user)
async def ping(ctx):
    await ctx.send(f'{round(client.latency * 1000)}ms')


@client.command(aliases=["av", "pfp"])
@commands.cooldown(1, 4, commands.BucketType.user)
async def avatar(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author

    avatar = member.avatar_url

    embed = discord.Embed(title=f'{member.name}\'s avatar',
                          description=f'[Download]({member.avatar_url})')
    embed.set_footer(
        text=f"Asked by {ctx.author.name}#{ctx.author.discriminator}")
    embed.set_image(url=avatar)
    await ctx.reply(embed=embed)


@client.command(aliases=["mc", "membercount"])
@commands.cooldown(1, 4, commands.BucketType.user)
async def members(ctx):
    member_count = len(ctx.guild.members)
    user_count = len([m for m in ctx.guild.members if not m.bot])
    msg = f"all: `{member_count}`\nusers: `{user_count}`"
    await ctx.reply(msg)


@client.command(pass_context=True, aliases=["clear", "purge"])
@commands.has_permissions(administrator=True)
@commands.cooldown(1, 4, commands.BucketType.user)
async def clean(ctx, Limit: int):
    await ctx.channel.purge(limit=Limit + 1)
    await ctx.send(f'{ctx.author.mention} purged {Limit} messages',
                   delete_after=5)
    await ctx.message.delete()


@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, Member: discord.Member, *, reason='Unspecified'):
    guild = client.get_guild(874440438604496976)
    if Member.id == ctx.author.id:
        await ctx.send("You cannot ban yourself")
        return

    if Member.top_role >= ctx.author.top_role:
        await ctx.send(f"You can only ban members below your top role")
        return

    embed = discord.Embed(title=f'***Banned `{Member}` for `{reason}`***',
                          color=0x38805d)
    dmbed = discord.Embed(description=f'You were banned from `{guild.name}` for `{reason}`.\nDM a staff/owner if you feel this is unjustified')
    await Member.send(embed=dmbed)
    await Member.ban(reason=reason)
    await ctx.send(embed=embed, delete_after=10)
    await ctx.message.delete()


@client.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, *, Member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = Member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name,
                                               member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned `{Member}`', delete_after=10)
            await ctx.message.delete()
            return


@client.command(description="Mute command yay!!", aliases=["shut"])
@commands.has_permissions(manage_messages=True)
async def mute(ctx, Member: discord.Member, *, reason='Unspecified'):
    if Member.id == ctx.author.id:
        await ctx.send("You cannot mute yourself")
        return

    if Member.top_role >= ctx.author.top_role:
        await ctx.send(f"You can only mute members below your top role")
        return
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole,
                                          speak=False,
                                          send_messages=False,
                                          read_message_history=True,
                                          read_messages=False)

    await Member.add_roles(mutedRole, reason=reason)
    embed = discord.Embed(title=f'Muted `{Member}` for `{reason}`')
    await ctx.send(embed=embed, delete_after=10)
    dmbed = discord.Embed(title=f"You were muted in `{guild.name}` for `{reason}`.\nDM a staff/owner if you feel this is unjustified")
    await Member.send(embed=dmbed)
    await ctx.message.delete()


@client.command(description="Unmute command yay!!")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, Member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

    await Member.remove_roles(mutedRole)
    embed = discord.Embed(title=f'Unmuted `{Member}`')
    await ctx.send(embed=embed, delete_after=10)
    dmbed = discord.Embed(title=f"You were unmuted in `{ctx.guild.name}`")
    await Member.send(embed=dmbed)
    await ctx.message.delete()


@client.command(aliases=["abt", 'whois', 'who', 'ui', 'about'],
                description="Gets info about the user")
async def userinfo(ctx, *, member: discord.Member = None):
    if member == None:
        member = ctx.message.author

    embed = discord.Embed(title=f'{member}')
    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(name="Name", value=f'`{member.name}`')
    embed.add_field(name="Nickname", value=f'`{member.nick}`')
    embed.add_field(name="ID", value=f'`{member.id}`')
    embed.add_field(name="Account Created",
                    value=f'<t:{int(member.created_at.timestamp())}:R>')
    embed.add_field(name="Joined",
                    value=f'<t:{int(member.joined_at.timestamp())}:R>')
    members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
    embed.add_field(name="Join Position",
                    value=f'`{str(members.index(member)+1)}`')
    await ctx.send(embed=embed)


@client.command()
async def help(ctx, admin=None):

    nembed = discord.Embed(title="Command list",
                           description="Type '.help admin' for admin commands")
    nembed.add_field(name='.help', value='this command')

    nembed.add_field(
        name='.who',
        value='details about this command (abt, whois, who, ui, about)',
        inline=True)

    nembed.add_field(name='.snipe',
                     value='see the latest deleted message in chat',
                     inline=True)

    nembed.add_field(name='.ping', value='bot\'s ping', inline=True)

    nembed.add_field(name='.av',
                     value='see yours or mentioned\'s avatar',
                     inline=True)

    nembed.add_field(name='.members',
                     value='view member count (mc, membercount)',
                     inline=True)

    nembed.set_footer(text=f"all commands start with the '.' prefix")

    ambed = discord.Embed(
        title="Admin command list",
        description="These commands will only work if you have admin perms",
        color=0xff0000)

    ambed.add_field(name='.ban', value='ban users', inline=True)

    ambed.add_field(name='.unban', value='unban users', inline=True)

    ambed.add_field(name='.mute',
                    value='mute users, they can still read the chat',
                    inline=True)

    ambed.add_field(name='.unmute',
                    value='you guessed it, unmute users',
                    inline=True)

    ambed.add_field(name='.restart',
                    value='reload main.py and `events` cog',
                    inline=True)

    if admin == None:
        await ctx.message.add_reaction('✅')
        await ctx.reply(embed=nembed, delete_after=60)
    elif admin.lower() == 'admin':
        await ctx.message.add_reaction('✅')
        await ctx.reply(embed=ambed, delete_after=60)


client.run(put token here)
