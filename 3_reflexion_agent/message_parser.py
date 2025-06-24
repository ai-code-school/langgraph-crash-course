import json
from typing import re

from schema import AnswerQuestion, Reflection


def build_aq_schema(args):
    if isinstance(args.get("reflection"), str):
        # Dummy transformation: you must implement a real parser if needed
        args["reflection"] = Reflection(
            missing="reflexion",
            superfluous=args.get("reflection")
        )
    return AnswerQuestion(**args)

def extract_answer_tools(ai_message):
    """Manual parser to replace PydanticToolsParser"""
    if not hasattr(ai_message, 'tool_calls') or not ai_message.tool_calls:
        return []

    results = []
    for tool_call in ai_message.tool_calls:
        if tool_call['name'] == 'AnswerQuestion':

            # Create AnswerQuestion object from tool call args
            answer_obj = build_aq_schema(tool_call['args'])
            results.append(answer_obj)

    return results


def parse_ollama_response(ai_message):
    """
    Unified parser that handles Ollama's inconsistent response format.
    Checks both tool_calls and content attributes.
    """
    results = []

    # Method 1: Check for proper tool_calls first
    if hasattr(ai_message, 'tool_calls') and ai_message.tool_calls:
        print("✅ Found tool_calls - using standard parsing")
        for tool_call in ai_message.tool_calls:
            if tool_call['name'] == 'AnswerQuestion':
                try:
                    # Handle field name variations
                    args = tool_call['args'].copy()

                    # Ensure required fields exist
                    if 'reflection' not in args:
                        args['reflection'] = {}
                    if 'description' not in args:
                        args['description'] = ""

                    answer_obj = AnswerQuestion(**args)
                    results.append(answer_obj)
                except Exception as e:
                    print(f"❌ Error parsing tool call: {e}")
                    print(f"Args: {tool_call['args']}")

        if results:
            return results

    # Method 2: Check content for JSON (when tool_calls fails)
    if ai_message.content:
        print("🔄 No tool_calls found - checking content for JSON")
        try:
            # Clean the content
            content = ai_message.content.strip()

            # Remove markdown formatting if present
            content = re.sub(r'^```json\s*', '', content)
            content = re.sub(r'\s*```$', '', content)

            # Try to parse as direct JSON
            try:
                parsed = json.loads(content)
                print("✅ Parsed content as direct JSON")
            except json.JSONDecodeError:
                # Look for JSON-like structure within the content
                json_match = re.search(r'\{.*"name":\s*"AnswerQuestion".*\}', content, re.DOTALL)
                if json_match:
                    json_str = json_match.group(0)
                    parsed = json.loads(json_str)
                    print("✅ Extracted JSON from content")
                else:
                    print("❌ No valid JSON found in content")
                    return results

            # Handle different JSON structures
            if "parameters" in parsed:
                # Format: {"name": "AnswerQuestion", "parameters": {...}}
                tool_args = parsed["parameters"]
            elif "args" in parsed:
                # Format: {"name": "AnswerQuestion", "args": {...}}
                tool_args = parsed["args"]
            else:
                # Direct format: {"answer": "...", "description": "...", "reflection": "..."}
                tool_args = parsed

            # Ensure required fields
            if 'reflection' not in tool_args:
                tool_args['reflection'] = {}
            if 'description' not in tool_args:
                tool_args['description'] = ""

            answer_obj = AnswerQuestion(**tool_args)
            results.append(answer_obj)
            print("✅ Successfully created AnswerQuestion object from content")

        except Exception as e:
            print(f"❌ Error parsing content: {e}")
            print(f"Content preview: {ai_message.content[:200]}...")

    if not results:
        print("❌ No valid responses found in either tool_calls or content")

    return results