def generatePrompt(prompt, model="gpt-3.5-turbo", temperature=0.7):
    """
    Generates a response from the AI model based on the provided prompt.
    
    Args:
        prompt (str): The input prompt for the AI model.
        model (str): The model to use for generation (default: "gpt-3.5-turbo").
        temperature (float): Controls the randomness of the output (default: 0.7).
    
    Returns:
        str: The generated response from the AI model.
    """
    import openai

    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature
    )
    
    return response.choices[0].message.content.strip()