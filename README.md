# movie_theater_simulator
A program that simulates various patterns of customer arrival and queueing for movie theater ticket purchases. 
Simulates a variety of arrangements of ticket lines, ticket windows, and patterns of customer arrival.

Two arrangements:
* One or more ticket windows, each with its own separate ticket line.
* Multiple ticket windows, and one ticket line that all customers stand in; a customer can proceed from this single line to any available ticket window.

Configurations and customer arrivals are set as file inputs, in the file "simulation.txt".
Those parameters will be described in an input file, a text file that specifies the length of the simulation, 
the number of ticket windows, whether there is a single ticket line or a separate line for each window, and the speed at which customers are processed at each window. 
In addition, the input file will contain a sequence of customer arrivals, specifying how many customers will arrive at the theater at which times. 
