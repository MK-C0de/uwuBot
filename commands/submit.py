import discord, block, blockchain
import commands.user as user

from discord.utils import get
from commands.helper import today, getName

filler = ['<', '>', '!', '@']
"""Exchanges user uwuCreds for (a) raffle ticket(s)"""
async def buy_ticket(ctx, amount, BLOCKCHAIN):
    """1. Blockchain will be evaluated, user cred/ticket total is checked
       2. Blockchain will be validated, new block will be added to the end of Blockchain"""
       
    """Read Blockchain and return user total"""
    id, name = ctx.author.id, ctx.author.name
    user_creds = user.totalCreds(id, BLOCKCHAIN)
    user_tickets = user.totalTickets(id, BLOCKCHAIN)
    
    """Check if User requested -1 to purchase all tickets"""
    total_cost = 0
    if amount < 1:
        count = 0 
        while True:
            cost = 2000 + 400*(user_tickets + count)
            if cost + total_cost < user_creds:
                total_cost += cost
                count += 1
            else: 
                amount = count
                break
    else:
        for i in range(amount):
            total_cost += 2000 + 400*(user_tickets + i)
            
    """Check if User has sufficient amount of uwuCreds"""
    if user_creds - total_cost > 0:
        
        """Generate new Block"""
        new_block1 = block.Block(
            user = id,
            name = name,
            timestamp = today(),
            description = f'Bought {amount} ticket(s)',
            data = -total_cost
        )
        
        new_block2 = block.Block(
            user = id,
            name = name,
            timestamp = today(),
            description = 'Ticket',
            data = amount
        )
        
        """Update Blockchain"""
        if BLOCKCHAIN.isChainValid() == False:
            print('The current Blockchain is not valid, performing rollback.')
            BLOCKCHAIN = blockchain.Blockchain()
    
        BLOCKCHAIN.addBlock(new_block1)
        BLOCKCHAIN.addBlock(new_block2)
        if BLOCKCHAIN.isChainValid():
            BLOCKCHAIN.storeChain()           
    
        """Return Message"""
        embed = discord.Embed(
            title = f'Buy Ticket',
            description = f'Poggerz! **+{amount}** ticket(s) were added to your *Wallet*!',
            color = 15697464    
        ).set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text='@~ powered by oogway desu')
        await ctx.send(embed=embed)
        
    else:
        embed = discord.Embed(
            title = f'Buy Ticket',
            description = f'Insufficient funds, you require **{total_cost}** uwuCreds!',
            color = 6053215    
        ).set_thumbnail(url='https://66.media.tumblr.com/2d52e78a64b9cc97fac0cb00a48fe676/tumblr_inline_pamkf7AfPf1s2a9fg_500.gif')
        embed.set_footer(text='@~ powered by oogway desu')
        await ctx.send(embed=embed)
        
"""Allow moderators to generate one additional submit to a user"""
async def bonusSubmit(ctx, reciever, client, BLOCKCHAIN):
    """1. User will be checked for Moderator status
       2. Blockchain will be validated, new block will be added to the end of Blockchain"""
    
    """Parses Reciever id from <@id>"""
    giver_id, reciever_id = ctx.author.id, reciever
    for ch in filler: reciever_id = reciever_id.replace(ch, '')
    reciever_id = int(reciever_id)
    
    """Check if the Giver is a moderator"""
    role = get(ctx.guild.roles, name='Moderator')
    if role.id in [y.id for y in ctx.author.roles]:
        
        """Generate new Block"""
        new_block = block.Block(
            user = reciever_id,
            name = await getName(reciever_id, client),
            timestamp = today(),
            description = f'Bonus Submit',
            data = 0
        )
        
        """Update Blockchain"""
        if BLOCKCHAIN.isChainValid() == False:
            print('The current Blockchain is not valid, performing rollback.')
            BLOCKCHAIN = blockchain.Blockchain()
    
        BLOCKCHAIN.addBlock(new_block)
        if BLOCKCHAIN.isChainValid():
            BLOCKCHAIN.storeChain()           
        
        """Return Message"""
        embed = discord.Embed(
            title = f'Bonus Submit',
            description = f'Wubba Lubba Dub Dub!\u3000\u3000\u3000\u3000\n**+1** Submit was added to <@{reciever_id}>\'s *Wallet*!',
            color = 16749300    
        ).set_image(url='https://gifimage.net/wp-content/uploads/2017/09/anime-happy-dance-gif-10.gif')
        embed.set_footer(text='@~ powered by oogway desu')
        await ctx.send(embed=embed)
    else: 
        embed = discord.Embed(
            title = f'Bonus Submit',
            description = f'Insufficient power, you are not a moderator!',
            color = 6053215    
        ).set_thumbnail(url='https://media1.tenor.com/images/80662c4e35cf12354f65f1d6f7beada8/tenor.gif')
        embed.set_footer(text='@~ powered by oogway desu')
        await ctx.send(embed=embed)
        
"""Allow users to view a top users, does not display their total uwuCreds"""
async def leaderboard (ctx, BLOCKCHAIN):
    """1. Blockchain will be evaluated, User uwuCreds will be checked
       2. Blockchain will be evaluated, User tickets will be checked"""

    leaderboard = user.getTop(BLOCKCHAIN)
    desc = 'Here lists the most active students on UwUversity!\n\n'
    count = 1
    for member in leaderboard:
        if count == 1:
            desc += f'\u3000** #{count} ** \u3000\u3000 **{member[0]}** \u3000~({member[1]})\n'
            count += 1
            continue

        desc += f'\u3000** #{count} ** '
        if count > 9: desc += '\u3000\u2000'
        else: desc += '\u3000\u3000'
        desc += f'*{member[0]}*\n'
        count += 1
    
    """Return Message"""
    embed = discord.Embed(
        title = f'Leaderboard',
        description = desc,
        color = 6943230    
    ).set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text='@~ powered by oxygen tax')
    await ctx.send(embed=embed)
    
"""Allow users to claim an additional reward after daily submits are used!"""
async def claimBonus (ctx, client, BLOCKCHAIN):
    """1. Blockchain will be evaluated, User daily will be checked
       2. Blockchain will be evaluated, User submits will be checked
       3. Blockchain will be validated, new block will be added to the end of Blockchain"""
       
    id, name = ctx.author.id, ctx.author.name
    user_daily = user.getDailyCount(id, BLOCKCHAIN)
    user_submits = user.totalSubsToday(id, BLOCKCHAIN)
    
    """Check if User has used daily submits before claim"""
    if user_submits < 3:
        embed = discord.Embed(
            title = f'Claim Bonus',
            description = f'You must exhaust your daily submits to claim the *Bonus*!',
            color = 6053215    
        ).set_thumbnail(url='https://media1.tenor.com/images/80662c4e35cf12354f65f1d6f7beada8/tenor.gif')
        embed.set_footer(text='@~ powered by oxygen tax')
        await ctx.send(embed=embed)
        return
    
    if user.hasClaim(id, BLOCKCHAIN) == False:
        embed = discord.Embed(
            title = f'Claim Bonus',
            description = f'You have already claimed your bonus today!',
            color = 6053215    
        ).set_image(url='https://i.pinimg.com/originals/0d/cc/db/0dccdb5a90ed01d7c7c554deba3f66c3.gif')
        embed.set_footer(text='@~ powered by oxygen tax')
        await ctx.send(embed=embed)
        return

    bonus = int(user_daily / 7)
    bonus_creds = 100 + bonus*80
    
    """Generate new Block"""
    new_block = block.Block(
        user = id,
        name = name,
        timestamp = today(),
        description = f'Claim Bonus',
        data = bonus_creds
    )
        
    """Update Blockchain"""
    if BLOCKCHAIN.isChainValid() == False:
        print('The current Blockchain is not valid, performing rollback.')
        BLOCKCHAIN = blockchain.Blockchain()
    
    BLOCKCHAIN.addBlock(new_block)
    if BLOCKCHAIN.isChainValid():
        BLOCKCHAIN.storeChain()           
    
    desc = f'Congratulations on your submits!\n'
    desc += f'From **+{bonus}** *Bonus*, you claimed **+{bonus_creds}** creds!'
        
    """Return Message"""
    embed = discord.Embed(
        title = f'Claim Bonus',
        description = desc,
        color = 16700447    
    ).set_image(url='https://i.pinimg.com/originals/de/6b/5d/de6b5df29abaf7124387b9c86ca46a29.gif')
    embed.set_footer(text='@~ powered by oxygen tax')
    await ctx.send(embed=embed)

"""Allow users to see the list of raffle participants"""
async def rafflelist (ctx, BLOCKCHAIN):
    """1. Blockchain will be evaluated, User uwuCreds will be checked
       2. Blockchain will be evaluated, User tickets will be checked"""

    rafflelist = user.getRaffle(BLOCKCHAIN)
    
    desc = 'Here lists the participating rafflers, the next drawing is Tuesday (8/13)!\n\n'
    count = 1

    mem_list = ''
    for member in rafflelist:
        mem_list += f'\u3000\u3000**{member[1]}**'
        if member[1] > 9: mem_list += '\u3000\u2000'
        else: mem_list += '\u3000\u3000'
        mem_list += f'*{member[0]}*\n'

    if mem_list == '': mem_list += 'Currently there are no participants...'
    else: desc += mem_list
    
    """Return Message"""
    embed = discord.Embed(
        title = f'Current Raffle',
        description = desc,
        color = 6943230    
    ).set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text='@~ powered by oxygen tax')
    await ctx.send(embed=embed)

