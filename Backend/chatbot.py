
import os
import glob
import sys

# 🛠️ Fix: Set stdout to UTF-8 to avoid UnicodeEncodeError with emojis
sys.stdout.reconfigure(encoding='utf-8')

from typing import Dict
from gemini_client import ask_gemini


class UPLawChatbot:
    def __init__(self):
        self.legal_texts: Dict[str, str] = {}
        self.data_folder = 'data'
        self.load_all_legal_texts()
    
    def load_all_legal_texts(self) -> None:
        try:
            txt_files = glob.glob(os.path.join(self.data_folder, '*.txt'))#global 
            
            if not txt_files:
                print(f"⚠️  No .txt files found in {self.data_folder}/ folder!")
                print("Please add some legal text files to get started.")
                return
            
            print(f"📚 Loading {len(txt_files)} legal document(s)...")
            
            for file_path in txt_files:
                try:
                    filename = os.path.basename(file_path)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                        if content:
                            self.legal_texts[filename] = content
                            print(f"✅ Loaded: {filename}")
                        else:
                            print(f"⚠️  Empty file: {filename}")
                except Exception as e:
                    print(f"❌ Error loading {os.path.basename(file_path)}: {e}")
            
            print(f"📖 Total legal documents loaded: {len(self.legal_texts)}")
        
        except Exception as e:
            print(f"❌ Error accessing data folder: {e}")
    
    def get_combined_legal_text(self) -> str:
        if not self.legal_texts:
            return "No legal documents available."
        
        combined_text = "LEGAL DOCUMENTS REFERENCE:\n\n"
        for filename, content in self.legal_texts.items():
            combined_text += f"=== {filename.upper()} ===\n{content}\n\n"
        return combined_text.strip()
    
    def build_prompt(self, user_question: str) -> str:
        legal_text = self.get_combined_legal_text()

        prompt = f"""You are a legal assistant specialized in Uttar Pradesh laws. Below are the legal documents you can refer to:

{legal_text}

USER QUESTION: {user_question}
1. Use only the legal texts provided to answer and explain properly.
2. If not covered, say: "This specific legal matter is not covered in the available documents. Please consult a qualified lawyer."
3. Structure your answer with sections:
   - **LAW:** Explain the relevant law simply.
   - **LEGAL PROVISION:** Cite the relevant section.
   - **YOUR SITUATION:** Analyze user's question.
   - **WHAT YOU CAN DO:** Step-by-step practical advice.
   - **PROCESS TO FOLLOW:** Clear instructions for actions.
   - **IMPORTANT NOTES:** Key warnings or alerts.
4. Use plain language, be practical and clear.
5. If unsure, recommend consulting a lawyer.
6. End with: "If you have further questions, feel free to ask!"
7. Keep tone friendly, professional, and clear.

RESPONSE:"""
        
        return prompt
    
    def display_help(self) -> None:#for help function
        print("This bot can assist with various legal questions related to Uttar Pradesh laws.")
        print("You can ask about specific legal provisions, legal procedures, documents required, and more.")
        print("For a list of topics on which bot can help, type 'topic'.")

    def show_command_list(self) -> None:#for showing command list
        help_text = """
🤖 UP LAW CHATBOT - COMMAND LIST

Available Commands:
• Type your legal question and press Enter
• '--help' - Show available commands
• 'help' - Show what this bot can assist you with
• 'files' - List loaded legal documents
• 'topic' - Show available legal topics
• 'exit' or 'quit' - Exit the chatbot

Tips:
• Ask specific questions for better answers
• The bot only answers based on loaded legal documents
• For complex legal matters, always consult a qualified lawyer
"""
        print(help_text)
    
    def list_files(self) -> None:
        if not self.legal_texts:
            print("❌ No legal documents loaded.")
            return
        
        print("\n📚 LOADED LEGAL DOCUMENTS:")
        print("=" * 40)
        for i, filename in enumerate(self.legal_texts.keys(), 1):
            print(f"{i}. {filename}")
        print("=" * 40)
    
    def run(self) -> None:
        if not self.legal_texts:
            print("❌ No legal documents available. Please add .txt files to the data/ folder.")
            return
        
        print("\n" + "="*50)
        print("🤖 UP LAW CHATBOT")
        print("="*50)
        print("Type 'help' or '--help' for assistance, 'exit' to quit")
        print("="*50 + "\n")
        
        while True:
            try:
                user_input = input("💬 You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['exit', 'quit']:
                    print("👋 Thank you for using UP Law Chatbot. Goodbye!")
                    break
                elif user_input.lower() == 'help':
                    self.display_help()#for help
                    continue
                elif user_input.lower() == '--help':
                    self.show_command_list()#for showing command list
                    continue
                elif user_input.lower() == 'files':
                    self.list_files()#for listing files
                    continue
                elif user_input.lower() == 'topic':#for showing topics
                    print("📚 The bot can assist you with the following topics:")
                    print("1. Labour Laws")
                    print("2. Property Laws")
                    print("3. Family Laws")
                    print("4. Criminal Laws")
                    print("5. Civil Laws")
                    continue
                
                print("🤔 Processing your question...")
                prompt = self.build_prompt(user_input)
                response = ask_gemini(prompt)
                print(f"\n📋 Bot: {response}\n")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                print("INVALID COMMAND. Type 'help' for assistance.")


def main():
    try:
        chatbot = UPLawChatbot()
        chatbot.run()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        print("Please check your setup and try again.")


if __name__ == "__main__":
    main()
