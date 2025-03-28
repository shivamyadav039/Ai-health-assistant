# # voiceBot UI with Gradio
# import os
# import gradio as gr

# from brain_of_the_doctor  import encode_image, analyze_image_with_query
# from voice_of_the_patient import record_audio, transcribe_with_groq
# from voice_of_the_doctor import text_to_speech_with_gtts, text_to_speech_with_elevenlabs


# system_prompt="""You have to act as a professional doctor, i know you are not but this is for learning purpose. 
#             What's in this image?. Do you find anything wrong with it medically? 
#             If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
#             your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
#             Donot say 'In the image I see' but say 'With what I see, I think you have ....'
#             Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
#             Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""


# def process_inputs(audio_filepath, image_filepath):
#     speech_to_text_output = transcribe_with_groq(GROQ_API_KEY=os.environ.get("GROQ_API_KEY"), 
#                                                  audio_filepath=audio_filepath,
#                                                  stt_model="whisper-large-v3")

#     # Handle the image input
#     if image_filepath:
#         doctor_response = analyze_image_with_query(query=system_prompt+speech_to_text_output, encoded_image=encode_image(image_filepath), model="llama-3.2-11b-vision-preview")
#     else:
#         doctor_response = "No image provided for me to analyze"

#     voice_of_doctor = text_to_speech_with_elevenlabs(input_text=doctor_response, output_filepath="final.mp3") 

#     return speech_to_text_output, doctor_response, voice_of_doctor


    

# # Create the interface
# iface = gr.Interface(
#     fn=process_inputs,
#     inputs=[
#         gr.Audio(sources=["microphone"], type="filepath"),
#         gr.Image(type="filepath")
#     ],
#     outputs=[
#         gr.Textbox(label="Speech to Text"),
#         gr.Textbox(label="Doctor's Response"),
#         gr.Audio("Temp.mp3")
#     ],
#     title="AI Doctor with Vision and Voice"
# )

# iface.launch(debug=True)


import os
import gradio as gr
from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import record_audio, transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_elevenlabs

system_prompt = """You have to act as a professional doctor..."""

def process_inputs(audio_filepath, image_filepath):
    speech_to_text_output = transcribe_with_groq(
        GROQ_API_KEY=os.environ.get("GROQ_API_KEY"), 
        audio_filepath=audio_filepath,
        stt_model="whisper-large-v3"
    )

    if image_filepath:
        doctor_response = analyze_image_with_query(
            query=system_prompt + speech_to_text_output, 
            encoded_image=encode_image(image_filepath), 
            model="llama-3.2-11b-vision-preview"
        )
    else:
        doctor_response = "No image provided for analysis."

    voice_of_doctor = text_to_speech_with_elevenlabs(input_text=doctor_response, output_filepath="final.mp3") 

    return speech_to_text_output, doctor_response, voice_of_doctor

# --------------------------------------------
# Building the Interactive Multi-Page UI
# --------------------------------------------

with gr.Blocks(theme="soft") as app:
    gr.Markdown("# 🤖 AI Health Assistant - Virtual Doctor")

    with gr.Tabs():
        # Home Page
        with gr.Tab("🏠 Home"):
            gr.Markdown("## Welcome to the AI Health Assistant!")
            gr.Markdown("### **Key Features:**")
            gr.Markdown("- **Voice-Based Diagnosis** 🎤")
            gr.Markdown("- **Image Analysis for Medical Conditions** 🏥")
            gr.Markdown("- **Instant AI-powered Doctor's Response** 🤖")
            gr.Markdown("- **Secure & Private Consultations** 🔒")

        # AI Doctor Page
        with gr.Tab("🩺 AI Doctor"):
            gr.Markdown("## **Consult the AI Doctor**")
            audio_input = gr.Audio(sources=["microphone"], type="filepath", label="🎤 Speak Your Symptoms")
            image_input = gr.Image(type="filepath", label="📸 Upload a Medical Image (Optional)")

            with gr.Row():
                speech_output = gr.Textbox(label="Speech to Text")
                doctor_response = gr.Textbox(label="Doctor's Response")

            voice_output = gr.Audio(label="Doctor's Voice Response")
            submit_btn = gr.Button("Submit", variant="primary")

            submit_btn.click(
                process_inputs,
                inputs=[audio_input, image_input],
                outputs=[speech_output, doctor_response, voice_output]
            )

        # Services Page
        with gr.Tab("💡 Services"):
            gr.Markdown("## **Our AI Health Services**")
            gr.Markdown("""
            - **Symptom Analysis** 🤕: Get AI-generated diagnoses based on your symptoms.
            - **Image-Based Diagnosis** 📷: Upload images for medical analysis.
            - **AI-Powered Consultation** 💬: Receive instant AI doctor responses.
            - **Voice-Based Interaction** 🎙️: Speak your symptoms instead of typing.
            """)

        # Contact Page
        with gr.Tab("📞 Contact"):
            gr.Markdown("## **Get in Touch**")
            gr.Markdown("Have questions or need support? Contact us!")
            gr.Markdown("- 📧 Email: support@aihealthassistant.com")
            gr.Markdown("- 📞 Phone: +1-800-555-1234")

app.launch(debug=True)















































































































































































