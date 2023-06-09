from nextcord.ext import commands
from nextcord import Intents
from gtts import gTTS
from voicevox import Client
import nextcord

token = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

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
        
        sound = gTTS(text=text, lang="ja", slow = False)
        sound.save("tts-audio.wav")
            
        if vc.is_playing():
            vc.stop
            
        source = await nextcord.FFmpegOpusAudio.from_probe("tts-audio.wav", method = "fallback")
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
    bot.run(token)
