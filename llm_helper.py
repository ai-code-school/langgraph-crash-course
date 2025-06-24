def invoke_with_tools_retry(chain, input_data, max_retries=3):
    """Retry the chain invocation until we get tool calls"""
    result = None
    for attempt in range(max_retries):
        result = chain.invoke(input_data)

        # Check if we got tool calls
        if hasattr(result, 'tool_calls') and result.tool_calls:
            print(f"✅ Success on attempt {attempt + 1}")
            return result

        # Check if we got content but no tool calls
        output_tokens = result.usage_metadata.get('output_tokens', 0) if hasattr(result, 'usage_metadata') else 0
        if output_tokens > 10:  # Model generated content but didn't use tools
            print(f"⚠️  Attempt {attempt + 1}: Model generated {output_tokens} tokens but no tool calls")
            print(f"Raw Response: \n{result}")
        else:
            print(f"❌ Attempt {attempt + 1}: No significant response")

    print(f"❌ Failed after {max_retries} attempts")
    return result  # Return last attempt
