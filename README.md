# Telegram Bicing Bot 🚴

Bicing is a bicycle sharing system in Barcelona with stations distributed
throughout the city that include many docks for bikes. This project consists
of a Telegram Bot that answers questions related to geometric graphs defined
over Bicing stations. Some of the answers are given by plotting graphs over
maps to ease the visualization of the output.

## Project Structure

Our project has two main parts:

* **`bot.py`**: This file contains the Telegram Bot.
* **`data.py`**: This file contains functions related to geometric graphs and
other related topics that are used by the Bot. Although the functions are
oriented to Bicing database, they can be easily modifiable to work with other
similar databases.

## Getting Started

The following instructions will help you to install all the prerequisites to
run and use both the Telegram Bot and the functions it's based on.

### Prerequisites

#### To use the Bot

To use the Telegram Bot, you only need to have a device with Telegram installed
on it. You can download it to your Desktop or use it online in
[this webpage](https://telegram.org/) or download it in your preferred app store
if you are using a smartphone. After downloading Telegram, you will need to
create an account, but don't worry, it's free! 😊

#### To use the code behind the Bot

The Bot uses Python functions related to geometric graphs. If you want to run
this code separately, you will need to install Python 3 in your computer. You
can find the instructions to do so in the official
[webpage](https://www.python.org/downloads/).

### Installing

Nothing else is needed to use the Telegram Bot. However, to use the Python
functions you will have to install some libraries. Run the following command
in any directory with the `requirements.txt` file in it:

```{bash}
pip install -r requirements.txt
```
You shouldn't have any problemes using `pip` because it comes together with
the latest Python versions. If some error occurs, just upgrade your `pip`
version or install `pip` by using this
[link](https://pip.pypa.io/en/stable/installing/).

## Features

In the [Commands](#commands) section you'll find the available commands for the
Bot, that can also handle most [errors and warnings](#errors-and-warnings).

### Commands

Bot commands follow a `/command <arguments>` structure. Available commands are:

- `/start`

Gives a welcoming message to the user.

- `/authors`

Gives information and emails of the authors.

- `/help`

Gives brief instructions about the Bot commands.
    
- `/graph <distance>`

If `distance` (in meters) is specified and it's a float number, creates a geometric graph
over Bicing stations. All the stations are the nodes and two of them are
connected if their distance is lower or equal to `distance`. If it's not
specified, the default value is 1000.
    
- `/nodes`

Gives the number of nodes (stations) of the (previously created) graph.
    

- `/components`

Gives the number of connected components of the (previously created) graph.

- `/edges`

Gives the number of edges of the (previously created) graph.

- `/plotgraph`

Shows a map of the current graph with its edges.

- `/route <origin>, <destination>`

Given two valid addresses in Barcelona, finds the shortest route between
them. The given route has a walking part towards the first Bicing station (if
it's the case), a cycling path between connected stations and, finally, it can have
another walking part towards the destination. The section of the path that is 
traveled walking appears in green whereas the one traveled on bike appears in
blue, to make things more visual for the user. It also gives a linear approximation
of the time that it takes to travel between the addresses, considering that
you travel on foot at 4 km/h and at 10 km/h by bike.

- `/valid_route <origin>, <destination>`

It does the same as the previous `/route` command. However, it is guaranteed that
the route is available at that moment, that is, that the first station visited has
at least a bike and the last station has at least a dock.

- `/distribute <min_bikes>, <min_docks>`

Given a minimum number of bikes for each station `min_bikes` and a minimum
number of empty docks for each station `min_docks`, this command returns the
minimum transportation cost of bikes and the edge with the highest cost. We
can move bikes around the geometric graph to get to a solution in which all 
the stations meet the requirements. The cost of a solution is defined as the sum 
of the distances of each moving bike, then the edge with the highest cost is 
the one with maximum distance\*number of moving bikes.

### Errors and warnings

The most common errors and possible warnings are handled by the Bot, that
returns a message to the user. The authors have tried to made these messages
both brief and clear.

## Execution and testing

To execute the Telegram Bot, search for it username in Telegram's search bar.
Its username is @bicing2019. 

### Telegram Bot Tests

In this section you can find examples and tests of the Telegram Bot. Note that
all the tests for the Telegram Bot are implicit tests of the `data.py` functions. 

#### Simple commands

When you open for the first time the bot, you'll find something similar to this:

<center><img src='/images/restart.jpg' width='100'></center>

After clicking on **Start** or **Restart**, you'll be able to call your first
commands. Here you can find some screenshots showing how to use basic commands.

<center><img src='/images/start.jpg' height='100'></center>
<center><img src='/images/help.jpg' height='100'></center>
<center><img src='/images/basic.jpg' height='100'></center>

#### Plotgraph
#### Routes
#### Distribute
#### Route vs. Valid Route
#### Errors and warnings
* CHECK REGULAR FUNCTIONS
* PLOTGRAPHS WITH FEW EDGES (d = 100) AND QUITE SOME (d = 700)
* RUTES (BONICA, LLARGA, CURTA, en el mateix punt, caminada i inventada)
* DISTRIBUTE (working, not bikes, not docks, not answer, not capcity, nothing to do)
* VALID_ROUTE (one doesnt change, one does)

## Design Choices

* We have decided to implement the geometric graph without assuming that the
earth is flat in a small region, but rather taking into account latitude
and longitude, and considering always the worst case (since the distance equivalent 
to a degree of longitude depends on which latitude we are at), this is more deeply
explained in the comments of the function `geometric_graph` code.

* We have decided that in order to get the geometric graph, it is strictly
necessary to first use the command `/graph`, that is, when calling a function
that needs this graph when was not previously calculated, the bot will send 
a message to the user and not just initialize the graph with default value.
We have thought to do it this way because the user may have forgot to declare
the graph and would therefore obtain information about a graph which hasn't 
choosed.

* We have decided to implement another command, `/valid_route`, because we want
our bot to be useful for the user, and the route command wasn't enough
because the user could arrive to a station with no bikes or be unlable 
to return the bike at the end of the path.

* In both `/route` and `/valid_route` commands, we thought that it is useful
for the user to have an approximated time of travelling, as it was explained
in the [Commands](#commands) section. Moreover, when showing a route, we emphasise
the origin and destination points with a bigger marker to make visualization easier.

* Note that each time we call the command `/graph` we update the Bicing information.
We choosed this option because it keeps up-to-date data and the user doesn't have
to remember to use other commands (like `/start`) each time it wants to refresh it.

## Built With

Our [Telegram](https://telegram.org/) Bot is build with [Python](https://www.python.org).

## Authors

* **Max Balsells** - <max.balsells.i@est.fib.upc.edu>
* **Maria Prat** - <maria.prat@est.fib.upc.edu>

## References

* [Project statement.](https://github.com/jordi-petit/ap2-bicingbot-2019)
* [How to create a Telegram Bot.](https://github.com/jordi-petit/exemples-telegram)
* [Bicing data.](https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_information)
* [NetworkX tutorial.](https://networkx.github.io/documentation/stable/tutorial.html)
