from flask import Flask, send_file, request
from PIL import Image, ImageDraw, ImageFont
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import requests
from io import BytesIO
from flask import Flask, render_template
import random
import os
from flask import Flask, send_file
import requests
from PIL import Image
from io import BytesIO

import requests
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

from flask import Flask, send_file, request
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
import requests
from flask import Flask, send_file



from flask_caching import Cache
shape_position = (50, 100)
app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/rank/<name>/<rank_type>')
def generate_rank_image(name, rank_type):
    try:
        # Extract avatar URL from query parameters
        avatar_url = request.args.get('pfp')

        # Determine rank text and color based on rank type
        if rank_type.lower() == 'cat+':
            rank_text = "Cat+"
            rank_color1 = "purple"
            rank_color2 = "white"
            background_url = random.choice([
                'https://wallpapercave.com/wp/wp5171323.jpg',
                'https://wallpapercave.com/wp/wp2057070.jpg',
                # Add more background URLs for "Cat+" rank
            ])
        else:
            rank_text = rank_type
            rank_color1 = "blue"
            rank_color2 = "white"
            background_url = 'https://i.ibb.co/Bwrb0Cv/imageedit-2-6515667300.jpg'  # Default background URL

        # Open and resize background image
        background_response = requests.get(background_url)
        background_response.raise_for_status()
        background = Image.open(BytesIO(background_response.content)).convert("RGBA")
        background = background.resize((600, 202))

        # Create drawing context
        draw = ImageDraw.Draw(background)
        font = ImageFont.truetype("arial.ttf", 28)  # Adjust font and size as needed

        # Blur the background image
        blur_radius = 5
        blurred_background = background.filter(ImageFilter.GaussianBlur(blur_radius))

        # Draw rank text on blurred background
        draw_blurred = ImageDraw.Draw(blurred_background)
        draw_blurred.text((180, 70), f"This is your rank: {rank_text}", font=font, fill=rank_color1)
        draw_blurred.text((175, 70), f"This is your rank: {rank_text}", font=font, fill=rank_color2)

        # Draw main text on original background
        draw.text((180, 70), f"This is your rank: {rank_text}", font=font, fill=rank_color1)
        draw.text((175, 70), f"This is your rank: {rank_text}", font=font, fill=rank_color2)

        # Add additional text and quotes for "Cat+" rank
        if rank_type.lower() == 'cat+':
            # Fetch a quote from the quotable.io API
            quote_api_url = 'https://api.quotable.io/quotes/random?maxLength=40'
            quote_response = requests.get(quote_api_url)
            quote_response.raise_for_status()  # Ensure the request was successful

            # Parse JSON response
            quote_data = quote_response.json()

            if isinstance(quote_data, list) and len(quote_data) > 0:
                # Access the content inside the first element of the list
                quote_text = quote_data[0].get('content', '')
            else:
                quote_text = 'We can win'

            # Draw the quote text on the blurred background
            draw_blurred.text((5, 170), f'"{quote_text}"', font=font, fill="green")
            draw_blurred.text((0, 170), f'"{quote_text}"', font=font, fill="white")

            # Draw additional text
            draw_blurred.text((180, 100), "🎮 GG ezy Your the best!", font=font, fill="blue")
        else:
            # Draw additional text for non-"Cat+" ranks
            draw_blurred.text((180, 100), "Good job enjoy your perks!", font=font, fill="blue")

        # Open and paste avatar onto blurred background
        avatar_response = requests.get(avatar_url)
        avatar_response.raise_for_status()
        avatar = Image.open(BytesIO(avatar_response.content))
        avatar = avatar.resize((120, 120))
        blurred_background.paste(avatar, (30, 35))  # Adjust position as needed

        # Save the resulting image
        image_buffer = BytesIO()
        blurred_background.save(image_buffer, format='PNG')
        image_buffer.seek(0)

        # Return the image file
        return send_file(image_buffer, mimetype='image/png')

    except Exception as e:
        print(e)
        return "An error occurred while generating the rank image.", 500
######################################################################



######################################################################
    
    
@app.route('/vod/<username>/<interval>/<mode>')
def generate_bedwars_image22(username, interval, mode):
    try:
        additional_info_url = f"https://stats.pika-network.net/api/profile/{username}/"
        additional_info_response = requests.get(additional_info_url)

        if additional_info_response.status_code == 200:
            additional_data = additional_info_response.json()
            special_value_username = additional_data.get("username", None)

            if special_value_username:
                bedwars_stats_url = f"https://stats.pika-network.net/api/profile/{special_value_username}/leaderboard?type=bedwars&interval={interval}&mode={mode}"
                bedwars_stats_response = requests.get(bedwars_stats_url)

                if bedwars_stats_response.status_code == 200:
                    pika_data = bedwars_stats_response.json()
                    result_image = generate_bedwars_image22(username, interval, mode, pika_data, additional_data, special_value_username)

                    image_buffer = BytesIO()
                    result_image.save(image_buffer, format='PNG')
                    image_buffer.seek(0)

                    return send_file(image_buffer, mimetype='image/png')
                else:
                    return "Failed to fetch Bed Wars stats.", 500
            else:
                return f"Failed to fetch special value username for {username}.", 500
        else:
            return f"Failed to fetch additional information for {username}.", 500

    except Exception as e:
        print(e)
        return f"🏳️‍⚧️ An error occurred ❌ ., 🛠️ Zumi Bot api Version V1 : Loaded failure noted as {e}", 500

def generate_bedwars_image22(username, interval, mode, pika_data, additional_data, special_value_username):
    # Create a blank transparent image
    result_image = Image.new('RGBA', (1280, 720), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(result_image)

    # Overlay image
    idk_image_url = 'https://i.ibb.co/SsN6TFW/alpha2fgsdg-1-Bedwars-sidktats.png'
    idk_image = Image.open(BytesIO(requests.get(idk_image_url).content)).convert('RGBA')
    idk_image = idk_image.resize((1280, 720), resample=Image.LANCZOS)
    result_image.paste(idk_image, (0, 0), idk_image)

    # Add skin to the image if available
    skin_url = f"https://visage.surgeplay.com/full/512/{username}"
    headers = {'User-Agent': 'Zumi/1.0 (+http://zumi.42web.io/?i=1; Nadhilaplayz@gmail.com)'}
    skin_response = requests.get(skin_url, stream=True, headers=headers)

    if skin_response.status_code == 200:
        skin_image = Image.open(BytesIO(skin_response.content)).convert('RGBA')
        skin_image = skin_image.resize((300, 500), resample=Image.LANCZOS)
        result_image.paste(skin_image, (950, 10), skin_image)
    else:
        # Use default skin image
        default_skin_image = Image.open("default_skin.png").convert('RGBA')
        default_skin_image = default_skin_image.resize((220, 500), resample=Image.LANCZOS)
        result_image.paste(default_skin_image, (980, 10), default_skin_image)

    if additional_data.get("discord_verified"):
        discord_icon_url = "https://th.bing.com/th/id/R.5ff232157d19b921f7dc016519e3c577?rik=qQzQh7EIMFt0sg&pid=ImgRaw&r=0"
        discord_icon = Image.open(BytesIO(requests.get(discord_icon_url).content)).convert('RGBA')
        discord_icon = discord_icon.resize((35, 35), resample=Image.LANCZOS)
        result_image.paste(discord_icon, (995, 645), discord_icon)

    if additional_data.get("email_verified"):
        email_icon_url = "https://logos-world.net/wp-content/uploads/2020/11/Gmail-Logo.png"
        email_icon = Image.open(BytesIO(requests.get(email_icon_url).content)).convert('RGBA')
        email_icon = email_icon.resize((35, 25), resample=Image.LANCZOS)
        result_image.paste(email_icon, (950, 650), email_icon)

    skin_url2 = f"https://visage.surgeplay.com/face/512/{special_value_username}"
    headers = {'User-Agent': 'Zumi/1.0 (+http://zumi.42web.io/?i=1; Nadhilaplayz@gmail.com)'}
    skin_response2 = requests.get(skin_url2, stream=True, headers=headers)

    print("Head Image API Response Status Code:", skin_response2.status_code)  # Debugging line

    if additional_data.get("ranks"):
      rank_display_name = additional_data["ranks"][0].get("displayName", "N/A")
      rank_level = additional_data["ranks"][0].get("level", 0)

      # Define colors based on rank
      if rank_display_name == "Vip":
          rank_color = "green"
      elif rank_display_name == "Elite":
          rank_color = "lightblue"  # You mentioned light aqua, lightblue is closer
      elif rank_display_name == "Titan":
          rank_color = "yellow"
      else:
          rank_color = "white"  # Default color if rank not specified

      draw.text((395, 45), f": {rank_display_name}", fill=rank_color, font=ImageFont.truetype("mine.ttf", 40))
    else:
      print("No ranks found")


    if skin_response2.status_code == 200:
        skin_image2 = Image.open(BytesIO(skin_response2.content)).convert('RGBA')
        skin_image = skin_image2.resize((45, 45), resample=Image.LANCZOS)
        result_image.paste(skin_image, (20, 50), skin_image)
        # Save the image locally for inspection
        skin_image2.save("head_image.png")  # Debugging line
    else:
        print("Failed to retrieve head image.")  # Debugging line

    # Drawing text and statistic\

  
    draw.text((75, 45), f"| {username.replace('_', ' ').capitalize()} ", fill='white', font=ImageFont.truetype("mine.ttf", 40))

    
    draw.text((600, 650), f"({mode.replace('_', ' ').lower()}) ({interval.lower().capitalize()})", fill='white', font=ImageFont.truetype("mine.ttf", 20))
    rank_level = additional_data["rank"].get("level", "N/A")

    stat_positions = [
        ("Wins", get_entry_value(pika_data, "Wins"), (100, 200)),
        ("Losses", get_entry_value(pika_data, "Losses"), (410, 200)),
        ("Final deaths", get_entry_value(pika_data, "Final deaths"), (417, 320)),
        ("Final kills", get_entry_value(pika_data, "Final kills"), (85, 320)),
        ("Beds broken", get_entry_value(pika_data, "Beds destroyed"), (87, 565)),
        ("Beds lost", get_entry_value(pika_data, "Losses"), (412, 565)),
        ("Kills", get_entry_value(pika_data, "Kills"), (85, 440)),
        ("Deaths", get_entry_value(pika_data, "Deaths"), (405, 440)),
    ]

    

    for stat_name, stat_value, position in stat_positions:
        draw.text(position, f"{stat_value}", fill='white', font=ImageFont.truetype("arial.ttf", 40))

    highest_winstreak_value = get_entry_value(pika_data, "Highest winstreak reached")
    draw.text((735, 440), f"{highest_winstreak_value}", fill='white', font=ImageFont.truetype("arial.ttf", 36))

    # Api section

    final_deaths = int(get_entry_value(pika_data, "Final deaths"))
    final_kills = int(get_entry_value(pika_data, "Final kills"))
    final_kill_to_death_ratio = final_kills / final_deaths if final_deaths > 0 else final_kills
    draw.text((725, 320), f"{final_kill_to_death_ratio:.2f}", fill='white', font=ImageFont.truetype("arial.ttf", 36))

    wins = int(get_entry_value(pika_data, "Wins"))
    losses = int(get_entry_value(pika_data, "Losses"))
    win_to_loss_ratio = wins / losses if losses > 0 else wins
    draw.text((735, 200), f"{win_to_loss_ratio:.2f}", fill='white', font=ImageFont.truetype("arial.ttf", 36))

    games_played = get_entry_value(pika_data, "Games played")
    draw.text((730, 565), f"{games_played}", fill='white', font=ImageFont.truetype("arial.ttf", 36))

    if additional_data.get("clan"):
        clan_name = additional_data["clan"].get("name", "No Clan")
        draw.text((950, 570), f"{clan_name}", fill='purple', font=ImageFont.truetype("mine.ttf", 36))
    else:
        draw.text((960, 570), "No Guild", fill='white', font=ImageFont.truetype("mine.ttf", 40))

    if additional_data.get("rank"):
        rank_level = additional_data["rank"].get("level", "N/A")
        draw.text((950, 610), f"Network Level: @{rank_level}", fill='pink', font=ImageFont.truetype("mine.ttf", 26))
    else:
        draw.text((950, 610), "No Levels Found!", fill='red', font=ImageFont.truetype("mine.ttf", 26))

    return result_image
    
############################################################################

@app.route('/bw/<username>/<interval>/<mode>')
def generate_bedwars_image(username, interval, mode):
    try:
        additional_info_url = f"https://stats.pika-network.net/api/profile/{username}/"
        additional_info_response = requests.get(additional_info_url)

        if additional_info_response.status_code == 200:
            additional_data = additional_info_response.json()
            special_value_username = additional_data.get("username", None)

            if special_value_username:
                bedwars_stats_url = f"https://stats.pika-network.net/api/profile/{special_value_username}/leaderboard?type=bedwars&interval={interval}&mode={mode}"
                bedwars_stats_response = requests.get(bedwars_stats_url)

                if bedwars_stats_response.status_code == 200:
                    pika_data = bedwars_stats_response.json()
                    result_image = generate_bedwars_image(username, interval, mode, pika_data, additional_data, special_value_username)

                    image_buffer = BytesIO()
                    result_image.save(image_buffer, format='PNG')
                    image_buffer.seek(0)

                    return send_file(image_buffer, mimetype='image/png')
                else:
                    return "Failed to fetch Bed Wars stats.", 500
            else:
                return f"Failed to fetch special value username for {username}.", 500
        else:
            return f"Failed to fetch additional information for {username}.", 500

    except Exception as e:
        print(e)
        return f"🏳️‍⚧️ An error occurred ❌ ., 🛠️ Zumi Bot api Version V1 : Loaded failure noted as {e}", 500

def generate_bedwars_image(username, interval, mode, pika_data, additional_data, special_value_username):
    result_image = Image.new('RGBA', (1280, 720), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(result_image)

    # Background
    if additional_data.get("rank", {}).get("level", 0) >= 6:
        background_urls = [
            'https://wallpaperaccess.com/full/2936972.jpg',  # Japanese Street at Night
            'https://th.bing.com/th/id/R.46e91d3ebbe8ae4642f7bc094310dbd8?rik=fjseaUEGM6tVng&pid=ImgRaw&r=0',
            'https://wallpaperaccess.com/full/4583657.png',

        ]

        random_background_url = random.choice(background_urls)
        background_image = Image.open(BytesIO(requests.get(random_background_url).content)).convert('RGBA')
        background_image = background_image.resize((1280, 720), resample=Image.LANCZOS)
    else:
        background_image = Image.open("Rise1-0.png").convert('RGBA')
        background_image = background_image.resize((1280, 720), resample=Image.LANCZOS)

    result_image.paste(background_image, (0, 0))

    # Overlay image
    idk_image_url = 'https://i.ibb.co/SsN6TFW/alpha2fgsdg-1-Bedwars-sidktats.png'
    idk_image = Image.open(BytesIO(requests.get(idk_image_url).content)).convert('RGBA')
    idk_image = idk_image.resize((1280, 720), resample=Image.LANCZOS)
    result_image.paste(idk_image, (0, 0), idk_image)

    # Add skin to the image if available
    skin_url = f"https://visage.surgeplay.com/full/512/{username}"
    headers = {'User-Agent': 'Zumi/1.0 (+http://zumi.42web.io/?i=1; Nadhilaplayz@gmail.com)'}
    skin_response = requests.get(skin_url, stream=True, headers=headers)

    if skin_response.status_code == 200:
        skin_image = Image.open(BytesIO(skin_response.content)).convert('RGBA')
        skin_image = skin_image.resize((300, 500), resample=Image.LANCZOS)  
        result_image.paste(skin_image, (950, 10), skin_image)
    else:
        # Use default skin image
        default_skin_image = Image.open("default_skin.png").convert('RGBA')
        default_skin_image = default_skin_image.resize((220, 500), resample=Image.LANCZOS)
        result_image.paste(default_skin_image, (980, 10), default_skin_image)

    if additional_data.get("discord_verified"):
        discord_icon_url = "https://th.bing.com/th/id/R.5ff232157d19b921f7dc016519e3c577?rik=qQzQh7EIMFt0sg&pid=ImgRaw&r=0"
        discord_icon = Image.open(BytesIO(requests.get(discord_icon_url).content)).convert('RGBA')
        discord_icon = discord_icon.resize((35, 35), resample=Image.LANCZOS)
        result_image.paste(discord_icon, (995, 645), discord_icon)

    if additional_data.get("email_verified"):
        email_icon_url = "https://logos-world.net/wp-content/uploads/2020/11/Gmail-Logo.png"
        email_icon = Image.open(BytesIO(requests.get(email_icon_url).content)).convert('RGBA')
        email_icon = email_icon.resize((35, 25), resample=Image.LANCZOS)
        result_image.paste(email_icon, (950, 650), email_icon)

    skin_url2 = f"https://visage.surgeplay.com/face/512/{special_value_username}"
    headers = {'User-Agent': 'Zumi/1.0 (+http://zumi.42web.io/?i=1; Nadhilaplayz@gmail.com)'}
    skin_response2 = requests.get(skin_url2, stream=True, headers=headers)

    print("Head Image API Response Status Code:", skin_response2.status_code)  # Debugging line

    if additional_data.get("ranks"):
      rank_display_name = additional_data["ranks"][0].get("displayName", "N/A")
      rank_level = additional_data["ranks"][0].get("level", 0)

      # Define colors based on rank
      if rank_display_name == "Vip":
          rank_color = "green"
      elif rank_display_name == "Elite":
          rank_color = "lightblue"  # You mentioned light aqua, lightblue is closer
      elif rank_display_name == "Titan":
          rank_color = "yellow"
      else:
          rank_color = "white"  # Default color if rank not specified

      draw.text((395, 45), f": {rank_display_name}", fill=rank_color, font=ImageFont.truetype("mine.ttf", 40))
    else:
      print("No ranks found")


    if skin_response2.status_code == 200:
        skin_image2 = Image.open(BytesIO(skin_response2.content)).convert('RGBA')
        skin_image = skin_image2.resize((45, 45), resample=Image.LANCZOS)
        result_image.paste(skin_image, (20, 50), skin_image)
        # Save the image locally for inspection
        skin_image2.save("head_image.png")  # Debugging line
    else:
        print("Failed to retrieve head image.")  # Debugging line

    # Drawing text and statistic\

  
    draw.text((75, 45), f"| {username.replace('_', ' ').capitalize()} ", fill='white', font=ImageFont.truetype("mine.ttf", 40))

    
    draw.text((600, 650), f"({mode.replace('_', ' ').lower()}) ({interval.lower().capitalize()})", fill='white', font=ImageFont.truetype("mine.ttf", 20))
    rank_level = additional_data["rank"].get("level", "N/A")

    stat_positions = [
        ("Wins", get_entry_value(pika_data, "Wins"), (100, 200)),
        ("Losses", get_entry_value(pika_data, "Losses"), (410, 200)),
        ("Final deaths", get_entry_value(pika_data, "Final deaths"), (417, 320)),
        ("Final kills", get_entry_value(pika_data, "Final kills"), (85, 320)),
        ("Beds broken", get_entry_value(pika_data, "Beds destroyed"), (87, 565)),
        ("Beds lost", get_entry_value(pika_data, "Losses"), (412, 565)),
        ("Kills", get_entry_value(pika_data, "Kills"), (85, 440)),
        ("Deaths", get_entry_value(pika_data, "Deaths"), (405, 440)),
    ]

    

    for stat_name, stat_value, position in stat_positions:
        draw.text(position, f"{stat_value}", fill='white', font=ImageFont.truetype("arial.ttf", 40))

    highest_winstreak_value = get_entry_value(pika_data, "Highest winstreak reached")
    draw.text((735, 440), f"{highest_winstreak_value}", fill='white', font=ImageFont.truetype("arial.ttf", 36))

    # Api section

    final_deaths = int(get_entry_value(pika_data, "Final deaths"))
    final_kills = int(get_entry_value(pika_data, "Final kills"))
    final_kill_to_death_ratio = final_kills / final_deaths if final_deaths > 0 else final_kills
    draw.text((725, 320), f"{final_kill_to_death_ratio:.2f}", fill='white', font=ImageFont.truetype("arial.ttf", 36))

    wins = int(get_entry_value(pika_data, "Wins"))
    losses = int(get_entry_value(pika_data, "Losses"))
    win_to_loss_ratio = wins / losses if losses > 0 else wins
    draw.text((735, 200), f"{win_to_loss_ratio:.2f}", fill='white', font=ImageFont.truetype("arial.ttf", 36))

    games_played = get_entry_value(pika_data, "Games played")
    draw.text((730, 565), f"{games_played}", fill='white', font=ImageFont.truetype("arial.ttf", 36))

    if additional_data.get("clan"):
        clan_name = additional_data["clan"].get("name", "No Clan")
        draw.text((950, 570), f"{clan_name}", fill='purple', font=ImageFont.truetype("mine.ttf", 36))
    else:
        draw.text((960, 570), "No Guild", fill='white', font=ImageFont.truetype("mine.ttf", 40))

    if additional_data.get("rank"):
        rank_level = additional_data["rank"].get("level", "N/A")
        draw.text((950, 610), f"Network Level: @{rank_level}", fill='pink', font=ImageFont.truetype("mine.ttf", 26))
    else:
        draw.text((950, 610), "No Levels Found!", fill='red', font=ImageFont.truetype("mine.ttf", 26))

    return result_image

def get_entry_value(data, key):
  entry_data = data.get(key, {}).get('entries', None)
  if entry_data is not None:
      return entry_data[0].get('value', 'N/A')
  else:
      return 0
background_font = ImageFont.truetype("arial.ttf", 24)
level_font = ImageFont.truetype("arial.ttf", 20)

def draw_rounded_rectangle(draw, position, size, color, radius):
  x, y = position
  width, height = size
  draw.rectangle([x, y + radius, x + width, y + height - radius], fill=color)
  draw.rectangle([x + radius, y, x + width - radius, y + height], fill=color)
  draw.pieslice([x, y, x + radius * 2, y + radius * 2], 180, 270, fill=color)
  draw.pieslice([x + width - radius * 2, y, x + width, y + radius * 2], 270, 360, fill=color)
  draw.pieslice([x, y + height - radius * 2, x + radius * 2, y + height], 90, 180, fill=color)
  draw.pieslice([x + width - radius * 2, y + height - radius * 2, x + width, y + height], 0, 90, fill=color)

def draw_progress_bar(draw, position, size, progress, color):
  x, y = position
  width, height = size
  progress_width = int(width * progress)
  draw.rectangle([x, y, x + progress_width, y + height], fill=color)

@app.route('/lvls/<int:level>/<int:messages>/<guild_name>')
def generate_level_image(level, messages, guild_name):
  try:
      # Create a blank image with the specified dimensions
      image_width = 600
      image_height = 200
      background_color = (54, 57, 63)  # Discord background color
      background = Image.open("backgb2.png")  # Load custom background image
      background = background.resize((image_width, image_height))  # Resize background image

      # Create a drawing context
      draw = ImageDraw.Draw(background)
      font = ImageFont.truetype("arial.ttf", 20)  # Adjust font and size as needed

      # Add guild name text at the top
      guild_text = f"AKA {guild_name}"
      guild_text_bbox = draw.textbbox((0, 0), guild_text, font=font)
      guild_text_width = guild_text_bbox[2] - guild_text_bbox[0]
      draw.text((430, 180), guild_text, fill=(255, 255, 255), font=font)

      # Load user avatar
      avatar_url = request.args.get('pfp')
      if avatar_url:
          avatar_response = requests.get(avatar_url)
          if avatar_response.status_code == 200:
              avatar_image = Image.open(BytesIO(avatar_response.content)).convert('RGBA')
              avatar_size = (150, 150)  # Larger avatar size
              avatar_image = avatar_image.resize(avatar_size, resample=Image.LANCZOS)
              background.paste(avatar_image, (430, 20), avatar_image)

      # Add level, messages, and progress bar inside a rectangle
      rectangle_position = (20, 20)  # Adjusted position
      rectangle_size = (image_width - 50 - avatar_size[0], 160)  # Adjusted size
      rectangle_color = (32, 34, 37)  # Dark grey color
      draw_rounded_rectangle(draw, rectangle_position, rectangle_size, rectangle_color, 10)

      # Add level text
      level_text = f"Level: {level}"
      draw.text((rectangle_position[0] + 20, 50), level_text, fill=(255, 255, 255), font=font)

      # Add messages text
      messages_text = f"Messages: {messages}"
      draw.text((rectangle_position[0] + 20, 80), messages_text, fill=(255, 255, 255), font=font)

      # Draw progress bar
      progress_bar_position = (rectangle_position[0] + 20, 100)  # Adjusted position
      progress_bar_size = (rectangle_size[0] - 40, 20)  # Adjusted size
      progress_color = (114, 137, 218)  # Discord accent color
      progress = min(level / 100, 1.0)
      progressed = 9# Cap progress at 100%
      draw_progress_bar(draw, progress_bar_position, progress_bar_size, progress, progress_color)


      # Add progress text
      progress_text = f"Progress: {progress:.1%}"
      draw.text((rectangle_position[0] + 20, 150), progress_text, fill=(255, 255, 255), font=font)

      # Save the resulting image to a BytesIO buffer
      image_buffer = BytesIO()
      background.save(image_buffer, format='PNG')
      image_buffer.seek(0)

      # Return the image file
      return send_file(image_buffer, mimetype='image/png')

  except Exception as e:
      error_message = f"An error occurred while generating the level image: {str(e)}"
      print(error_message)
      return error_message, 500


 
if __name__ == "__main__":
    app.run(debug=True)
