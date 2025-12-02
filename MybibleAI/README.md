
# Bible GPT

**Explore Scripture with the Power of AI**

Bible GPT is a full-stack web application designed to provide users with an interactive and insightful way to study the Bible. By leveraging a powerful generative AI, users can ask questions, get detailed explanations of scripture, and engage in a conversational exploration of biblical texts.

---

## ✨ Key Features

-   **AI-Powered Chat:** Engage in a natural conversation with an AI to get answers and insights on biblical topics.
-   **Secure User Authentication:** A complete sign-up and login system to provide a personalized user experience.
-   **Modern, Responsive UI:** A clean and intuitive interface built with Next.js and Tailwind CSS, ensuring a great experience on any device.
-   **Light & Dark Modes:** Seamlessly switch between themes for comfortable reading in any lighting condition.
-   **Admin Capabilities:** Includes backend infrastructure for application management.

---

## 🛠️ Tech Stack

The project is built with a modern, separated frontend and backend architecture.

### Frontend (`bible-gpt-frontend`)

-   **Framework:** [Next.js](https://nextjs.org/) (React)
-   **Language:** [TypeScript](https://www.typescriptlang.org/)
-   **Styling:** [Tailwind CSS](https://tailwindcss.com/)
-   **UI Components:** [Shadcn/ui](https://ui.shadcn.com/) & [Radix UI](https://www.radix-ui.com/)
-   **Authentication:** [NextAuth.js](https://next-auth.js.org/)
-   **AI Integration:** [Vercel AI SDK](https://sdk.vercel.ai/) for handling chat interactions.
-   **Form Management:** [React Hook Form](https://react-hook-form.com/) with [Zod](https://zod.dev/) for validation.

### Backend (`bibleAI_project`)

-   **Framework:** [Django](https://www.djangoproject.com/)
-   **Language:** [Python](https://www.python.org/)
-   **Database:** [SQLite](https://www.sqlite.org/index.html) (as configured by default in Django)
-   **API:** Built using Django REST Framework to serve the frontend.

---

## 🚀 Getting Started

Follow these instructions to set up and run the project on your local machine for development.

### Prerequisites

-   [Node.js](https://nodejs.org/en) (v18 or later)
-   [Python](https://www.python.org/downloads/) (v3.8 or later) and `pip`

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/bible-ai.git
    cd bible-ai
    ```

2.  **Set up the Backend (`bibleAI_project`):**
    -   Navigate to the backend directory:
        ```bash
        cd bibleAI_project
        ```
    -   Create a virtual environment and activate it:
        ```bash
        # For Windows
        python -m venv venv
        .\venv\Scripts\activate
        ```
        ```bash
        # For macOS/Linux
        python3 -m venv venv
        source venv/bin/activate
        ```
    -   Install the required Python packages (assuming a `requirements.txt` file exists):
        ```bash
        pip install -r requirements.txt
        ```
    -   Apply database migrations:
        ```bash
        python manage.py migrate
        ```

3.  **Set up the Frontend (`bible-gpt-frontend`):**
    -   From the root directory, navigate to the frontend folder:
        ```bash
        cd ../bible-gpt-frontend
        ```
    -   Install the required npm packages:
        ```bash
        npm install
        ```

4.  **Environment Variables:**
    -   In the `bible-gpt-frontend` directory, create a file named `.env.local`. Add the following environment variables required for authentication and the AI service.
        ```env
        # .env.local

        # A secret key for NextAuth.js to encrypt sessions.
        # You can generate one here: https://generate-secret.vercel.app/32
        NEXTAUTH_SECRET="your-super-secret-key-here"
        NEXTAUTH_URL="http://localhost:3000"

        # Your Google Generative AI API Key for the chat functionality
        GOOGLE_API_KEY="your-google-api-key-here"
        ```

---

## 🏃‍♂️ Running the Application

To run the application, you must start both the backend and frontend servers in separate terminal windows.

1.  **Start the Backend (Django) Server:**
    -   Open a terminal, navigate to the `bibleAI_project` directory, and ensure your virtual environment is activated.
    -   Run the Django development server:
        ```bash
        python manage.py runserver
        ```
    -   The backend API will be running at `http://127.0.0.1:8000`.

2.  **Start the Frontend (Next.js) Server:**
    -   Open a second terminal and navigate to the `bible-gpt-frontend` directory.
    -   Run the Next.js development server:
        ```bash
        npm run dev
        ```
    -   Open your browser and go to `http://localhost:3000` to use the application.

---

## 📂 Project Structure

The repository is organized into two main parts:
