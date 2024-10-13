# Cricbot Application

## Overview

Cricbot is a chatbot application designed to provide live cricket scores and handle various user intents. It leverages OpenAI's language models to understand user queries and generate appropriate responses. The application is structured to ensure modularity and ease of maintenance.

## Directory Structure

```
Cricbot/
├── app/
│   ├── src/
│   │    ├── constants/
│   │    │   ├── __init__.py
│   │    │   └── constants.py
│   │    ├── models/
│   │    │   ├── __init__.py
│   │    │   └── match_details.py
│   │    ├── prompts/
│   │    │   ├── all_live_matches_response_prompt.txt
│   │    │   ├── fallback_response_prompt.txt
│   │    │   ├── intent_identifier_system_message.txt
│   │    │   └── live_score_response_prompt.txt
│   │    ├── services/
│   │    │   ├── __init__.py
│   │    │   ├── intent_identifier_service.py
│   │    │   ├── intent_handler_service.py
│   │    │   ├── live_score_service.py
│   │    │   └── response_generator_service.py
│   │    ├── utils/
│   │    │   ├── __init__.py
│   │    │   └── common_util.py
│   │    ├── chains/
│   │    │   ├── __init__.py
│   │    │   └── cricbot_chain.py
│   │    ├── enums/
│   │    │   ├── __init__.py
│   │    │   └── intents.py
│   ├── main.py
│   └── cricbot_app.py
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
- **Chains**: Manages the sequence of operations using Langchain for generating responses.
- **Enums**: Defines enumerations used across the application.

## Recent Updates

- **Streamlit Integration**: The application now includes a Streamlit interface for a more interactive user experience.
- **Enhanced Error Handling**: Improved error handling mechanisms for better reliability.
- **Modular Codebase**: Refactored code to enhance readability and maintainability.
- **Langchain Integration**: Utilized Langchain to streamline the sequence of operations and improve response generation.
- **Streaming Enabled**: Added streaming capabilities for real-time interaction.
- **Deprecated Cricbot Service**: Replaced with a more modular approach using langchains

## Future Enhancements

- **Logging**: Add logging for better monitoring and debugging.
- **Testing**: Implement unit and integration tests to ensure reliability.
- **Advanced User Interface**: Develop a GUI for a more interactive user experience.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License.

---

This README provides a comprehensive overview of the Cricbot application, including setup instructions, usage, and future enhancements. Feel free to modify the content to better suit your project's needs.