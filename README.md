# Flash Card Project

## Author
Yash Mishra

## Description
This project is a basic flash card application with user authentication. Flash cards are organized into decks, and each deck belongs to a specific category. Users can choose a deck (topic) of their choice and retrieve cards in random order. The answers are provided on the back of the flipping cards.

## Technologies Used
- Python and the following modules:
  - click==8.0.3
  - colorama==0.4.4
  - Flask==2.0.2
  - itsdangerous==2.0.1
  - Jinja2==3.0.3
  - MarkupSafe==2.0.1
  - psycopg2==2.9.2
  - Werkzeug==2.0.2
- SQLite for the database
- HTML for layout
- CSS for decoration

## Database Schema Design
The project uses two main tables:

### Cards Table
The `cards` table stores the content for decks and flashcards. It includes fields such as:
- `id`: Unique identifier for each card
- `deck_id`: Foreign key linking the card to a specific deck
- `question`: The question or prompt on the flash card
- `answer`: The answer to the flash card

### Users Table
The `users` table is responsible for authenticating users. It includes fields like:
- `id`: Unique identifier for each user
- `username`: User's chosen username
- `password`: Encrypted password for user authentication

## Video
A demonstration of the project can be found in the following [video](https://drive.google.com/file/d/1x1PGPnivnuhVmCX8uZPO-ISib0nlbUHt/view?usp=sharing).

Feel free to explore the flash card application and enhance your learning experience! If you have any questions or feedback, please contact the author at the provided email address.
