import json
import pygame
import sys
import boto3
from botocore.exceptions import ClientError



class SpeechSynthesizer:
    def __init__(self):
        self.polly_client = boto3.client('polly')

    def synthesize(self, text, engine='neural', voice='Joanna', audio_format='mp3', lang_code=None, include_visemes=True):

        """
        Synthesizes speech or speech marks from text, using the specified voice.

        :param text: The text to synthesize.
        :param engine: The kind of engine used. Can be standard or neural.
        :param voice: The ID of the voice to use.
        :param audio_format: The audio format to return for synthesized speech. When
                             speech marks are synthesized, the output format is JSON.
        :param lang_code: The language code of the voice to use. This has an effect
                          only when a bilingual voice is selected.
        :param include_visemes: When True, a second request is made to Amazon Polly
                                to synthesize a list of visemes, using the specified
                                text and voice. A viseme represents the visual position
                                of the face and mouth when saying part of a word.
        :return: The paths to the audio file and viseme file that contains the synthesized speech and a list
                 of visemes that are associated with the speech audio.
        """
        try:
            kwargs = {
                "Engine": engine,
                "OutputFormat": audio_format,
                "Text": text,
                "VoiceId": voice,
            }
            if lang_code is not None:
                kwargs["LanguageCode"] = lang_code

            # Synthesize speech
            response = self.polly_client.synthesize_speech(**kwargs)
            audio_stream = response["AudioStream"].read()

            # Save the audio stream to a file
            audio_file_path = "/home/emoore/speech.mp3"
            with open(audio_file_path, 'wb') as file:
                file.write(audio_stream)
            print(f"Audio file saved to {audio_file_path}")

            viseme_file_path = None
            if include_visemes:
                # Synthesize visemes
                kwargs["OutputFormat"] = "json"
                kwargs["SpeechMarkTypes"] = ["viseme"]
                response = self.polly_client.synthesize_speech(**kwargs)
                visemes = response["AudioStream"].read().decode()

                # Save the visemes to a file
                viseme_file_path = "/home/emoore/visemes.json"
                with open(viseme_file_path, 'w') as file:
                    file.write(visemes)
                print(f"Viseme file saved to {viseme_file_path}")

        except ClientError:
            logger.exception("Couldn't synthesize speech.")
            raise
        else:
            return audio_file_path, viseme_file_path

# Mapping of viseme values to image filenames
viseme_to_filename = {
    'e': '/home/emoore/visemes/lips_e.png',
    'i': '/home/emoore/visemes/lips_e.png',
    'm': '/home/emoore/visemes/lips_m.png',
    'o': '/home/emoore/visemes/lips_o.png',
    'c': '/home/emoore/visemes/lips_c.png',
    'k': '/home/emoore/visemes/lips_c.png',
    't': '/home/emoore/visemes/lips_c.png',
    'a': '/home/emoore/visemes/lips_a.png',
    'u': '/home/emoore/visemes/lips_u.png',
    '@': '/home/emoore/visemes/lips_u.png',
    'E': '/home/emoore/visemes/lips_u.png',
    'O': '/home/emoore/visemes/lips_u.png',
    'th': '/home/emoore/visemes/lips_th.png',
    'f': '/home/emoore/visemes/lips_f.png',
    'w': '/home/emoore/visemes/lips_w.png',
    'ch': '/home/emoore/visemes/lips_ch.png',
    'r': '/home/emoore/visemes/lips_r.png',
    'sil': '/home/emoore/visemes/lips_sil.png',
    'p': '/home/emoore/visemes/lips_m.png',
    's': '/home/emoore/visemes/lips_c.png',  
    'S': '/home/emoore/visemes/lips_ch.png',
    'T': '/home/emoore/visemes/lips_th.png',  
}

# Initialize the screen
# Initialize Pygame
pygame.init()

image = pygame.image.load(viseme_to_filename['p'])  # Replace 'p' with the value of a valid viseme
image_width, image_height = image.get_size()

# Create a window with the size of the image
screen = pygame.display.set_mode((image_width, image_height))

def display_viseme(viseme):
    # Clear the screen
    screen.fill((0, 0, 0))
    
    # Draw the viseme image
    screen.blit(pygame.image.load(viseme_to_filename[viseme]), (0, 0))
    
    # Update the display
    pygame.display.flip()


def display_animation(text):
    synthesizer = SpeechSynthesizer()
    audio_path, viseme_path = synthesizer.synthesize(text=text)

    # Load the speech sound file
    speech_sound = pygame.mixer.Sound(audio_path)

    # Load viseme timings from visemes.json
    with open(viseme_path, 'r') as f:
        viseme_timings = [json.loads(line) for line in f]

    # Set up the display
    image = pygame.image.load(viseme_to_filename['p'])  # Replace 'p' with the value of a valid viseme
    screen = pygame.display.set_mode(image.get_size())

    # Main animation loop
    clock = pygame.time.Clock()
    speech_sound.play()
    start_time = pygame.time.get_ticks()  # Record the start time
    viseme_index = 0

    while pygame.mixer.get_busy() or viseme_index < len(viseme_timings):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time  # Calculate the elapsed time
        if viseme_index < len(viseme_timings) and elapsed_time >= viseme_timings[viseme_index]['time']:
            display_viseme(viseme_timings[viseme_index]['value'])
            viseme_index += 1

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# Example usage
text = "I need to say a lot of stuff to see whether this is working correctly."
display_animation(text)
