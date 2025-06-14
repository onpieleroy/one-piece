from dotenv import load_dotenv
import discord
from discord.ext import commands
import os
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
load_dotenv()
bot=commands.Bot(command_prefix="!",intents=discord.Intents.default())

np.set_printoptions(suppress=True)

model = load_model("keras_Model.h5", compile=False)

class_names = open("labels.txt", "r").readlines()
manga_index = 0
anime_index = 1
@bot.command()
async def manganime(ctx):
    if not ctx.message.attachments:
        return await ctx.send("Veloceeee... allega un immagine (con !manganime)")
    
    try:
        risposte = []
        for i, attachment in enumerate(ctx.message.attachments):
            await attachment.save(f"temp_img_{i}.jpg")
            image = Image.open(f"temp_img_{i}.jpg").convert("RGB")
            size = (224, 224)
            image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
            image_array = np.asarray(image)
            normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

            data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
            data[0] = normalized_image_array

            prediction = model.predict(data)
            index = np.argmax(prediction)
            class_name = class_names[index].strip()
            confidence_score = prediction[0][index]

            risposte.append(f"**Immagine {i+1}:**{class_name}\n**Confidenza:** {confidence_score:.2%}")
        await ctx.send("\n\n".join(risposte))
    finally:
        for i in range(len(ctx.message.attachments)):
            temp_file = f"temp_img_{i}.jpg"
            if os.path.exists(f"temp_img_{i}.jpg"):
                os.remove(f"temp_img_{i}.jpg")
                
@bot.command()
async def anime(ctx):
    if not ctx.message.attachments:
        return await ctx.send("Veloceeee... allega un immagine (con !anime)")
    
    try:
        risposte = []
        for i, attachment in enumerate(ctx.message.attachments):
            await attachment.save(f"temp_img_{i}.jpg")
            image = Image.open(f"temp_img_{i}.jpg").convert("RGB")
            size = (224, 224)
            image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
            image_array = np.asarray(image)
            normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

            data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
            data[0] = normalized_image_array

            prediction = model.predict(data)
            anime_confidence = prediction[0][anime_index]

            risposte.append(f"**Immagine {i+1}:** Anime\n**Confidenza:** {anime_confidence:.2%}")
        await ctx.send("\n\n".join(risposte))
    finally:
        for i in range(len(ctx.message.attachments)):
            temp_file = f"temp_img_{i}.jpg"
            if os.path.exists(f"temp_img_{i}.jpg"):
                os.remove(f"temp_img_{i}.jpg")

@bot.command()
async def manga(ctx):
    if not ctx.message.attachments:
        return await ctx.send("Veloceeee... allega un immagine (con !manga)")
    
    try:
        risposte = []
        for i, attachment in enumerate(ctx.message.attachments):
            await attachment.save(f"temp_img_{i}.jpg")
            image = Image.open(f"temp_img_{i}.jpg").convert("RGB")
            size = (224, 224)
            image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
            image_array = np.asarray(image)
            normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

            data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
            data[0] = normalized_image_array

            prediction = model.predict(data)
            manga_confidence = prediction[0][manga_index]

            risposte.append(f"**Immagine {i+1}:** Manga\n**Confidenza:** {manga_confidence:.2%}")
        await ctx.send("\n\n".join(risposte))
    finally:
        for i in range(len(ctx.message.attachments)):
            temp_file = f"temp_img_{i}.jpg"
            if os.path.exists(f"temp_img_{i}.jpg"):
                os.remove(f"temp_img_{i}.jpg")
    
bot.run(os.getenv(BOT_TOKEN))