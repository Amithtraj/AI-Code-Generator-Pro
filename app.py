import time
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
import json
import os
from pathlib import Path
from typing import Optional, Dict

class CodeGeneratorApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("AI Code Generator Pro")
        self.session = requests.Session()
        self.setup_config()
        self.create_widgets()
        self.setup_retry_adapter()
        
    def setup_config(self):
        self.config = {
            "API_URL": "http://localhost:1234/v1/chat/completions",
            "API_KEY": "lm-studio",
            "MODEL_NAME": "unsloth/DeepSeek-R1-Distill-Llama-8B-GGUF",
            "TEMPERATURE": 0.4,
            "MAX_TOKENS": 4096,
            "MAX_RETRIES": 3,
            "RETRY_DELAY": 1.5,
            "TIMEOUT": 30
        }
        
    def setup_retry_adapter(self):
        adapter = requests.adapters.HTTPAdapter(
            max_retries=self.config["MAX_RETRIES"]
        )
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        
    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Input Section
        input_frame = ttk.LabelFrame(main_frame, text="Code Generation Parameters", padding=10)
        input_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        ttk.Label(input_frame, text="Requirements:").grid(row=0, column=0, sticky="w")
        self.input_text = tk.Text(input_frame, height=12, width=80, wrap=tk.WORD)
        self.input_text.grid(row=1, column=0, columnspan=2, pady=5)
        
        ttk.Label(input_frame, text="Language:").grid(row=2, column=0, sticky="w")
        self.language_var = tk.StringVar(value="Python")
        self.lang_combo = ttk.Combobox(input_frame, textvariable=self.language_var,
                                     values=["Python", "JavaScript", "Java", "C++", "TypeScript", "html"])
        self.lang_combo.grid(row=2, column=1, sticky="ew")
        
        # Output Section
        output_frame = ttk.LabelFrame(main_frame, text="Generated Code", padding=10)
        output_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        self.output_text = tk.Text(output_frame, height=20, width=80, wrap=tk.NONE)
        self.output_text.pack(pady=5)
        
        # Control Panel
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=2, column=0, sticky="ew", pady=10)
        
        ttk.Button(control_frame, text="Generate Code", command=self.generate_code).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Debug Code", command=self.debug_code).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Save Code", command=self.save_code).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Settings", command=self.show_settings).pack(side=tk.RIGHT, padx=5)
        
        # Status Bar
        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
    def update_status(self, message: str, error: bool = False):
        self.status_bar.config(
            text=message,
            foreground="red" if error else "black"
        )
        self.root.update_idletasks()
        
    def generate_code(self):
        requirements = self.input_text.get("1.0", tk.END).strip()
        if not requirements:
            messagebox.showerror("Input Error", "Please enter code requirements")
            return
            
        self.update_status("Generating code...")
        
        prompt = self.create_code_prompt(requirements)
        messages = [
            {"role": "system", "content": self.get_system_prompt()},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = self.api_call_with_retry(messages)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, response)
            self.update_status("Code generated successfully")
        except Exception as e:
            self.update_status(f"Generation failed: {str(e)}", error=True)
            messagebox.showerror("API Error", f"Failed to generate code:\n{str(e)}")
            
    def debug_code(self):
        code = self.output_text.get("1.0", tk.END).strip()
        error = self.get_error_from_user()
        
        if not error:
            return
            
        prompt = self.create_debug_prompt(code, error)
        messages = [
            {"role": "system", "content": "Senior Software Debugger"},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = self.api_call_with_retry(messages)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, response)
            self.update_status("Code debugged successfully")
        except Exception as e:
            self.update_status(f"Debugging failed: {str(e)}", error=True)
            messagebox.showerror("API Error", f"Debugging failed:\n{str(e)}")
            
    def save_code(self):
        code = self.output_text.get("1.0", tk.END).strip()
        if not code:
            messagebox.showwarning("Save Warning", "No code to save")
            return
            
        default_ext = self.get_file_extension()
        file_path = filedialog.asksaveasfilename(
            defaultextension=default_ext,
            filetypes=[(f"{self.language_var.get()} Files", f"*{default_ext}"), ("All Files", "*.*")]
        )
        
        if not file_path:
            return
            
        try:
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w') as f:
                f.write(code)
            self.update_status(f"Code saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save file:\n{str(e)}")
            self.update_status("Save failed", error=True)
            
    def api_call_with_retry(self, messages: list) -> str:
        for attempt in range(self.config["MAX_RETRIES"]):
            try:
                response = self.session.post(
                    self.config["API_URL"],
                    json={
                        "model": self.config["MODEL_NAME"],
                        "messages": messages,
                        "temperature": self.config["TEMPERATURE"],
                        "max_tokens": self.config["MAX_TOKENS"]
                    },
                    headers={"Authorization": f"Bearer {self.config['API_KEY']}"},
                    timeout=self.config["TIMEOUT"]
                )
                response.raise_for_status()
                return response.json()['choices'][0]['message']['content']
            except Exception as e:
                if attempt < self.config["MAX_RETRIES"] - 1:
                    self.update_status(f"Retrying ({attempt+1}/{self.config['MAX_RETRIES']})...")
                    time.sleep(self.config["RETRY_DELAY"] * (attempt + 1))
                else:
                    raise RuntimeError(f"API request failed after {self.config['MAX_RETRIES']} attempts") from e
                    
    def create_code_prompt(self, requirements: str) -> str:
        return f"""Generate production-quality {self.language_var.get()} code meeting these requirements:

Requirements:
{requirements}

Instructions:
1. Implement complete functionality
2. Follow best practices
3. Include error handling
4. Add documentation
5. Use modern language features
6. Validate inputs
7. Optimize performance

Provide ONLY the code with no explanations or markdown formatting."""
    
    def create_debug_prompt(self, code: str, error: str) -> str:
        return f"""Debug this code:

{code}

Error:
{error}

Instructions:
1. Identify root cause
2. Fix while preserving functionality
3. Add error prevention
4. Maintain style consistency
5. Add fix comments

Provide ONLY the fixed code with brief inline comments explaining fixes."""
    
    def get_system_prompt(self) -> str:
        return f"""You are a senior {self.language_var.get()} developer. 
Create clean, efficient, production-ready code following best practices.
Include proper error handling, documentation, and validation."""
        
    def get_file_extension(self) -> str:
        return {
            "Python": ".py",
            "JavaScript": ".js",
            "Java": ".java",
            "C++": ".cpp",
            "TypeScript": ".ts",
            "html": ".html"
        }.get(self.language_var.get(), ".txt")
        
    def get_error_from_user(self) -> Optional[str]:
        dialog = tk.Toplevel(self.root)
        dialog.title("Enter Error Information")
        
        ttk.Label(dialog, text="Paste error message:").pack(pady=5)
        error_text = tk.Text(dialog, height=10, width=60)
        error_text.pack(pady=5)
        
        result = []
        
        def on_submit():
            result.append(error_text.get("1.0", tk.END).strip())
            dialog.destroy()
            
        ttk.Button(dialog, text="Submit", command=on_submit).pack(pady=5)
        self.root.wait_window(dialog)
        return result[0] if result else None
        
    def show_settings(self):
        # Implement settings dialog for API configuration
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = CodeGeneratorApp(root)
    root.mainloop()