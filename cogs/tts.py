import discord
from discord.ext import commands
from edge_tts import Communicate
import asyncio

class TTSCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    voice_clients = {}

    async def try_join(self, ctx):
        if ctx.guild.id in self.voice_clients:
            await ctx.respond("I'm already connected to a voice channel in this server.")
            return False

        if ctx.author.voice is None:
           await ctx.respond("You must be in a voice channel to use this command.")
           return False

        voice_client = await ctx.author.voice.channel.connect()
        self.voice_clients[voice_client.guild.id] = voice_client
        return True

    @commands.slash_command(name="join", description="join voice channel")
    async def join(self, ctx):
        if (await self.try_join(ctx)):
            await ctx.respond(f"joined {ctx.author.voice.channel.name}")

    @commands.slash_command(name="tts", description="Generate TTS audio from text and play it in a voice channel.")
    async def tts(self, ctx, text: str):
        # get current voice channel / join one that the user is in
        if ctx.guild.id not in self.voice_clients and not await self.try_join(ctx):
            return
        voice_client = self.voice_clients[ctx.guild.id]

        # Generate audio from text
        await Communicate(text, 'en-IE-EmilyNeural').save('tts.mp3')

        # Stop playback if already playing
        if voice_client.is_playing():
            voice_client.stop()

        # Start speaking the TRUTH
        voice_client.play(discord.FFmpegPCMAudio("tts.mp3"))

        # respond to command
        await ctx.respond(f"I say: \"{text}\"")

    @commands.slash_command(name="leave", description="bot leave voice channel")
    async def leave(self, ctx):
        await ctx.guild.voice_client.disconnect()
        self.voice_clients[ctx.guild.id] = None
        await ctx.respond("ok bye")

def setup(client):
    client.add_cog(TTSCommands(client))
