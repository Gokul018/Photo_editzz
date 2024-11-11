import os
import base64
import mimetypes
import random
import streamlit as st
from io import BytesIO

# Function to create the image gallery
def create_image_gallery(uploaded_files):
    # List of 80 random small quotes
    random_quotes = [
        "Dream big.", "Live in the moment.", "Choose kindness.", "Make today count.", 
        "Be the change.", "Stay positive.", "Keep going.", "Be yourself.", "Believe in yourself.", 
        "You are enough.", "Good things take time.", "Stay humble.", "Create your own luck.", 
        "Enjoy the little things.", "You are stronger than you think.", "Follow your heart.", 
        "Make it happen.", "Do what you love.", "Embrace the journey.", "Stay curious.", 
        "Find beauty in simplicity.", "Live with passion.", "Believe in your dreams.", "Be fearless.", 
        "Your only limit is you.", "Start where you are.", "Live with intention.", "It’s okay to not be okay.", 
        "Don’t stop until you’re proud.", "Let your light shine.", "The best is yet to come.", 
        "Love yourself.", "You are capable of amazing things.", "Life is now.", "Take the risk or lose the chance.", 
        "Never give up.", "Success is a journey.", "Make each day your masterpiece.", 
        "Life is what happens when you’re busy making other plans.", "Be the reason someone smiles today.", 
        "Keep your head up.", "You’ve got this.", "One day at a time.", "Do it with passion or not at all.", 
        "Everything happens for a reason.", "Be proud of how far you’ve come.", "Stay strong.", 
        "Nothing worth having comes easy.", "Believe in magic.", "You miss 100% of the shots you don’t take.", 
        "You’re never too old to dream.", "Life is short, smile while you still have teeth.", 
        "Be a voice, not an echo.", "Keep your dreams alive.", "Progress, not perfection.", "Stay wild.", 
        "Chase your dreams.", "Think happy thoughts.", "You create your own destiny.", "Do it for yourself.", 
        "Life’s a journey, not a destination.", "Make it happen.", "Keep shining.", "Trust the process.", 
        "Learn from yesterday, live for today.", "Life is better when you’re laughing.", "Follow your bliss.", 
        "Live with no regrets.", "Don’t look back, you’re not going that way.", 
        "Sometimes you have to create your own sunshine.", 
        "Don’t wait for the perfect moment, take the moment and make it perfect.", "Happiness is an inside job.", 
        "Life is tough, but so are you.", "The secret to getting ahead is getting started.", 
        "Turn your wounds into wisdom.", "Let it go.", "Fall in love with becoming the best version of yourself.", 
        "Don’t just exist, live.", "Success doesn’t come from what you do occasionally, it comes from what you do consistently.", 
        "When you feel like quitting, remember why you started.", "You are what you believe you are.", 
        "The best way to predict the future is to create it.", "Live your dreams.", "Find your balance.", 
        "Be yourself; everyone else is already taken.", "Make your life a masterpiece."
    ]

    # HTML template with embedded CSS and JavaScript
    html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scattered Image Gallery</title>
    <style>
        body {
            margin: 0;
            padding: 20px;
            background: #f0f0f0;
            min-height: 100vh;
            overflow-x: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-wrap: wrap;
            position: relative;
        }
        .image-container {
            position: absolute;
            cursor: pointer;
            transition: all 0.5s ease;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            background: white;
            padding: 10px;
            border-radius: 5px;
            width: 160px;  /* Smaller fixed width for consistency */
            text-align: center;
            z-index: 100;  /* Higher z-index to ensure images are above the video */
        }
        .image-container img {
            width: 100%;  /* Set width to 100% of the container */
            height: auto;
            border-radius: 3px;
        }
        .caption {
            margin-top: 8px;
            font-family: Arial, sans-serif;
            font-size: 12px;  /* Smaller font size for caption */
            color: #555;
        }

        /* Fade-out animation for disappearing images */
        @keyframes fadeOutShrink {
            0% {
                opacity: 1;
                transform: scale(1) rotate(0deg);
            }
            100% {
                opacity: 0;
                transform: scale(0.5) rotate(45deg);
            }
        }

        .fading {
            animation: fadeOutShrink 1s forwards;
        }

        #video-container {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            display: block;  /* Always visible */
            width: 200px;  /* Set width similar to the images */
            height: auto;
            z-index: 1;  /* Behind images */
            visibility: hidden; /* Initially hidden */
            text-align: center; /* Center the play button */
            border: 10px solid white;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2); /* Polaroid style */
            border-radius: 10px;
            background-color: white;
        }
        video {
            width: 100%;
            height: auto;
            border-radius: 10px;
            display: none;  /* Hide video initially */
        }
        .birthday-text {
            font-size: 18px;
            font-family: 'Comic Sans MS', cursive, sans-serif;
            font-weight: bold;
            color: #f15f5f;
            margin-top: 15px;
            padding: 5px 10px;
            background-color: #fff3e6;
            border-radius: 5px;
        }

        .play-button {
            background-color: #f15f5f;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            border-radius: 5px;
            margin-top: 10px;
        }

        /* Add media queries to make the layout responsive */
        @media (max-width: 768px) {
            #video-container {
                width: 100%;
                max-width: 300px;
                height: auto;
                transform: translate(-50%, -50%);
            }
        }
    </style>
</head>
<body>
    <div id="gallery"></div>
    <div id="video-container">
        <video id="gallery-video" controls muted>
            <source src="VIDEO_PATH" type="video/mp4">
            Your browser does not support the video tag.
        </video>
        <div class="birthday-text" id="birthday-text">Happy Birthday!</div>
        <button class="play-button" id="play-button">Play Video</button>
    </div>
    <script>
        let clickedImages = 0;

        function getRandomPosition(element) {
            const windowWidth = window.innerWidth - 250;
            const windowHeight = window.innerHeight - 250;
            
            const x = Math.random() * windowWidth;
            const y = Math.random() * windowHeight;
            
            return { x, y };
        }

        function createImageElements(images) {
            const gallery = document.getElementById('gallery');
            
            images.forEach((imageData, index) => {
                const { src, caption } = imageData;
                
                const container = document.createElement('div');
                container.className = 'image-container';
                
                const img = document.createElement('img');
                img.src = src;
                container.appendChild(img);
                
                const captionElem = document.createElement('div');
                captionElem.className = 'caption';
                captionElem.innerText = caption;
                container.appendChild(captionElem);
                
                const pos = getRandomPosition(container);
                container.style.left = pos.x + 'px';
                container.style.top = pos.y + 'px';
                container.style.transform = `rotate(${Math.random() * 30 - 15}deg)`; // Random rotation

                // Click event to hide image and track clicks
                container.addEventListener('click', function() {
                    this.classList.add('fading'); // Add fading class for animation
                    
                    setTimeout(() => {
                        this.style.display = 'none';  // Hide the image container after animation
                    }, 1000);  // Delay to match the animation duration
                    
                    clickedImages++; // Increment clicked image count
                    
                    // Check if two images have been clicked (disappeared)
                    if (clickedImages >= 2) {
                        // Make video container visible
                        const videoContainer = document.getElementById('video-container');
                        videoContainer.style.visibility = 'visible';
                    }
                });
                
                gallery.appendChild(container);
            });
        }

        // Play button click event
        document.getElementById('play-button').addEventListener('click', function() {
            const video = document.getElementById('gallery-video');
            video.style.display = 'block'; // Show video element
            video.play(); // Play the video
            this.style.display = 'none'; // Hide the play button after it is clicked
        });

        // Initialize with images and captions
        const imagesList = IMAGES_PLACEHOLDER;
        createImageElements(imagesList);
    </script>
</body>
</html>
'''

    def get_image_base64(image_file):
        try:
            mime_type = mimetypes.guess_type(image_file.name)[0]
            base64_data = base64.b64encode(image_file.read()).decode('utf-8')
            return f"data:{mime_type};base64,{base64_data}"
        except Exception as e:
            print(f"Error processing {image_file.name}: {e}")
            return None

    # Process uploaded images
    image_files = []
    for uploaded_file in uploaded_files:
        base64_image = get_image_base64(uploaded_file)
        if base64_image:
            # Select a random quote from the list of quotes
            random_caption = random.choice(random_quotes)
            # Add the image with a random quote
            image_files.append(f'{{ src: "{base64_image}", caption: "{random_caption}" }}')

    if not image_files:
        st.error("No valid images found.")
        return None

    # Replace placeholder with actual image data (formatted as a JavaScript array)
    html_content = html_template.replace('IMAGES_PLACEHOLDER', f'[{", ".join(image_files)}]')
    # Replace placeholder with the video path
    html_content = html_content.replace('VIDEO_PATH', './video/WhatsApp%20Video%202024-11-11%20at%2013.08.48.mp4')

    # Create output HTML file in memory
    output_file = BytesIO()
    output_file.write(html_content.encode('utf-8'))
    output_file.seek(0)

    return output_file

# Streamlit UI
st.title("Image Gallery Generator")

# Input: Upload images
uploaded_files = st.file_uploader("Choose images", type=["jpg", "jpeg", "png", "gif", "webp"], accept_multiple_files=True)

if uploaded_files:
    # Generate Gallery HTML
    output_file = create_image_gallery(uploaded_files)
    if output_file:
        st.success("Gallery created successfully!")
        
        # Provide download button
        st.download_button(
            label="Download Gallery HTML",
            data=output_file,
            file_name="gallery.html",
            mime="text/html"
        )
    else:
        st.error("Failed to create gallery.")
