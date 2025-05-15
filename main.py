import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from match import Match
from match_status import MatchStatus
from bet import Bet
from help import help_commands

load_dotenv()

# Configuration des Intents
intents = discord.Intents.default()  # Active les intents de base
intents.message_content = True        # Nécessaire pour lire les messages
intents.members = True               # Nécessaire pour voir les membres (si utilisé)

# Dictionnaire pour stocker les matches {id: Match}
matches = {}
current_id_match = 1  # Compteur pour générer des IDs
bets={}
user_scores = {}
point_grid = [10, 7, 5, 3, 1]


bot = commands.Bot(
    command_prefix="!", 
    intents=intents  # <-- Intents passés ici
)
help_commands(bot)

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

def get_roles(member: discord.Member = None):
    roles = [role.name for role in member.roles if role.name != "@everyone"]
    return roles

@bot.command()
async def create_match(ctx, team1: str, team2: str):
    if 'Modo_bot' not in get_roles(ctx.author):
        await ctx.send("Erreur : vous n'avez pas la permission pour effectuer cette commande")
        return
    """Crée un nouveau match entre deux équipes avec un ID unique"""
    global current_id_match
    
    new_match = Match(team1, team2)
    matches[current_id_match] = new_match
    await ctx.send(f"✅ Match créé (ID: {current_id_match}): {new_match}")
    current_id_match += 1


@bot.command()
async def list_matches(ctx):
    """Affiche la liste de tous les matches"""
    if not matches:
        await ctx.send("ℹ️ Aucun match enregistré.")
        return
    
    embed = discord.Embed(
        title="📋 Liste des Matches",
        color=discord.Color.blurple()
    )
    
    for match_id, match in matches.items():
        embed.add_field(
            name=f"🔢 ID {match_id}",
            value=f"{match}",
            inline=False
        )
    
    await ctx.send(embed=embed)

@bot.command()
async def start_match(ctx, match_id : int):
    if 'Modo_bot' not in get_roles(ctx.author):
        await ctx.send("Erreur : vous n'avez pas la permission pour effectuer cette commande")
        return
    if match_id not in matches:
        await ctx.send("Erreur : l'ID indiqué ne corespond à aucun match")
        return
    m = matches[match_id]
    if m.status == MatchStatus.NOT_STARTED:
        m.score = (0,0)
        m.status = MatchStatus.STARTED
    else:
        await ctx.send("Attention on ne peut démarrer qu'un match n'ayant jamais été démarré")
        return
    await ctx.send(f"Match lancé : {m}")
    return

@bot.command()
async def stop_match(ctx, match_id : int, score1 : int, score2 : int):
    if 'Modo_bot' not in get_roles(ctx.author):
        await ctx.send("Erreur : vous n'avez pas la permission pour effectuer cette commande")
        return
    if match_id not in matches:
        await ctx.send("Erreur : l'ID indiqué ne corespond à aucun match")
        return
    m = matches[match_id]
    m.score = (score1, score2)
    m.status = MatchStatus.FINISHED
    if match_id in bets:
        for bet in bets[match_id]:
            bet.set_score_reel(score1, score2)
    ranked_bets = get_rank_bets(match_id)
    update_score(ranked_bets)
    await ctx.send(f"Match arrêté : {m}")

@bot.command()
async def bet(ctx, match_id : int, score1 : int, score2 : int):

    author = ctx.author
    if match_id not in matches:
        await ctx.send("Erreur : l'ID indiqué ne corespond à aucun match")
        return
    m = matches[match_id]
    if m.getstatus() == MatchStatus.STARTED or m.getstatus() == MatchStatus.FINISHED:
        await ctx.send("Ce match a déja commencé")
        return
    if author in get_betters(match_id):
        await ctx.send("Vous avez déjà parié sur ce match")
        return
    bet = Bet(author, score1, score2)
    if match_id not in bets:
        bets[match_id] = []
    bets[match_id].append(bet)
    await ctx.send("Pari bien pris en compte")

def get_betters(match_id: int):
    betters = []
    if match_id not in bets:
        return []
    for bet in bets[match_id]:
        betters.append(bet.author)
    return betters
def get_rank_bets(match_id: int):
    if match_id not in bets:
        return []
    bets_copy = bets[match_id].copy()
    if match_id not in matches:
        raise ValueError
    m = matches[match_id]
    if m.getstatus() != MatchStatus.FINISHED:
        raise ValueError("Cette méthode ne peut être appellée que sur des matchs finis")
    if match_id not in bets:
        return None
    bets_copy.sort()
    return bets_copy
@bot.command()
async def display_bets(ctx, match_id: int):
    if match_id not in bets:
        await ctx.send("Il n'y a aucun pari sur ce match")
        return
    await ctx.send(f"{bets[match_id]}")
    return

@bot.command()
async def display_ranked_bets(ctx, match_id: int):
    await ctx.send(f"{get_rank_bets(match_id)}")
    return

def update_score(ranked_bets):
    p = 0
    n = min(5,len(ranked_bets))
    for i in range(n):
        user = ranked_bets[i].author.name
        if user not in user_scores:
            user_scores[user] = 0
        user_scores[user] += point_grid[p]
        if i+1 < n:
            if ranked_bets[i].loss != ranked_bets[i+1].loss:
                p = i+1
    return
   
@bot.command()
async def display_scores(ctx):
    # Vérifie si le dictionnaire est vide
    if not user_scores:
        embed = discord.Embed(
            title="🏆 Classement des parieurs",
            description="Aucun score à afficher pour le moment.\nPlacez des paris pour apparaître ici !",
            color=0x7289da
        )
        embed.set_footer(text="Utilisez !bet pour commencer à parier !")
        await ctx.send(embed=embed)
        return

    # Trie les utilisateurs par score décroissant
    sorted_scores = sorted(user_scores.items(), key=lambda item: item[1], reverse=True)

    # Crée l'embed
    embed = discord.Embed(
        title="🏆 Classement des parieurs",
        description="Voici les scores de tous les participants :",
        color=0x00ff00  # Couleur verte pour symboliser la réussite
    )

    # Ajoute chaque utilisateur avec son score et une médaille si dans le top 3
    for index, (user, score) in enumerate(sorted_scores, start=1):
        if index == 1:
            medal = "🥇"
        elif index == 2:
            medal = "🥈"
        elif index == 3:
            medal = "🥉"
        else:
            medal = "🔹"
        
        embed.add_field(
            name=f"{medal} {index}. {user}",
            value=f"**Score:** {score} points",
            inline=False
        )

    # Pied de page
    embed.set_footer(text="Continuez à parier pour grimper dans le classement !")
    
    await ctx.send(embed=embed)

@bot.command()
async def timsko(ctx):
    await ctx.send("Oui mon frero 👍🏽")
    return

@bot.command()
async def roles(ctx, member: discord.Member = None):
    # Si aucun membre n'est mentionné, on prend l'auteur du message
    member = member or ctx.author
    
    # Liste des rôles du membre (exclut le rôle @everyone)
    roles = get_roles(member)
    
    await ctx.send(f"{member.display_name} a les rôles: {', '.join(roles) if roles else 'Aucun rôle'}")

if DISCORD_TOKEN is None:
    print("Erreur: Le token Discord n'a pas été trouvé dans le fichier .env")
else:
    bot.run(DISCORD_TOKEN)
