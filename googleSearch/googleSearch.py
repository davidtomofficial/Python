################################################################################
##   googleSearch.py - Python 3.6                                             ##
##   August 2023 David Tom - David Tom                                        ##
##   https://github.com/davidtomofficial                                          ##
################################################################################
##   This program is free software: you can redistribute it and/or modify     ##
##   it under the terms of the GNU General Public License as published by     ##
##   the Free Software Foundation, either version 3 of the License, or        ##
##   (at your option) any later version.                                      ##
##                                                                            ##
##   This program is distributed in the hope that it will be useful,          ##
##   but WITHOUT ANY WARRANTY; without even the implied warranty of           ##
##   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            ##
##   GNU General Public License for more details.                             ##
##                                                                            ##
##   You should have received a copy of the GNU General Public License        ##
##   along with this program.  If not, see <https://www.gnu.org/licenses/>.   ##
################################################################################

## Import Dependencies
from googlesearch import search
import random
import time

def main():
    print("Exit by typing 'exit()' or reaching End of File")
    while True:
        try:
            query = input("Enter your search: ").strip()
        except EOFError:
            break
        if query == "exit()":
            break
        if not query:
            continue

        for result in search(query, advanced=True):
            print(result)

        # Space successive searches; remote service limits still apply.
        time.sleep(round(random.uniform(3, 10), 2))

    print("Program terminating...")


if __name__ == '__main__':
    main()

# EOF: googleSearch.py
