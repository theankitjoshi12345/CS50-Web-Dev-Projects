# CS50 Web Development Projects

Learning projects for CS50's Web Programming with Python and JavaScript. This private repository collects exercises in Django, SQL-backed models, HTML/CSS, JavaScript, and browser-to-server requests.

## Projects
| Directory | Focus |
| --- | --- |
| `google/` | Search interface pages using HTML and CSS |
| `wiki/` | Markdown encyclopedia with search and entry management |
| `commerce/` | Auctions, listings, bids, categories, watchlists, and comments |
| `mail/` | Mail interface using JavaScript and Django email API routes |
| `project4/` | Social-network posts, profiles, following, editing, and likes |

These are coursework implementations. Completion, grading results, production readiness, and comprehensive test coverage are not asserted.

## Run a Django project locally
Use an isolated Python environment. The available dependency file is `mail/requirements.txt`; it specifies Django and psycopg2:
```sh
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r mail/requirements.txt
cd mail
python3 manage.py migrate
python3 manage.py runserver
```
Open http://127.0.0.1:8000. Each Django project has its own `manage.py`, settings, and database. Adapt the directory for the project being reviewed. The static `google/` pages can be opened directly in a browser.

## API work to inspect
The mail application defines routes for composing email, reading/updating an email, and retrieving mailboxes. The network project defines routes for posts, profiles, following, edits, and likes. These provide examples of frontend/backend interaction; they are not Anthropic or Gemini integrations.

## Private review and deployment limits
Keep assessment solutions private in accordance with [CS50's academic-honesty policy](https://cs50.harvard.edu/web/honesty/). Reviewer access should respect that policy.

Committed SQLite databases, development settings, and generated files are present. Use fresh local data and review settings before deployment; do not expose these databases or reuse development credentials in production. The included Django development server is for local use. No hosted demo is claimed.

## Attribution and license
Course materials and starter files originate from CS50/Harvard. See [LICENSE](LICENSE) for the limited scope covering original contributions; it does not relicense course materials or override academic-honesty requirements.
