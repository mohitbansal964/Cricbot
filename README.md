# Cricbot Application

## Overview

Cricbot is a chatbot application designed to provide live cricket scores and handle various user intents. It leverages OpenAI's language models to understand user queries and generate appropriate responses.

## Directory Structure

```
CRICBOT/
│
├── app/
│   ├── constants/
│   │   ├── __init__.py
│   │   └── constants.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── match_details.py
│   ├── prompts/
│   │   ├── fallback_response_prompt.txt
│   │   ├── intent_identifier_system_message.txt
│   │   └── live_score_response_prompt.txt
│   ├── services/
│   │   ├── __init__.py
│   │   ├── cricbot_service.py
│   │   ├── intent_identifier_service.py
│   │   ├── live_score_service.py
│   │   └── response_generator_service.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── common_util.py
│   ├── main.py
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

## Setup

### Prerequisites

- Python 3.x
- pip (Python package installer)

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/mohitbansal964/Cricbot.git
   cd Cricbot
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**

   Create a `.env` file in the root directory and add your OpenAI API key:

   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

Run the application using the following command:

```bash
python app/main.py
```

Interact with the bot by typing your queries. Type "exit" to terminate the session.

## Components

- **Constants**: Stores constant values used across the application.
- **Models**: Contains data models like `MatchDetails`.
- **Prompts**: Stores prompt templates for generating responses.
- **Services**: Contains the core logic for intent identification, live score fetching, and response generation.
- **Utils**: Provides utility functions for common tasks.

## Future Enhancements

- **Error Handling**: Improve error handling for network issues and invalid inputs.
- **Logging**: Add logging for better monitoring and debugging.
- **Testing**: Implement unit and integration tests to ensure reliability.
- **User Interface**: Develop a GUI for a more interactive user experience.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License.

---

This README provides a comprehensive overview of the Cricbot application, including setup instructions, usage, and future enhancements. Feel free to modify the content to better suit your project's needs.