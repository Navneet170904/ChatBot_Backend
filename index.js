// import express from "express";
// import cors from "cors";
// import { GoogleGenerativeAI } from "@google/generative-ai";

// import fetch from "node-fetch";

// if (!globalThis.fetch) {
//   globalThis.fetch = fetch;
// }

// const GOOGLE_API_KEY = "AIzaSyCiWVvjpAy6huRyUK5TzSAcQiUepvePcN4";
// const genAI = new GoogleGenerativeAI(GOOGLE_API_KEY);
// const app = express();

// app.use(cors({ origin: "http://localhost:3001" }));
// app.use(express.urlencoded({ extended: true }));
// app.use(express.json());

// app.get("/", (req, res) => {
//   res.send("Hello World!");
// });

// app.post("/api/data", async (req, res) => {
//   let query = req.body.text;

//   const model = genAI.getGenerativeModel({ model: "gemini-pro" });

//   const chat = model.startChat({
//     history: [],
//   });

//   const result = await chat.sendMessage(query);
//   const response = await result.response;
//   const text = response.text();
//   console.log(text);
//   console.log(chat._history)
// });

// app.listen(5000, () => {
//   console.log(`Server is running on port : http://localhost:5000`);
// });



import express from "express";
import cors from "cors";
import { GoogleGenerativeAI } from "@google/generative-ai";
import fetch from "node-fetch";
import mysql from "mysql2/promise"; // Use mysql2 for promise-based queries
import dotenv from "dotenv";

dotenv.config(); // Load .env variables

if (!globalThis.fetch) {
  globalThis.fetch = fetch;
}

// Use environment variables for credentials
const GOOGLE_API_KEY = process.env.GOOGLE_API_KEY;
const DB_CONFIG = {
  host: process.env.DB_HOST, // MySQL host
  user: process.env.DB_USER, // MySQL username
  password: process.env.DB_PASSWORD, // MySQL password
  database: process.env.DB_DATABASE, // MySQL database name
};

// Create MySQL connection pool
const pool = mysql.createPool(DB_CONFIG);

const genAI = new GoogleGenerativeAI(GOOGLE_API_KEY);
const app = express();

app.use(cors(
  // origin: "https://chat-bot-frontend-dun.vercel.app/" 
));
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

app.get("/", (req, res) => {
  res.send("Hello World!");
});

// Check MySQL connection at server start
const checkDBConnection = async () => {
  try {
    const [rows] = await pool.execute("SELECT 1");
    console.log("MySQL connection successful!");
  } catch (error) {
    console.error("MySQL connection error:", error.message);
  }
};

// Call the checkDBConnection when the server starts
checkDBConnection();

app.post("/api/data", async (req, res) => {
  try {
    const query = req.body.text;

    // Use Google Generative AI to process the query
    const model = genAI.getGenerativeModel({ model: "gemini-pro" });
    const chat = model.startChat({
      history: [],
    });

    const result = await chat.sendMessage(query);
    const responseText = result.response.text();

    console.log("Generated AI response:", responseText);

    // Insert the query and AI response into the database
    await pool.execute(
      "INSERT INTO messages (message_text, ai_response) VALUES (?, ?)",
      [query, responseText]
    );

    // Fetch data from MySQL based on the query
    const [rows] = await pool.execute("SELECT * FROM messages WHERE message_text LIKE ?", [`%${query}%`]);

    // Combine AI response and database data
    res.json({
      aiResponse: responseText,
      dbData: rows,
    });
  } catch (error) {
    console.error("Error:", error.message);
    res.status(500).json({
      error: "An error occurred while processing the query.",
      details: error.message,
    });
  }
});

// Start the server
app.listen(5000, () => {
  console.log("Server is running on http://localhost:5000");
});
