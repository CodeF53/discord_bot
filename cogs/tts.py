import discord
from discord.ext import commands
from edge_tts import Communicate
import asyncio

class TTSCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    voice_clients = {}

    @commands.slash_command(name="join", description="join voice channel")
    async def join(self, ctx):
        if ctx.author.voice is None:
           await ctx.respond("You must be in a voice channel to use this command.")
           return

        voice_client = await ctx.author.voice.channel.connect()
        self.voice_clients[voice_client.guild.id] = voice_client
        await ctx.respond(f"joined {ctx.author.voice.channel.name}")

    @commands.slash_command(name="tts", description="Generate TTS audio from text and play it in a voice channel.")
    async def tts(self, ctx, text: str):
        voice_client = None

        if ctx.guild.id not in self.voice_clients:
            if ctx.author.voice is None:
                await ctx.respond("You must be in a voice channel to use this command.")
                return

            voice_client = await ctx.author.voice.channel.connect()
            self.voice_clients[voice_client.guild.id] = voice_client
        else:
            voice_client = self.voice_clients[ctx.guild.id]

        await Communicate(text, 'en-IE-EmilyNeural').save('tts.mp3')

        voice_client.play(discord.FFmpegPCMAudio("tts.mp3"))

        await ctx.respond("I speak!")

        while voice_client.is_playing():
            await asyncio.sleep(1)

    @commands.slash_command(name="leave", description="bot leave voice channel")
    async def leave(self, ctx):
        await ctx.guild.voice_client.disconnect()
        self.voice_clients[ctx.guild.id] = None
        await ctx.respond("ok")

def setup(client):
    client.add_cog(TTSCommands(client))
