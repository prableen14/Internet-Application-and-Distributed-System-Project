# Crypto Trade App

Welcome to the Crypto Trade App, a Django-based web application for cryptocurrency trading and community engagement.

## Features

### User Authentication

- **Login/Logout**: Users can log in and out of the platform.
- **Registration**: New users can register, and during registration, they are required to upload a valid ID.

### Homepage

- The homepage dynamically changes based on whether the user is logged in or not.

### Navigation

- A navigation bar provides easy access to all pages.

### Coin Search

- Users can search for a specific coin, and upon finding it, they are directed to the coin details page.

### Currency Exchange

- A simple currency exchange feature is implemented.

### Highlights Component

- Display current trends, charts, patterns, rates, etc., similar to the "Highlights" button on [CoinMarketCap](https://coinmarketcap.com/).

### Buy/Sell Coins

- Users can buy and sell coins, with a link to the payment screen.
- The system considers the user's available funds before allowing a purchase.

### Buy/Sell History

- A separate UI displays the user's buy and sell history.

### Coin Market Information

- List all coins in the market along with their overall information in a table.

### Coin Details Page

- A dedicated screen to display detailed information about a specific coin.

### Network Page

- Users can post and track their posts, like posts, and leave comments.
- A feed displays other users' posts, allowing likes and comments.

### Community Page

- Users can write articles related to cryptocurrency.
- A page displays all the articles, and users can click on an article to read it in full.

## Installation

1. **Clone the repository:**

   ```bash
   git clone git@github.com:prableen14/Internet-Application-and-Distributed-System-Project.git
   cd Internet-Application-and-Distributed-System-Project
2. **Add Python interpreter**

    In PyCharm, open File -> Settings... -> Project: Internet-Application -> Python Interpreter

    Add a new interpreter if there isn't one
3. **Apply migrations:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
4. **Run the development server:**
    ```bask
    python manage.py runserver
5. **Open your browser and navigate to http://localhost:8000 to access the Crypto Trade App.**