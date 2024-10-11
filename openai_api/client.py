# quadros/signals.py

import google.generativeai as genai
from django.conf import settings

def get_pic_ai_bio(model_name, brand, year):
    try:
        generative_model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"Me mostre uma descrição de venda para o quadro {model_name} {brand} {year} em apenas 250 caracteres. Fale coisas específicas desse modelo."
        response = generative_model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                candidate_count=1,
                stop_sequences=["x"],
                max_output_tokens=250,  # Ajustado para 250 caracteres
                temperature=1.0,
                top_p=0.9,
                top_k=50,  # Valor típico, ajuste conforme necessário
                # Removidos: do_sample=True, include_prefix=True, include_suffix=False
            ),
        )
        print(response.text)
        return response.text.strip()
    except Exception as e:
        print(f"Erro ao gerar a descrição: {e}")
        return None
