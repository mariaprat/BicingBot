# Telegram Bicing Bot 🚲🚴

Bicing is a bicycle sharing system in Barcelona with stations distributed throughout the city that include many docks for bikes. This project consists of a Telegram Bot that answers questions related to geometric graphs defined over Bicing stations. Some of the answers are given by plotting graphs over maps to easily visualize the output. 

## Project Structure

Our project has two main parts:

* **`bot.py`**: This file contains the Telegram Bot.
* **`data.py`**: This file contains functions related to geometric graphs and other related topics that are used by the Bot but can be used separately.
 
## Getting Started

The following instructions will help you to install all the prerequisites to run and use both the Telegram Bot and the functions its based on.

### Prerequisites

#### To use the Bot

To use the Telegram Bot, you only need to have a device with Telegram installed. You can download it to your Desktop or use it online in [this webpage](https://telegram.org/) or download it in your preferred app store. After downloading Telegram, you will need to create a free account :).

#### To use the code behind the Bot

The Bot uses Python functions related to geometric graphs. If you want to run this code separately, you will need to install Python 3 in your computer. You can find the instructions to do so in the official [webpage](https://www.python.org/downloads/).

### Installing

Nothing else is needed to use the Telegram Bot. However, to use the Python functions you will have to install some libraries. Run the following commands in any directory with the `requirements.txt` file:

```{bash}
pip install -r requirements.txt
```
You shouldn't have any problemes using `pip` because it comes togheter with latest Python versions. If some error occurs, just upgrade your `pip` version or install `pip` by following this [link](https://pip.pypa.io/en/stable/installing/).

## Features

## Execution and testing

### Telegram Bot Tests

### `data.py` Tests

## Design Choices

## Built With

Our [Telegram](https://telegram.org/) Bot is build with [Python](https://www.python.org).

## Authors

* **Max Balsells** - <max.balsells.i@est.fib.upc.edu>
* **Maria Prat** - <maria.prat@est.fib.upc.edu>

## License

?

## References

* [Project statement.](https://github.com/jordi-petit/ap2-bicingbot-2019)
* [How to create a Telegram Bot.](https://github.com/jordi-petit/exemples-telegram)
* [Bicing data.](https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_information)
* [NetworkX tutorial.](https://networkx.github.io/documentation/stable/tutorial.html)
