from telethon.sync import TelegramClient, events
from telethon.tl.types import PeerUser, PeerChat, PeerChannel

async def delete_all_chats(api_id, api_hash, phone_number):
    client = TelegramClient('session_name', api_id, api_hash)

    try:
        await client.start(phone_number)

        # Check if 2FA is enabled
        if not client.is_user_authorized():
            # If 2FA is enabled, ask the user to enter the one-time password
            user_phone = await client.sign_in(phone_number)
            print(f"Please enter the one-time password sent to {user_phone.phone}:")

            # Wait for the user to input the OTP
            otp_code = input()
            await client.sign_in(code=otp_code)

        # Get all dialogs
        dialogs = await client.get_dialogs()

        # Prompt user for confirmation before deletion
        confirm = input("Are you sure you want to delete all chats? (yes/no): ").lower()
        if confirm != 'yes':
            print("Aborted. No chats were deleted.")
            return

        # Delete individual dialogs based on type
        for dialog in dialogs:
            entity = dialog.entity
            if isinstance(entity, (PeerUser, PeerChat, PeerChannel)):
                await client.delete_dialog(dialog)

        print("All chats deleted successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        await client.disconnect()

if __name__ == '__main__':
    # Take user input for API ID, API hash, and phone number
    api_id = input("Enter your API ID: ")
    api_hash = input("Enter your API hash: ")
    phone_number = input("Enter your phone number (in international format, e.g., +1234567890): ")

    # Run the script with user inputs
    TelegramClient.loop.run_until_complete(delete_all_chats(api_id, api_hash, phone_number))
