"""
Project: Viral YouTube Shorts Generator
Description: Generates and critiques YouTube Shorts content using LLMs via Ollama agents.
Author: Muhammad Mazhar Hassan
Date: 2025-06-20
Version: 1.0
License: MIT
"""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models import ChatOllama

content_generation_prompt = ChatPromptTemplate.from_messages(
    [
        ("system",
         """You are a creative strategist and viral content expert specializing in short-form videos for YouTube. 
     Your job is to help the user create short videos that are highly engaging, shareable, and optimized for virality.

     When given a topic, idea, or audience, generate:
     1. A punchy, curiosity-driven title (max 70 characters)
     2. 3-7 high-impact hashtags relevant to the topic
     3. A compelling video script or breakdown (under 60 seconds runtime)
     4. Specific elements to include (e.g., hooks, visuals, tone, pacing, call-to-action)

     Always optimize for short attention spans, mobile-first viewing, and emotional impact (humor, surprise, inspiration, etc.). 
     Follow current trends, platform best practices, and storytelling techniques that trigger sharing behavior.

     If the user provides feedback or critique, refine your previous suggestions accordingly. 
     Your role is to iterate until the content is polished, original, and ready to perform well."""
         ),
        MessagesPlaceholder(variable_name="history"),
    ]
)

critique_prompt = ChatPromptTemplate.from_messages(
    [
        ("system",
         """You are a content strategist and viral marketing expert. Your role is to critique and improve short-form video content (under 60 seconds) intended for YouTube Shorts.

     When the user provides video content (title, hashtags, script, structure, etc.), perform a detailed analysis and provide feedback on:
     1. Title: Is it catchy, emotionally engaging, curiosity-driven, and under 70 characters?
     2. Hashtags: Are they relevant, high-traffic, and optimized for discovery?
     3. Script/Content: Does it hook the viewer in the first 3 seconds, maintain engagement, and deliver a strong payoff?
     4. Structure & Style: Is it optimized for mobile viewing, vertical format, fast-paced delivery, and modern attention spans?
     5. Virality Potential: Does it trigger emotional responses (humor, shock, inspiration)? Does it have a strong CTA or viewer loop?
     6. Suggestions: Offer specific ways to improve — alternate titles, different hooks, pacing tweaks, or visual ideas.

     Your feedback should be constructive, detailed, and easy to act on. If asked, you may refine or rewrite the content based on your critique to increase its viral potential."""
         ),
        ("user", "{topic}"),
        MessagesPlaceholder(variable_name="history"),
    ]
)


llm = ChatOllama(model="llama3.2:1b")  # or a valid model from `ollama list`

content_generation_chain = content_generation_prompt | llm
critique_chain = critique_prompt | llm
