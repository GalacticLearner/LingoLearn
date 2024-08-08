# LingoLearn
##### Video Demo: 


## Introduction
LingoLearn is a web app built on flask focused on helping users develop their English vocabulary. Users can look up the
definitions of words and phrases, improve daily by learning from *Word of the Day* and *Phrase of the Day*, and bookmark 
words for later revision. Users can also practise from a large pool of words through quizzes, and train from the
contents of a recently finished book. Users can track their progress using Blingos- a token awarded for answering
correctly in quizzes.
The site is built on the Flask micro-framework, using MySQL for handling user data, and HTML, CSS and JavaScript for
the frontend of the site.


## Features

### User Profiles
Users can access *Definition Look-Up*, *Word of the Day*, and *Phrase of the Day* without registration. Creating a profile provides access to quizzes, bookmarks and progress tracking.

### Definition Look-Up
Users can search for any word or phrase in the homepage of the site. Definitions are provided, along with synonyms and antonyms if available.

### Word of the Day and Phrase of the Day
A new word and phrase are updated on the homepage of the website daily, which would enable users to improve their vocabulary regularly.

### Practice
Users are served random multiple choice questions, where they have to select the option that best matches the given definition. Ten blingos can be earned for a right answer, while a wrong answer deducts five blingos. A 50/50 lifeline gives users the option of eliminating two wrong options for 5 blingos. Quizzes can be a great way for users to test their skills and track their progress.

### Bookmarks
Definition Look-Ups come with an option to bookmark words and phrases for later review. These are stored in the bookmarks page, where a brief definition is provided along with the bookmarked word.

### Book Tutor
Users can test themselves from the contents of certain publicly available books. Selecting a book redirects to the practice page, where quizzes are served from the words found in the book. Previously searched books are stored in the bookshelf, for easy access.


## Technologies Used

### Flask
The web app is built on the Flask micro framework. Jinja is used to display various user data and dictionary data. All pages extend a common layout, reducing redundancy in implementing a navigation bar.

### MySQL
User data such as usernames, passwords and user IDs are stored using a MySQL database. Along with that, features such as bookmarks, bookshelf, and blingos are also enabled by MySQL.

### HTML, CSS
The front end of the web app is implemented through HTML and CSS. All styling is from CSS classes and inline styles.

### JavaScript
Javascript functions are used for handling logic in quizzes. These functions change styles and display messages, letting the user know the result of the quiz. The user databases is updated after quizzes using AJAX (Asynchronous JavaScript and XML) functions to make XML HTTP requests.

### Libraries, APIs

#### Dictionary API
Dictionary data such as word/phrase definitions, synonyms and antonyms are obtained through [Dictionary API](dictionaryapi.dev).

#### Twinword API
More data regarding words such as word-difficulty are provided by the [Twinword API](https://rapidapi.com/twinword/api/word-dictionary).

#### GutenbergPy
The [GutenbergPy](https://pypi.org/project/gutenbergpy/) package is used to obtain publicly available books from [Project Gutenberg](https://www.gutenberg.org/) for *Book Tutor*.

#### Google Images Search
The [Google Images Search](https://pypi.org/project/Google-Images-Search/) package is used to retrieve book covers for the bookshelf. The package uses a custom Google search engine.

#### APSscheduler
The [Advanced Python Scheduler](https://pypi.org/project/APScheduler/) package is used to schedule the *Word of the Day* and *Phrase of the Day* features to update daily.

#### Werkzeug
The [Werkzeug](https://pypi.org/project/Werkzeug/) package is used for encrypting and verifying user passwords.


## Distinctiveness
LingoLearn is the first website which enables users to directly train from the contents of a wide variety of books, and to store these books for later review.

## Future Scope
Difficulty Level of words and exams which have asked about a given word are data that could be provided to users in the future for better flexibility in learning.