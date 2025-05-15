import discord
def help_commands(bot):

    @bot.command()
    async def help_command(ctx):
        embed = discord.Embed(
            title="📋 Aide du Système de Paris Sportifs",
            description="Commandes disponibles pour parier sur les matchs :",
            color=0x7289da  # Couleur bleue Discord
        )
        
        # Commandes avec des champs séparés pour une meilleure lisibilité
        embed.add_field(
            name="🎯 Créer un match",
            value="`!create_match [équipe1] [équipe2]`\nCrée un nouveau match entre deux équipes",
            inline=False
        )
        
        embed.add_field(
            name="📜 Lister les matchs",
            value="`!list_matches`\nAffiche tous les matchs en cours et terminés",
            inline=False
        )
        
        embed.add_field(
            name="💰 Placer un pari",
            value="`!bet [ID_Match] [score1] [score2]`\nPariez sur le score final d'un match",
            inline=False
        )
        
        embed.add_field(
            name="🚦 Démarrer un match (bloque les paris)",
            value="`!start_match [ID_Match]`\nDémarre le match et bloque les nouveaux paris",
            inline=False
        )
        
        embed.add_field(
            name="🏁 Terminer un match",
            value="`!stop_match [ID_Match] [score1] [score2]`\nEnregistre le résultat final et calcule les gains",
            inline=False
        )
        
        embed.add_field(
            name="🏆 Voir les paris classés",
            value="`!display_ranked_bets [ID_Match]`\nAffiche les paris triés par proximité avec le résultat",
            inline=False
        )
        
        embed.add_field(
            name="📊 Classement général",
            value="`!display_scores`\nAffiche le classement de tous les parieurs",
            inline=False
        )
        
        # Pied de page avec des emojis
        embed.set_footer(text="⚽ Bonne chance pour vos paris ! 🏀")
        
        await ctx.send(embed=embed)