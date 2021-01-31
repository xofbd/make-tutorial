# GNU Make Tutorial

[GNU Make](https://www.gnu.org/software/make/) is a build automation tool; it enables you to easily build/install a project. It is a great tool for data science projects as it

* makes your results reproducible for not only you but others.
* only runs the necessary parts of your pipeline/workflow.
* creates a self-documenting source file.
* can be used for common development tasks such as unit testing and linting.

A great way to learn how to use GNU Make is through an actual project. Let's try to answer the following question: when did most movies begin to be filmed in color? This repository contains the necessary code to answer the posed question.

## Getting started
1. Install GNU Make on your computer. Most Unix like operating systems already have GNU Make pre-installed, but you may need to check by running `make --version`. For Windows users, you will need to first install [Cygwin](https://www.cygwin.com/) and then install GNU Make.

1. Create an account on [RapidAPI](https://rapidapi.com) and obtain an API key. Once you have, create a file named `.env` in the root directory with your API key like this:
   ```bash
   API_KEY=<your-key-here>
   ```
   Note, if you do not obtain an API key, the scripts will still run but will simulate obtaining the data from RapidAPI. Look at the documentation of `src/film_color.py` for more details.
1. Run `make all`.

## Approach
To answer the posed question, we scrape Wikipedia to obtain a list of Oscar nominees for Best Picture throughout the years. Afterwards, we use a web API provided by RapidAPI to get the film color data. Finally, the results are analyzed and a figure produced showing the fraction of films in color throughout the years. The main files are:

* `src/oscar_nominees.py`: creates a CSV of films to analyze
* `src/film_color.py`: creates a CSV with the film data
* `src/color_films_by_year.py`: creates a PNG visualizing the results
* `requirements.txt`: provides the necessary packages to run the project using a Python virtual environment

## Future work
Here's a list of suggestions for additions and changes to the project. Some deal directly with GNU Make but others focus on improving the analysis. Either way, you'll want to make the appropriate changes to the `Makefile`.

### Project improvements
1. At the moment, only about five movies are analyzed for each year. It would be better if we included more movies. Consider obtaining more movies for each year. Should you consider other Oscar nominated movies? What about the top grossing films for each year?

1. The process of obtaining the film data is not perfect. For example, currently, no information on the film color was obtained for *In Old Arizona*. Why was that the case? Can you see if there are ways to improve the code to gather more film data?

1. Apart from information about the color of the movie, the web API also returns other fields such as movie run time. Can you come up with other questions that can be answered using the API? How has the average movie length changed across the years?

1. Some movies have both "Color"" and "Black and White" listed for the type of film used. For example, *Forrest Gump* is a movie that is mostly in color with a few black and white scenes. Currently, any movie where the color field lists "Color" is labeled only as color. Is there a better way to improve on the labeling of films?

1. Looking up information about whether a film is in black or white or color is tedious. In fact, that is why we used data science techniques to answer the posed question. However, the process is not 100% perfect and trying to extend the code to cover all edge cases may be impossible or impractical. What if we manually looked up the movies to fill in some of holes in the data? How would you best implement incorporating manually gathered data? Consider reproducibility and properly documenting the process.

1. Currently, `src/color_films_by_year.py` both cleans up the obtained film data and creates the visualization. Perhaps a better approach is to apply separation of concerns and break that file into two. One file cleans up and processes the obtained film data while the other uses those processed results to create the visualization.

1. Tools such as [Pipenv](https://pipenv.pypa.io), [pip-tools](https://github.com/jazzband/pip-tools), and [Poetry](https://python-poetry.org) can help us separate packages needed for development and production and create deterministic builds. Currently, several packages listed in `requirements.txt` are only used for testing. How would you incorporate the usage of these tools in the `Makefile`?

### Makefile improvements
1. Make sure you go through your `Makefile` and use special variables. In a recipe, `$@` is equal to the target, `$<` is the first dependency, and `$^` is equal to all the dependencies of the target.

1. Is there anywhere you are repeating yourself? You can define a variable at the top of the `Makefile` and use it throughout. For example:

1. Create a rule or rules that allow for unit testing and linting. Unit testing and linting can be run by, with the virtual environment activated, `pytest -s tests` and `flake8 src`, respectively.

1. At the moment, the Python source file used to generate a particular file is **not** included as a prerequisite. Should it? What would be some pros and cons? How would you rewrite some of the recipes by considering the source file as a listed prerequisite?

1. There are a two types of prerequisites, normal and order-only. Take a look at the documentation for [order-only prerequisites](https://www.gnu.org/software/make/manual/html_node/Prerequisite-Types.html). Can you consider a place to use them in the current `Makefile`?

## Useful tips

1. By default, running `make` looks for a file named `Makefile`. To use a different file, use the `--file` option:
   ```
   make --file=Makefile-alt all
   ```

1. If you ever need to force the building of a target, you can use `-B` or `--always-make` option:
   ```
   make -B color_films_by_year.png
   ```
1. Sometimes it's nice to see what GNU Make will do rather than actually running the build. To have GNU Make do a "dry run" use the `--dry-run` option:
   ```
   make --dry-run color_films_by_year.png
   ```

## Additional resources
Here's a list of additional resources for GNU Make, ranging from a cheat sheet to the official documentation.

* [Software Carpentry](https://swcarpentry.github.io/make-novice/) has a nice tutorial that goes into more details about GNU Make. They start with the basics and cover important topics like pattern rules and functions.

* [Managing Projects with GNU Make](https://freecomputerbooks.com/Managing-Projects-with-GNU-Make.html) is a free book that takes a deep dive into the capabilities and power of GNU Make. While the book probably contains content that you'll never use, it's always good to see what is possible with GNU Make. You may want to look into this book once you've gotten a good handle on the basics of GNU Make.

* A nice [cheat sheet](https://devhints.io/makefile) as a quick reference. Also, consider their other cheat sheets like their [Bash scripting cheat sheet](https://devhints.io/bash).

* As always, it's worth looking at the [official documentation](https://www.gnu.org/software/make/).

## License
The project uses the GNU General Public License v3.0. The full license can be found in `LICENSE`.
