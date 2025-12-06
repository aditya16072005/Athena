Athena: Global Numeral System Explorer (React Edition) 🏛️

A Computational Engine for Cross-Cultural Mathematics & Linguistics.

Athena is an interactive educational platform that bridges Linguistics and Mathematics. Instead of just converting numbers, it teaches the underlying logic of how different civilizations (Roman, Mayan, Babylonian) construct meaning.

This version of Athena is built as a Single-Page Application (SPA) using React. It features a Client-Side Meta-System, meaning all the mathematical logic and procedural generation happens instantly in the user's browser without needing a backend server.

🚀 Key Features

1. 📚 The Cultural Explorer

Browse a curated library of numeral systems. The app dynamically parses the internal schema to display:

Base (Radix): e.g., Base-10, Base-20, Base-60.

Logic Type: Additive (summing symbols) vs. Positional (place value).

Symbol Maps: Unique glyphs for every culture.

2. 🧮 Smart Transpiler Engine

Convert Arabic numbers (e.g., 88) into target systems (e.g., Mayan) in real-time.

Logic Trace: Displays the step-by-step mathematical breakdown (e.g., “Highest power of 20 fitting in 88 is...”).

Glyph Rendering: Supports complex rendering like Mayan dots/bars or Cuneiform wedges using React components.

3. 🧠 Olympiad Practice Zone

A procedural puzzle generator inspired by the International Linguistics Olympiad (IOL).

Infinite Content: The JavaScript engine reverse-engineers math problems on the fly.

Pattern Recognition: Users must decode sequences and patterns rather than rote memorization.

🛠️ Technical Architecture

Athena uses a Modern Frontend Stack to deliver a fast, responsive experience.

Framework: React.js (Hooks & Functional Components).

State Management: useState, useMemo for efficient recalculation of math logic.

Styling: Tailwind CSS (Utility-first styling).

Icons: Lucide-React.

Logic Engine: A pure JavaScript Transpiler object that creates a layer of abstraction between the UI and the math rules.

Directory Structure

athena-react/
├── src/
│   ├── App.jsx             # ⚛️ Main Application Logic (The code you have)
│   ├── main.jsx            #    Entry point
│   └── index.css           #    Tailwind imports
├── public/                 #    Static assets
└── package.json            #    Dependencies


⚡ Quick Start Guide

Since this is a React project, you need Node.js installed.

1. Setup the Project

Open your terminal and create a new Vite project:

npm create vite@latest athena -- --template react
cd athena
npm install


2. Install Dependencies

Install the required libraries for icons and styling:

npm install lucide-react clsx tailwind-merge
# Follow Tailwind CSS setup instructions if not already configured


3. Add the Code

Replace the contents of src/App.jsx with the Athena React Code.

4. Run the App

Start the development server:

npm run dev


Open your browser to the local link provided (usually http://localhost:5173).

🧩 How It Works (The "Meta-System")

Athena avoids hard-coded if/else chains for languages. Instead, it uses a JSON-based Schema inside the JavaScript code:

const SYSTEM_DB = {
  mayan: {
    base: 20,
    logic: 'positional',
    zero: 'Θ',
    digitRenderer: 'mayan'
  }
};


The Engine object reads this configuration. When you select "Mayan", the engine swaps its mathematical rules (e.g., from Base-10 to Base-20) instantly. This allows for adding new languages (like "Egyptian") by simply adding a new object to the database, making the code highly scalable and maintainable.

🛡️ Tech Stack

Frontend: React 18, Vite.

Styling: Tailwind CSS.

Logic: JavaScript (ES6+).

📄 License

This project is open-source and available for educational use.
