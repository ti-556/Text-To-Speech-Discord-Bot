from nextcord.ext import commands
from nextcord import Intents
from voicevox import Client
import nextcord
import requests, json
import io

discordtoken = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix = "!", intents = intents)

@bot.command(name = "tts")
async def tts(ctx, *args):
    text =  " ".join(args)
    user = ctx.message.author
    if user.voice != None:
        try:
            vc = await user.voice.channel.connect()
        except:
            vc = ctx.voice_client
        
        params = {"text": text, "speaker": 1}
        query = requests.post("http://127.0.0.1:50021/audio_query", params=params)
        response = requests.post("http://127.0.0.1:50021/synthesis", headers={"Content-Type": "application/json"}, params=params, data=json.dumps(query.json()))
        with open("ttsvv-audio.wav", "wb") as fp:
            fp.write(response.content)
            
        if vc.is_playing():
            vc.stop
            
        source = await nextcord.FFmpegOpusAudio.from_probe("ttsvv-audio.wav", method = "fallback")
        vc.play(source)
    else:
        await ctx.send("vcに参加してからコマンドを実行してください")

@bot.command(name = "hi")
async def SendMessage(ctx):
    await ctx.send('Hello!')
    
@bot.event
async def on_ready():
    print(f"logged in as: {bot.user.name}")

if __name__ == '__main__':
    bot.run(discordtoken)
