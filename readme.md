# ChatCrypt Telegram Bot

This Python script sets up a Telegram bot that enables encryption and decryption of messages and files. The bot allows users to generate a private key, set the key, and then use it to encrypt or decrypt messages and various file types.

## Prerequisites

- Python 3.9 and Above
- Required Python libraries: `os`, `telebot`, `base64`, `cryptography`

## Getting Started

1. Clone the repository or download the script to your local machine.

2. Install the required Python libraries using pip:

   ```shell
   pip install telebot cryptography

3. Set up a Telegram bot and obtain the API key. Follow the official Telegram Bot documentation to create a new bot and get the API key.

4. Set the API key as an environment variable named API_KEY. You can set it directly in your system's environment variables or create a .env file in the project directory with the following content:
    ```shell
   API_KEY=<your_api_key_here>

5. Run the script:
    ```shell
    python main.py

6. Start interacting with the bot on Telegram.

## Usage

- Start the bot by sending the `/start` command.
- Generate a private key using the `/generate` command. The bot will generate a new key and send it to you.
- Set the private key using the `/set` command followed by the key value. For example: `/set my_private_key`.
- Activate encryption mode using the `/encode` command.
- Activate decryption mode using the `/decode` command.
- Send text messages to the bot to encrypt or decrypt them based on the current mode.
- Send voice, audio, photo, or document files to the bot for encryption or decryption.

## Contributing

Contributions are welcome! If you find any issues or want to add new features, please submit a pull request.

## Disclaimer

This code is provided as-is without any warranty. Use it at your own risk.

## Credits

The code is inspired by the Telegram Bot API and utilizes the telebot library for interacting with the Telegram API and the cryptography library for encryption and decryption operations.

## Contact

For any questions or inquiries, please contact [Me](subhamsingha2004@gmail.com).
