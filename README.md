# Novel Insights 


# Description
“Novel Insights” is a book review application that allows users to rate/review and discover new books. Users can read reviews written by others to make informed decisions on what books they plan on reading in the future. By providing a platform for users to express their viewpoints, they can easily connect with other book lovers! 

# Details
Creators: Krisha Chokshi, Nemi Desai, Veena Kommu, Stanley Wei, Emily Sun

Class: COM SCI 35L (Spring 2023)

Professor: Paul Eggert

# Basic Requirements: 
Dynamic Data: Our application displays dynamic data to the users through a variety of ways. For example, the User Profile page (viewed when the user logs into their account), shows their previous reviews and ratings, and new profile pictures. Another example is an updated Book page anytime a new review is added (updating the book’s overall rating as well). 

Uploading Data from Client to Backend: Whenever a user submits a review, our application stores the Book, Author, Subject of Review, Content of Review, Rating, and an optional Image of the Book to the server’s file system. Whenever the user adds a profile picture, our application stores their image associated with their name.

Meaningful Search: The user can utilize the search tool to search for books that they would like to write reviews for, or see reviews for. 

# Additional Features
1. Users are able to favorite books to add to their Profile Page
2. Users may visit other user profiles that display their names, profile pictures, favorite books and reviews 
3. Follow other users 
4. View a list of the Top 10 highest rated books
5. Upvote, or downvote reviews that are left by others 
6. Filter search results alphabetically, highest rated, lowest rated
7. Filter book reviews by highest rated, lowest rated, most upvoted, most downvoted
8. Add missing books by ISBN10

# Installation Instructions
*Note: requires Python3.*
<ol>
  <li>Clone this repository to a local directory: <code>git clone https://github.com/stanley-wei/CS35L-Project.git</code>
  <li><code>cd</code> into the project directory</li>
  <li>Install the required packages: <code>python -m pip install -r requirements.txt</code>
    <ul>
      <li>Optional: Create a virtual environment before installing.</li>
    </ul>
  <li>Setup: 
    <ul>
      <li><code>python manage.py makemigrations</code></li>
      <li><code>python manage.py migrate</code></li>
    </ul>
</ol>
Run <code>python manage.py runserver</code> to start a development server on your local machine (default: <code>127.0.0.1:8000</code>).
