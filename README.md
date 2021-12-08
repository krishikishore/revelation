# Revelation

## About Revelation

Revelation Journal is a scientific research journal designed to be utilized by high school and undergraduate students. We understand the difficulty for young researchers to getting their phenomenal research out into the world competing with the best scientists in the world who have an advantage across both experience and resources. We believe it is an important aspect of any young researcher's career to be able to publish one's work and allow researchers from all over the globe to access, learn from, and perhaps even cite the work in the context of their own research. Some of the main features of Revelation include the ability to publish one's own work, get feedback through a peer-review editing process, explore other young researchers' work, and get involved in the youth scientific community.

Video - [https://youtu.be/rnn-xHovv84](https://youtu.be/rnn-xHovv84)

### Built With
- [HTML](https://developer.mozilla.org/en-US/docs/Web/HTML)
- [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS)
- [Bootstrap](https://getbootstrap.com/)
- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
- [Jinja](https://jinja.palletsprojects.com/en/3.0.x/)
- [SQLite](https://www.sqlite.org/index.html)

## Getting Started

### Prerequisites (in order)

- Visual Studio Code
[Download Visual Studio Code](https://code.visualstudio.com/download)
- homebrew

Open the terminal within Visual Studio Code and enter this command:
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
You will see messages in the terminal for further installation steps which will likely include entering 2 commands.
- python

Open the terminal within Visual Studio Code and enter this command:
```
brew install python
```
- cs50

Open the terminal within Visual Studio Code and enter this command:
```
pip3 install cs50
```
- lib50

Open the terminal within Visual Studio Code and enter this command:
```
pip3 install lib50
```
- flask

Open the terminal within Visual Studio Code and enter this command:
```
pip3 install flask
```
Sometimes this command may fail due to permission errors in which case do
```
pip3 install flask --user
```
- flask_session

Open the terminal within Visual Studio Code and enter this command:
```
pip3 install flask_session
```
- rake-nltk

Open the terminal within Visual Studio Code and enter this command:
```
pip3 install rake-nltk
```
### Installation

1. Clone the repo in your intended folder locally by entering the following command in your terminal within Visual Studio Code:
```
git clone https://github.com/krishikishore/revelation.git
```
2. Navigate to the cloned repository by entering this command in your Visual Studio Code terminal:
```
cd revelation
```
3. Run the following command to start the Flask web server and follow the instructions to access the link to the website:
```
python3 -m flask run
```
## Usage

Welcome... to Revelation!

Upon accessing Revelation, the user is first brought to a simple, crisp, and, frankly, beautiful homepage. The simple website logo is displayed
in the top left, and clicking upon this will return the user to the homepage. The most eye-catching feature is the large orange banner, though,
within which the Revelation slogan can be found: "A scientific journal built for young researchers by young researchers". Beneath
this, articles which have been published are chosen randomly from the database and displayed in various ways, along with their title and field. 
Each article is also randomly assigned a color for aesthetic purposes. On the right side of the main body, there is a "Community" list that
shows people randomly selected from the database by their name, role, and school. Back at the top of the page, one finds a navigation bar for
the website and, in the top right, a search bar and login button. Let's now walk through each feature and its page.

The explore page displays the five different research fields and lists articles within each. The publish page will prompt the user to log-in,
(or sign-up, if necessary), but we will get back to that later. The community page displays randomly selected people from the users table, 
with all of their information. The about page gives a brief overview of Revelation's mission, usage, and publishing process. The contact page
allows users to input their email and submit a message to the journal. At the far right of the navigation bar resides the subcribe button, which
lets users subscribe to Revelation with their email. Above this, one will find a search bar with which they can look for articles based on specific
keywords. Upon entering the search term, this will bring them to the search page, displaying their results and allowing them to browse those articles
or search something else. 

Now that all the features accessible to non-logged-in users have been covered, let's move on to the log-in. After clicking log-in, the user will find
an option to sign up and create an account. After filling in the necessary information and choosing to be a "researcher" , they will be brought back
to the homepage, but now with their username and a user icon in the top-right, where the log-in button used to be. Hovering over this will bring about 
a dropdown menu, with which they can view the articles they've submitted (and their status), adjust their settings (including their password and information),
or logout. Furthermore, logged-in users can now click on the publish button in the navigation menu and be brought to a submission form. Here they can fill
in the information and content of a research paper that they wrote and submit it to an editor. After submission, they will be brought to their "My Articles" page, and now see a log of their submissions and other information on each, including the status.

Editors are the other type of user, as opposed to researcher, with much different functionality in their website. Upon logging-in (or registering) as
an editor, the user will be brought to their one and only page, titled "Articles to Edit". This will display all of the submitted articles to which they
were randomly assigned. Here they can select any of these articles, edit them accordingly, and choose to either publish the final product, thus updating
its status and allowing it to be displayed on the website, or they can reject the submission.

Also, at the bottom of every page is the copyright bar, as this amazing website will likely be targeted by nefarious online hackers looking to steal the 
priceless contents within.

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

## Contact

Krishi Kishore - kkishore@college.harvard.edu

Jake Pappo - jakepappo@college.harvard.edu

Project Link - [https://github.com/krishikishore/revelation](https://github.com/krishikishore/revelation)

## Acknowledgements

- [https://www.w3schools.com/](https://www.w3schools.com/)
- [https://stackoverflow.com/questions/45455993/resource-corpora-stopwords-not-found](https://stackoverflow.com/questions/45455993/resource-corpora-stopwords-not-found)
- [https://stackoverflow.com/questions/41940663/how-can-i-change-the-host-and-port-that-the-flask-command-uses](https://stackoverflow.com/questions/41940663/how-can-i-change-the-host-and-port-that-the-flask-command-uses)
- [https://www.analyticsvidhya.com/blog/2020/11/words-that-matter-a-simple-guide-to-keyword-extraction-in-python/](https://www.analyticsvidhya.com/blog/2020/11/words-that-matter-a-simple-guide-to-keyword-extraction-in-python/)
- [https://stackoverflow.com/questions/28128400/keep-footer-at-the-bottom-of-the-page-with-scrolling-if-needed](https://stackoverflow.com/questions/28128400/keep-footer-at-the-bottom-of-the-page-with-scrolling-if-needed)
- [https://stackoverflow.com/questions/1052772/keyboard-shortcut-to-untab-move-a-block-of-code-to-the-left-in-eclipse-apt](https://stackoverflow.com/questions/1052772/keyboard-shortcut-to-untab-move-a-block-of-code-to-the-left-in-eclipse-apt)
- [https://www.codegrepper.com/code-examples/css/flask+render+template+not+getting+css](https://www.codegrepper.com/code-examples/css/flask+render+template+not+getting+css)
- [https://stackoverflow.com/questions/13415152/submit-post-form-from-url](https://stackoverflow.com/questions/13415152/submit-post-form-from-url)
- [https://www.nature.com/](https://www.nature.com/)
- [https://www.youtube.com/watch?v=FVH-tXVRErg](https://www.youtube.com/watch?v=FVH-tXVRErg)
- [https://www.hongkiat.com/blog/css-viewport-units-vw-vh-wmin-vmax/](https://www.hongkiat.com/blog/css-viewport-units-vw-vh-wmin-vmax/)
- [https://stackoverflow.com/questions/16318413/dropdown-menu-z-index-problems](https://stackoverflow.com/questions/16318413/dropdown-menu-z-index-problems)
- [https://support.mozilla.org/en-US/kb/websites-look-wrong-or-appear-differently](https://support.mozilla.org/en-US/kb/websites-look-wrong-or-appear-differently)
- [https://www.tutorialspoint.com/How-to-Insert-Hyperlink-in-HTML-Page](https://www.tutorialspoint.com/How-to-Insert-Hyperlink-in-HTML-Page)
