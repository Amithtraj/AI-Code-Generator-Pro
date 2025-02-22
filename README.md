# AI Code Generator Pro 🤖💻

AI Code Generator Pro is a powerful tool that utilizes AI to generate, debug, and save code based on user-defined requirements. Built using Python and Tkinter for the graphical user interface, this app allows users to quickly generate clean, production-ready code in multiple programming languages, debug existing code, and save the generated output to a file. 

## Features ✨

- **Generate Code**: Enter your requirements and get fully functional, production-ready code with best practices, error handling, and validation.
- **Debug Code**: Paste your code and the error message, and let the AI fix issues while maintaining the original functionality.
- **Save Code**: Save the generated or debugged code to your system with the appropriate file extension for the chosen language.
- **Multiple Languages**: Supports Python, JavaScript, Java, C++, TypeScript, and HTML.
- **Retry Mechanism**: Built-in retries for API calls to ensure smooth operations even during network or service interruptions.
- **Customizable API Configuration**: The app connects to a customizable API that can be adjusted for different endpoints, models, and keys.
- **Responsive UI**: Built using Tkinter for a user-friendly, intuitive experience.

## Prerequisites 🛠️

To run this application, you need:

- **Python 3.x** installed on your system.
- **Tkinter** (usually included with Python).
- **Requests** library for API communication (can be installed via `pip install requests`).
- A working API endpoint for generating code (this app is configured to work with a local server at `http://localhost:1234/v1/chat/completions`).

## Installation 🔧

1. Clone or download this repository to your local machine:
    ```bash
    git clone https://github.com/yourusername/ai-code-generator-pro.git
    ```

2. Navigate to the project directory and install the required dependencies:
    ```bash
    pip install requests
    ```

3. Ensure you have a running API server at the configured URL (`http://localhost:1234/v1/chat/completions`) or modify the `API_URL` in the code to match your endpoint.

4. Run the application:
    ```bash
    python app.py
    ```

## Usage 📘

- **Input Requirements**: Type the code requirements in the provided text box, specify the programming language, and click **Generate Code**.
- **Generate Code**: Once the code is generated, it will appear in the output text box. You can then debug, save, or modify it further.
- **Debug Code**: If you're debugging existing code, paste it into the output section, and provide the error message when prompted.
- **Save Code**: Once satisfied with the generated or debugged code, click **Save Code** to save it as a file on your machine.
- **Settings**: Access the settings to configure API connection parameters (coming soon).

## Example Workflows ⚙️

1. **Generate Python Code**:  
    - Enter a description like: "Create a Python program that sorts a list of numbers using merge sort."
    - Select Python from the language dropdown.
    - Hit **Generate Code** and the app will provide the full code.

2. **Debug JavaScript Code**:  
    - Paste your JavaScript code that contains errors.
    - Enter the error message that you are receiving (e.g., "TypeError: Cannot read property 'map' of undefined").
    - Hit **Debug Code** and the AI will return the fixed version with inline comments explaining the changes.

3. **Save Java Code**:  
    - Once you've generated or debugged your code, hit **Save Code**, choose the location, and the file will be saved with the appropriate extension (`.java` for Java code).

## API Integration 🔌

The app communicates with an API to generate and debug code. Here’s a brief rundown of how the API works:

- **Model**: `unsloth/DeepSeek-R1-Distill-Llama-8B-GGUF`
- **Endpoint**: `POST /v1/chat/completions`
- **Request Body**: A list of messages containing the system prompt, user prompt (requirements or error details), and configuration parameters like `temperature` and `max_tokens`.
- **Retry Mechanism**: If the API call fails, the app will retry up to 3 times with incremental delays.

### Example API Request:
```json
{
  "model": "unsloth/DeepSeek-R1-Distill-Llama-8B-GGUF",
  "messages": [
    {"role": "system", "content": "You are a senior Python developer."},
    {"role": "user", "content": "Generate a Python function that reverses a string."}
  ],
  "temperature": 0.4,
  "max_tokens": 4096
}
```

## Customization ⚙️

You can modify the API configurations by updating the values in the `setup_config` method:

- **API_URL**: Your API endpoint URL.
- **API_KEY**: Authentication token for your API service.
- **MODEL_NAME**: The model to be used for code generation and debugging.
- **TEMPERATURE**: Controls the randomness of the output (0.0 for deterministic, 1.0 for more creative).
- **MAX_TOKENS**: Maximum tokens (words/characters) that the model can return.
- **MAX_RETRIES**: Number of retries in case of a failed request.
- **RETRY_DELAY**: Delay in seconds between retries.
- **TIMEOUT**: Timeout for the API request.

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

🚀 **Contribute**: Feel free to fork the repository, submit issues, or create pull requests to improve the app!
