# Bible GPT

**Explore Scripture with the Power of AI**

Bible GPT is a modern web application that provides an interactive way to study the Bible using Google's Gemini 2.5 Flash AI. Ask questions, get detailed explanations of scripture, and engage in conversational exploration of biblical texts.

---

## ✨ Key Features

- **🤖 AI-Powered Chat:** Natural conversation with Gemini 2.5 Flash AI for biblical insights
- **💬 Chat History:** Save and load previous conversations with automatic persistence
- **🔖 Bookmarks:** Save important AI responses for later reference
- **📖 Verse Search:** Quick lookup of Bible verses with popular verse shortcuts
- **🎤 Voice Input:** Speak your questions using voice recognition (Chrome/Edge)
- **📥 Export Chat:** Download conversations as text files
- **🎨 Modern UI:** Clean, responsive interface with Tailwind CSS and Shadcn/ui
- **📱 Mobile Responsive:** Works seamlessly on all devices

---

## 🛠️ Tech Stack

### Frontend
- **Framework:** [Next.js 14](https://nextjs.org/) (React)
- **Language:** [TypeScript](https://www.typescriptlang.org/)
- **Styling:** [Tailwind CSS](https://tailwindcss.com/)
- **UI Components:** [Shadcn/ui](https://ui.shadcn.com/) & [Radix UI](https://www.radix-ui.com/)
- **AI Integration:** Google Gemini 2.5 Flash via REST API
- **Icons:** [Lucide React](https://lucide.dev/)

---

## 🚀 Getting Started

### Prerequisites
- [Node.js](https://nodejs.org/en) (v18 or later)
- Google AI Studio API Key ([Get one here](https://aistudio.google.com/app/apikey))

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Daveside9/MybibleAI.git
   cd MybibleAI
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Set up environment variables:**
   Create a `.env.local` file in the root directory:
   ```env
   # Google Gemini API Key
   GOOGLE_API_KEY="your-google-api-key-here"
   GEMINI_API_KEY="your-google-api-key-here"
   
   # NextAuth Configuration
   NEXTAUTH_SECRET="your-super-secret-key-here"
   NEXTAUTH_URL="http://localhost:3000"
   ```

4. **Run the development server:**
   ```bash
   npm run dev
   ```

5. **Open your browser:**
   Navigate to `http://localhost:3000`

---

## 📖 How to Use

1. **Start a Conversation:** Type your question in the input box or use voice input
2. **Search Verses:** Click the book icon to quickly search for specific Bible verses
3. **Bookmark Responses:** Click the bookmark icon on any AI response to save it
4. **View History:** Click the menu icon to see all your previous conversations
5. **Export Chat:** Click the download icon to save your conversation as a text file
6. **New Chat:** Click "New Chat" in the sidebar to start fresh

---

## 🎯 Features in Detail

### Chat History
- Automatically saves all conversations to browser localStorage
- View, load, and delete previous chats
- Conversations are sorted by most recent

### Voice Input
- Click the microphone icon to speak your question
- Works in Chrome and Edge browsers
- Automatically converts speech to text

### Verse Search
- Quick access to popular Bible verses
- Search any verse by reference (e.g., "John 3:16")
- Instantly sends the verse query to the AI

### Bookmarks
- Save important AI responses
- View all bookmarks in one place
- Copy bookmarked text to clipboard
- Delete bookmarks you no longer need

### Export
- Download entire conversations as text files
- Includes timestamps and sender information
- Perfect for sharing or archiving insights

---

## 🔧 Configuration

### API Key Setup
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env.local` file
4. Restart the development server

### Supported Models
The app uses `gemini-2.5-flash` which provides:
- Fast responses
- High-quality biblical knowledge
- Free tier available

---

## 📝 License

This project is open source and available under the MIT License.

---

## 🙏 Acknowledgments

- Powered by [Google Gemini 2.5 Flash](https://ai.google.dev/)
- UI components from [Shadcn/ui](https://ui.shadcn.com/)
- Built with [Next.js](https://nextjs.org/)

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

---

**Made with ❤️ for Bible study and research**
