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

## Input Phase
print("Exit loop by typing 'exit()' or wait for End of File")
query = input("Enter Your search: ")

## Processing and Output Phase
# continue loop until user inputs exit value or until EOF
while (query != "exit()"):
    # outputs search query
    for i in (search(query, advanced=True)):
        print(i)

    # delay will prevent abuse
    delay = round(random.uniform(3, 10), 2)    # random values chosen
    time.sleep(delay)

    # reinsert query for new search
    query = input("\nEnter your search: ")

# End program
print("Program terminating...")

# EOF: googleSearch.py
